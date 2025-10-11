"""
# =============================================================================
    SISTEMA DE PONTO - MERCEARIA
    Versão: 2.0 Corrigida
    Data: Outubro 2025

    Sistema de controle de ponto para funcionáris com:
    - Registro via site (validação Wi-Fi)
    - Registro via WhatsApp (CallMeBot)
    - Relatórios automáticos
    - Backup mensal via Telegram
# =============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================

import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from functools import wraps
from datetime import datetime, date, timedelta, time
import pytz
from dateutil.relativedelta import relativedelta
import requests
from urllib.parse import quote
import os
import logging
from logging.handlers import RotatingFileHandler
import json

# 🔐 SEGURANÇA: Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()  # Carrega o arquivo .env

# =============================================================================
# TIMEZONE
# =============================================================================

TIMEZONE = pytz.timezone('America/Sao_Paulo')

def agora_sp():
    return datetime.now(TIMEZONE)

def hoje_sp():
    return agora_sp().date()

# =============================================================================
# LOGGING
# =============================================================================

if not os.path.exists('logs'):
    os.makedirs('logs')

whatsapp_logger = logging.getLogger('whatsapp_falhas')
whatsapp_logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('logs/whatsapp_falhas.log', maxBytes=1000000, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
whatsapp_logger.addHandler(handler)

falhas_whatsapp_hoje = []

# =============================================================================
# 🔐 FLASK - COM SEGURANÇA
# =============================================================================

app = Flask(__name__)

# ✅ Secret key do arquivo .env
app.secret_key = os.getenv('SECRET_KEY', 'fallback_chave_temporaria_MUDE_ISSO')

if app.secret_key == 'fallback_chave_temporaria_MUDE_ISSO':
    print("⚠️ AVISO: SECRET_KEY não configurada no .env!")

# =============================================================================
# 🔐 MYSQL - COM SEGURANÇA
# =============================================================================

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB', 'ponto_db')

if not MYSQL_PASSWORD:
    raise Exception("❌ ERRO: MYSQL_PASSWORD não configurada no .env!")

print("✅ Parte 1 carregada: Imports e Configurações Flask (SEGURA)")

# =============================================================================
# 🔐 WHATSAPP - COM SEGURANÇA
# =============================================================================

# ✅ Chaves do arquivo .env
CALLMEBOT_KEYS = {
    '+553175124667': os.getenv('CALLMEBOT_ADMIN'),
    '+553191932116': os.getenv('CALLMEBOT_MAISA'),
    '+553188179900': os.getenv('CALLMEBOT_IRLAINE'),
    '+553191909665': os.getenv('CALLMEBOT_TESTE'),
    '+553193731622': os.getenv('CALLMEBOT_TESTE1')
}

# Verificar se estão configuradas
for telefone, chave in CALLMEBOT_KEYS.items():
    if not chave:
        print(f"⚠️ AVISO: Chave CallMeBot não configurada para {telefone}")

URL_SITE = os.getenv('URL_SITE', 'seu-site.com')


# Horários (mantidos no código - não são sensíveis)
HORARIOS_FUNCIONARIAS = {
    'Maísa': {
        'seg': {'entrada': '08:00', 'saida': '18:00'},
        'ter': {'entrada': '08:00', 'saida': '18:00'},
        'qua': {'entrada': '08:00', 'saida': '18:00'},
        'qui': {'entrada': '08:00', 'saida': '18:00'},
        'sex': {'entrada': '08:00', 'saida': '18:00'},
        'sab': {'entrada': '08:00', 'saida': '14:00'},
        'dom': None
    },
    'Teste': {
        'seg': {'entrada': '08:00', 'saida': '18:00'},
        'ter': {'entrada': '08:00', 'saida': '18:00'},
        'qua': {'entrada': '08:00', 'saida': '18:00'},
        'qui': {'entrada': '08:00', 'saida': '18:00'},
        'sex': {'entrada': '08:00', 'saida': '18:00'},
        'sab': {'entrada': '08:00', 'saida': '14:00'},
        'dom': None
    }
}

# =============================================================================
# 🔐 TELEGRAM - COM SEGURANÇA
# =============================================================================

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

BACKUP_ATIVADO = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

if not BACKUP_ATIVADO:
    print("⚠️ AVISO: Telegram não configurado (backup desativado)")

print("✅ Parte 2 carregada: Configurações WhatsApp e Telegram (SEGURA)")

# =============================================================================
# FUNÇÕES BANCO DE DADOS - MySQL
# =============================================================================

def get_db():
    """
    Obtém conexão com banco de dados MySQL.
    Usa Flask 'g' para reutilizar conexão durante request.
    
    Returns:
        Connection: Conexão PyMySQL com DictCursor
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=DictCursor,
            autocommit=False,
            charset='utf8mb4'
        )
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Fecha conexão com banco ao final de cada request.
    Executado automaticamente pelo Flask.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
    Executa query SELECT no banco.
    
    Args:
        query (str): SQL query com placeholders %s
        args (tuple): Valores para substituir placeholders
        one (bool): Se True, retorna apenas 1 resultado
    
    Returns:
        dict/list: Dicionário (se one=True) ou lista de dicionários
    
    Exemplo:
        user = query_db('SELECT * FROM users WHERE id = %s', (user_id,), one=True)
        users = query_db('SELECT * FROM users WHERE tipo = %s', ('funcionaria',))
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute(query, args)
        rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """
    Executa query INSERT/UPDATE/DELETE no banco.
    Faz commit automático.
    
    Args:
        query (str): SQL query com placeholders %s
        args (tuple): Valores para substituir placeholders
    
    Returns:
        int: ID do último registro inserido (para INSERT)
    
    Exemplo:
        record_id = execute_db(
            'INSERT INTO records (user_id, data, hora_entrada) VALUES (%s, %s, %s)',
            (user_id, hoje, '08:00:00')
        )
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute(query, args)
        db.commit()
        return cur.lastrowid

# =============================================================================
# ✅ CORREÇÃO 4: Try/except para schema.sql + ✅ CORREÇÃO 10: Índices
# =============================================================================

def init_db():
    """
    Inicializa banco de dados COM PROTEÇÃO DE DADOS:
    1. Cria database se não existir (nunca apaga)
    2. Executa schema.sql APENAS se tabelas não existirem
    3. Cria índices para otimização
    4. Cria usuário admin padrão se não existir
    
    ⚠️ PROTEÇÃO: Nunca apaga dados existentes!
    """
    # Criar database (nunca apaga, só cria se não existir)
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        cursorclass=DictCursor,
        autocommit=True,
        charset='utf8mb4'
    )
    with conn.cursor() as cur:
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
    conn.close()
    
    # Conectar ao database criado
    db = get_db()
    with db.cursor() as cur:
        # 🛡️ PROTEÇÃO: Verificar se tabelas já existem
        cur.execute("""
            SELECT COUNT(*) as total 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_name = 'users'
        """, (MYSQL_DB,))
        
        resultado = cur.fetchone()
        tabelas_existem = resultado['total'] > 0
        
        if tabelas_existem:
            print("✅ BANCO DE DADOS JÁ EXISTE - Dados preservados!")
            print(f"   Database: {MYSQL_DB}")
            
            # Contar registros existentes
            try:
                cur.execute("SELECT COUNT(*) as total FROM users")
                users = cur.fetchone()
                cur.execute("SELECT COUNT(*) as total FROM records")
                records = cur.fetchone()
                print(f"   👥 Usuários: {users['total']}")
                print(f"   📊 Registros de ponto: {records['total']}")
            except:
                pass
        else:
            print("📦 PRIMEIRA EXECUÇÃO - Criando tabelas...")
            # Tentar executar schema.sql
            try:
                with open('schema.sql', 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                # Executar cada statement separadamente
                for statement in schema_sql.split(';'):
                    stmt = statement.strip()
                    if stmt:
                        cur.execute(stmt)
                db.commit()
                print("✅ Tabelas criadas com sucesso!")
            
            except FileNotFoundError:
                print("⚠️ AVISO: schema.sql não encontrado!")
                print("   O sistema pode não funcionar corretamente.")
                print("   Verifique se o arquivo schema.sql existe na raiz do projeto.")
            
            except Exception as e:
                print(f"❌ ERRO CRÍTICO ao executar schema.sql: {e}")
                print("   O sistema NÃO poderá funcionar corretamente!")
                raise
        
        # Criar índices (sempre verifica, nunca quebra se já existir)
        print("🔍 Verificando índices...")
        indices_config = [
            ("idx_records_user_data", "records", "user_id, data"),
            ("idx_records_data", "records", "data"),
            ("idx_users_telefone", "users", "telefone"),
            ("idx_solicitacoes_status", "solicitacoes_correcao", "status")
        ]
        
        for nome_indice, tabela, colunas in indices_config:
            try:
                cur.execute("""
                    SELECT COUNT(*) as existe
                    FROM information_schema.statistics 
                    WHERE table_schema = DATABASE()
                    AND table_name = %s
                    AND index_name = %s
                """, (tabela, nome_indice))
                
                resultado = cur.fetchone()
                
                if resultado['existe'] == 0:
                    query = f"CREATE INDEX {nome_indice} ON {tabela} ({colunas})"
                    cur.execute(query)
                    print(f"   ✅ Índice {nome_indice} criado")
                else:
                    print(f"   ℹ️ Índice {nome_indice} OK")
            
            except Exception as e:
                print(f"   ⚠️ Erro no índice {nome_indice}: {e}")
        
        db.commit()
        print("✅ Índices verificados!")
        
        # Criar usuário admin APENAS se não existir
        cur.execute("SELECT * FROM users WHERE tipo = 'admin' LIMIT 1")
        admin = cur.fetchone()
        
        if not admin:
            senha_admin = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
            cur.execute(
                "INSERT INTO users (nome, username, senha, tipo) VALUES (%s, %s, %s, 'admin')",
                ('Administrador', 'admin', senha_admin)
            )
            db.commit()
            print("✅ Usuário admin criado!")
            print("   Login: admin")
            print("   Senha: admin123")
            print("   ⚠️ TROQUE A SENHA após primeiro login!")
        else:
            print("✅ Usuário admin já existe")

# =============================================================================
# DECORADORES DE AUTENTICAÇÃO
# =============================================================================

def login_required(f):
    """
    Decorator: Garante que usuário está logado.
    Redireciona para login se não estiver.
    
    Uso:
        @app.route('/dashboard')
        @login_required
        def dashboard():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator: Garante que usuário é admin.
    Redireciona para login se não for.
    
    Uso:
        @app.route('/admin/relatorios')
        @admin_required
        def relatorios():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('tipo') != 'admin':
            flash('Acesso negado.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =============================================================================
# ✅ CORREÇÃO 3: LIMPEZA DE DADOS ANTIGOS (13 MESES)
# =============================================================================

def cleanup_old_records():
    """
    Remove registros com mais de 13 meses (395 dias).
    
    Por quê 13 meses?
    - Cálculo de 13º precisa de dados do ano inteiro
    - 13 meses garante que sempre terá 12 meses completos
    - Exemplo: Em janeiro/2026, ainda terá dados de dezembro/2024
    
    Executado automaticamente antes de:
    - Listar registros no admin
    - Exibir tela da funcionária
    
    IMPORTANTE: Backup automático é feito ANTES da limpeza!
    """
    cutoff = hoje_sp() - timedelta(days=395)  # 13 meses
    execute_db("DELETE FROM records WHERE data < %s", (cutoff.isoformat(),))

# =============================================================================
# ✅ CORREÇÃO 9: FUNÇÃO ÚNICA DE FORMATAÇÃO (remove duplicação)
# =============================================================================

def format_hora(h):
    """
    Formata hora para exibição (HH:MM).
    Função centralizada - NÃO crie versões locais!
    
    Args:
        h: Pode ser None, datetime, time, timedelta ou string
    
    Returns:
        str: Hora formatada como 'HH:MM' ou '-' se None
    
    Exemplos:
        format_hora(None) → '-'
        format_hora(datetime(2025,10,4,8,30)) → '08:30'
        format_hora(timedelta(hours=8, minutes=30)) → '08:30'
        format_hora('08:30:00') → '08:30'
    """
    if h is None:
        return '-'
    
    # Se é timedelta (retorno do MySQL para TIME)
    if isinstance(h, timedelta):
        total_seg = int(h.total_seconds())
        horas = total_seg // 3600
        minutos = (total_seg % 3600) // 60
        return f"{horas:02d}:{minutos:02d}"
    
    # Se é datetime ou time
    if isinstance(h, (datetime, time)):
        return h.strftime('%H:%M')
    
    # Se é string, tentar converter
    try:
        dt = datetime.strptime(str(h), '%H:%M:%S')
        return dt.strftime('%H:%M')
    except:
        return str(h)

# =============================================================================
# CÁLCULO DE VALOR POR HORA E DIA
# =============================================================================

def calcular_valor_hora(data_trabalho, funcionaria_nome=None):
    """
    Calcula valor por hora baseado no dia da semana.
    Valores vêm do banco de dados (configuráveis pelo admin).
    
    Args:
        data_trabalho (date): Data do trabalho
        funcionaria_nome (str): Nome da funcionária (para regras futuras)
    
    Returns:
        float: Valor por hora
    """
    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
    tipo_dia = dias_semana[data_trabalho.weekday()]
    
    # Buscar valor configurado no banco
    config = query_db(
        "SELECT valor_hora FROM configuracoes_pagamento WHERE tipo_dia = %s AND ativo = 1",
        (tipo_dia,),
        one=True
    )
    
    # Se encontrou no banco, usa o valor configurado
    if config:
        return float(config['valor_hora'])
    
    # Fallback: Se não tem no banco, usa valores antigos (retrocompatibilidade)
    print(f"⚠️ AVISO: Valor não encontrado no banco para {tipo_dia}. Usando fallback.")
    return 10.0 if data_trabalho.weekday() == 6 else 6.9

def calcular_valor_dia(data_trabalho, hora_entrada, hora_saida, funcionaria_nome=None):
    """
    Calcula total de horas trabalhadas e valor do dia.
    
    Args:
        data_trabalho (date): Data do trabalho
        hora_entrada (time): Hora de entrada
        hora_saida (time): Hora de saída
        funcionaria_nome (str): Nome da funcionária
    
    Returns:
        tuple: (horas_trabalhadas timedelta, valor float)
    
    Exemplo:
        horas, valor = calcular_valor_dia(date(2025,10,4), time(8,0), time(18,0))
        # horas = timedelta(hours=10)
        # valor = 69.0 (10 horas × R$ 6,90)
    """
    if not hora_entrada or not hora_saida:
        return None, 0
    
    # Calcular diferença
    dt_entrada = datetime.combine(date.today(), hora_entrada)
    dt_saida = datetime.combine(date.today(), hora_saida)
    horas_trabalhadas = dt_saida - dt_entrada
    
    # Converter para decimal
    horas_dec = horas_trabalhadas.total_seconds() / 3600
    
    # Calcular valor
    valor_hora = calcular_valor_hora(data_trabalho, funcionaria_nome)
    valor = round(horas_dec * valor_hora, 2)
    
    return horas_trabalhadas, valor

def funcionaria_trabalha_hoje(nome, dia_semana):
    """
    Verifica se funcionária trabalha em determinado dia.
    
    Args:
        nome (str): Nome da funcionária
        dia_semana (str): 'seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom'
    
    Returns:
        dict ou None: {'entrada': 'HH:MM', 'saida': 'HH:MM'} ou None
    
    Exemplo:
        horario = funcionaria_trabalha_hoje('Maísa', 'seg')
        # horario = {'entrada': '08:00', 'saida': '18:00'}
    """
    horarios = HORARIOS_FUNCIONARIAS.get(nome)
    if not horarios:
        return None
    return horarios.get(dia_semana)

print("✅ Parte 3 carregada: Funções de Banco e Auxiliares")

# =============================================================================
# FUNÇÕES WHATSAPP - CallMeBot
# =============================================================================

def enviar_whatsapp(telefone, mensagem):
    """
    Envia mensagem via WhatsApp usando CallMeBot.
    
    ✅ CORREÇÃO 6: Agora registra falhas em log + lista para relatório diário
    
    Args:
        telefone (str): Número com DDI (ex: '+5531999999999')
        mensagem (str): Texto da mensagem (markdown básico suportado)
    
    Returns:
        bool: True se enviou com sucesso, False se erro
    
    Observações:
        - Usa escape \n para quebra de linha
        - Suporta *negrito*, _itálico_
        - Timeout de 10 segundos
        - Falhas são registradas em logs/whatsapp_falhas.log
    """
    global falhas_whatsapp_hoje
    
    try:
        # Buscar chave do telefone
        apikey = CALLMEBOT_KEYS.get(telefone)
        
        if not apikey:
            erro = f"Chave não configurada para {telefone}"
            whatsapp_logger.error(erro)
            falhas_whatsapp_hoje.append({
                'telefone': telefone,
                'erro': erro,
                'timestamp': agora_sp().isoformat()
            })
            print(f"❌ {erro}")
            return False
        
        # Limpar telefone (remover caracteres especiais)
        phone = telefone.replace('+', '').replace('-', '').replace(' ', '')
        
        # Codificar mensagem para URL
        text = quote(mensagem)
        
        # Montar URL da API CallMeBot
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={text}&apikey={apikey}"
        
        # Enviar requisição com timeout
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ WhatsApp enviado para {telefone}")
            return True
        else:
            erro = f"Erro HTTP {response.status_code}: {response.text}"
            whatsapp_logger.error(f"{telefone} - {erro}")
            falhas_whatsapp_hoje.append({
                'telefone': telefone,
                'erro': erro,
                'timestamp': agora_sp().isoformat()
            })
            print(f"❌ {erro}")
            return False
    
    except requests.Timeout:
        erro = "Timeout (10s)"
        whatsapp_logger.error(f"{telefone} - {erro}")
        falhas_whatsapp_hoje.append({
            'telefone': telefone,
            'erro': erro,
            'timestamp': agora_sp().isoformat()
        })
        print(f"❌ Timeout ao enviar WhatsApp para {telefone}")
        return False
    
    except Exception as e:
        erro = str(e)
        whatsapp_logger.error(f"{telefone} - {erro}")
        falhas_whatsapp_hoje.append({
            'telefone': telefone,
            'erro': erro,
            'timestamp': agora_sp().isoformat()
        })
        print(f"❌ Erro ao enviar WhatsApp: {e}")
        return False

# =============================================================================
# ✅ CORREÇÃO 2: WEBHOOK SEM VALIDAÇÃO WI-FI (estava incorreta!)
# =============================================================================

@app.route('/webhook/whatsapp', methods=['POST', 'GET'])
def webhook_whatsapp():
    """
    Recebe mensagens do WhatsApp via CallMeBot.
    
    ✅ IMPORTANTE: SEM validação de Wi-Fi!
    Motivo: IP do request é do servidor CallMeBot, não da funcionária.
    
    Comandos aceitos:
    - 'entrada', 'oi', 'bom dia', 'cheguei' → Registra entrada
    - 'saida', 'saída', 'tchau', 'até', 'fui' → Registra saída
    - 'ponto', 'status', 'hoje' → Consulta ponto do dia
    
    ⚠️ SOBRE LOCALIZAÇÃO:
    Não há como validar localização via WhatsApp!
    Recomendações:
    1. Confie nas funcionárias
    2. Monitore padrões suspeitos (sempre mesma hora exata)
    3. Cruze com câmeras da loja (se tiver)
    4. Em caso de suspeita, peça foto da tela do celular com localização
    
    Retorna sempre '200 OK' para CallMeBot não reenviar.
    """
    try:
        # CallMeBot envia dados via GET params
        telefone = request.args.get('phone')  # Sem o '+'
        mensagem = request.args.get('text', '').lower().strip()
        
        if not telefone or not mensagem:
            return "OK", 200
        
        # Adicionar '+' ao telefone
        telefone_formatado = f"+{telefone}"
        
        # Buscar funcionária pelo telefone
        funcionaria = query_db(
            "SELECT * FROM users WHERE telefone = %s AND tipo = 'funcionaria'",
            (telefone_formatado,),
            one=True
        )
        
        if not funcionaria:
            print(f"⚠️ Telefone não cadastrado: {telefone_formatado}")
            return "OK", 200
        
        # Pegar data/hora atual de São Paulo
        hoje = hoje_sp().isoformat()
        now_time = agora_sp().strftime('%H:%M:%S')
        
        # COMANDO: ENTRADA
        if any(palavra in mensagem for palavra in ['entrada', 'oi', 'bom dia', 'cheguei', 'olá', 'ola']):
            record = query_db(
                "SELECT * FROM records WHERE user_id = %s AND data = %s",
                (funcionaria['id'], hoje),
                one=True
            )
            
            if record and record['hora_entrada']:
                resposta = f"⚠️ Você já registrou entrada hoje às {format_hora(record['hora_entrada'])}"
            else:
                # Registrar entrada
                if record:
                    execute_db(
                        "UPDATE records SET hora_entrada = %s WHERE id = %s",
                        (now_time, record['id'])
                    )
                else:
                    execute_db(
                        "INSERT INTO records (user_id, data, hora_entrada) VALUES (%s, %s, %s)",
                        (funcionaria['id'], hoje, now_time)
                    )
                
                resposta = (
                    f"✅ *Entrada registrada!*\n\n"
                    f"📅 Data: {hoje_sp().strftime('%d/%m/%Y')}\n"
                    f"🕐 Horário: {now_time[:5]}\n\n"
                    f"Tenha um ótimo dia! 💪"
                )
            
            enviar_whatsapp(telefone_formatado, resposta)
        
        # COMANDO: SAÍDA
        elif any(palavra in mensagem for palavra in ['saida', 'saída', 'tchau', 'ate', 'até', 'fui', 'indo']):
            record = query_db(
                "SELECT * FROM records WHERE user_id = %s AND data = %s",
                (funcionaria['id'], hoje),
                one=True
            )
            
            if not record or not record['hora_entrada']:
                resposta = "❌ Você ainda não registrou entrada hoje!"
            elif record['hora_saida']:
                resposta = f"⚠️ Você já registrou saída às {format_hora(record['hora_saida'])}"
            else:
                # Registrar saída
                execute_db(
                    "UPDATE records SET hora_saida = %s WHERE id = %s",
                    (now_time, record['id'])
                )
                
                # Calcular horas trabalhadas
                entrada_time = (
                    datetime.strptime(record['hora_entrada'], '%H:%M:%S').time()
                    if isinstance(record['hora_entrada'], str)
                    else record['hora_entrada']
                )
                saida_time = datetime.strptime(now_time, '%H:%M:%S').time()
                
                dt_entrada = datetime.combine(date.today(), entrada_time)
                dt_saida = datetime.combine(date.today(), saida_time)
                diff = dt_saida - dt_entrada
                
                horas = int(diff.total_seconds() // 3600)
                minutos = int((diff.total_seconds() % 3600) // 60)
                
                resposta = (
                    f"✅ *Saída registrada!*\n\n"
                    f"📊 RESUMO DO DIA:\n"
                    f"📅 Data: {hoje_sp().strftime('%d/%m/%Y')}\n"
                    f"🕐 Entrada: {format_hora(record['hora_entrada'])}\n"
                    f"🕔 Saída: {now_time[:5]}\n"
                    f"⏱️ Trabalhado: {horas}h{minutos:02d}m\n\n"
                    f"Dúvidas? Acesse: {URL_SITE}\n\n"
                    f"Até amanhã! 👋"
                )
            
            enviar_whatsapp(telefone_formatado, resposta)
        
        # COMANDO: CONSULTAR PONTO
        elif 'ponto' in mensagem or 'status' in mensagem or 'hoje' in mensagem:
            record = query_db(
                "SELECT * FROM records WHERE user_id = %s AND data = %s",
                (funcionaria['id'], hoje),
                one=True
            )
            
            if not record or not record['hora_entrada']:
                resposta = "📊 *Ponto de hoje*\n\nAinda não registrado."
            elif record['hora_saida']:
                entrada_time = (
                    datetime.strptime(record['hora_entrada'], '%H:%M:%S').time()
                    if isinstance(record['hora_entrada'], str)
                    else record['hora_entrada']
                )
                saida_time = (
                    datetime.strptime(record['hora_saida'], '%H:%M:%S').time()
                    if isinstance(record['hora_saida'], str)
                    else record['hora_saida']
                )
                
                dt_entrada = datetime.combine(date.today(), entrada_time)
                dt_saida = datetime.combine(date.today(), saida_time)
                diff = dt_saida - dt_entrada
                
                horas = int(diff.total_seconds() // 3600)
                minutos = int((diff.total_seconds() % 3600) // 60)
                
                resposta = (
                    f"📊 *Ponto de hoje*\n\n"
                    f"✅ Entrada: {format_hora(record['hora_entrada'])}\n"
                    f"✅ Saída: {format_hora(record['hora_saida'])}\n"
                    f"⏱️ Trabalhado: {horas}h{minutos:02d}m"
                )
            else:
                resposta = (
                    f"📊 *Ponto de hoje*\n\n"
                    f"✅ Entrada: {format_hora(record['hora_entrada'])}\n"
                    f"⏳ Saída: Ainda trabalhando..."
                )
            
            enviar_whatsapp(telefone_formatado, resposta)
        
        else:
            # Comando não reconhecido
            resposta = (
                "🤖 *Comandos disponíveis:*\n\n"
                "• Digite *entrada* para registrar entrada\n"
                "• Digite *saida* para registrar saída\n"
                "• Digite *ponto* para consultar seu ponto\n\n"
                "💡 Dica: 'oi', 'tchau' também funcionam!"
            )
            enviar_whatsapp(telefone_formatado, resposta)
        
        return "OK", 200
    
    except Exception as e:
        whatsapp_logger.error(f"Erro no webhook: {e}")
        print(f"❌ Erro no webhook: {e}")
        return "OK", 200

# =============================================================================
# ROTAS DE TESTE WHATSAPP (pode remover em produção)
# =============================================================================

@app.route('/testar-whatsapp')
# @login_required  # ← Descomente para exigir login
def testar_whatsapp():
    """
    Rota de teste: Envia mensagem para o número Teste.
    Acesse: /testar-whatsapp
    """
    telefone = '+553193731622'  # Teste1
    mensagem = "🎉 Teste de WhatsApp! Se você recebeu isso, está funcionando!"
    
    sucesso = enviar_whatsapp(telefone, mensagem)
    
    if sucesso:
        return "✅ Mensagem enviada! Verifique seu WhatsApp."
    else:
        return "❌ Erro ao enviar. Verifique logs/whatsapp_falhas.log"

@app.route('/testar-wpp/<telefone>')
def testar_wpp_numero(telefone):
    """
    Rota de teste: Envia mensagem para qualquer número.
    Exemplo: /testar-wpp/5531999999999
    """
    telefone_formatado = f"+{telefone}" if not telefone.startswith('+') else telefone
    mensagem = "🧪 Teste de WhatsApp! Se você recebeu isso, está funcionando!"
    
    sucesso = enviar_whatsapp(telefone_formatado, mensagem)
    
    if sucesso:
        return f"✅ Mensagem enviada para {telefone_formatado}!"
    else:
        return (
            f"❌ Erro ao enviar para {telefone_formatado}.<br><br>"
            f"Verifique:<br>"
            f"1. Chave CallMeBot configurada em CALLMEBOT_KEYS<br>"
            f"2. Número correto (com DDI)<br>"
            f"3. Arquivo logs/whatsapp_falhas.log para detalhes"
        )

print("✅ Parte 4 carregada: Funções e Webhook WhatsApp")

# =============================================================================
# ROTAS DE AUTENTICAÇÃO
# =============================================================================

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Página de login do sistema.
    Admin → Redireciona para /admin
    Funcionária → Redireciona para /funcionaria
    """
    session.pop('_flashes', None)

    if request.method == 'POST':
        username = request.form['username'].strip()
        senha = request.form['senha'].encode()
        
        user = query_db(
            "SELECT * FROM users WHERE username = %s",
            (username,),
            one=True
        )
        
        if user and bcrypt.checkpw(
            senha,
            user['senha'].encode() if isinstance(user['senha'], str) else user['senha']
        ):
            # Login bem-sucedido
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nome'] = user['nome']
            session['tipo'] = user['tipo']
            
            # Redirecionar baseado no tipo
            if user['tipo'] == 'funcionaria':
                return redirect(url_for('funcionaria'))
            else:
                return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha inválidos.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Faz logout e limpa sessão.
    """
    session.clear()
    return redirect(url_for('login'))

# =============================================================================
# ROTAS DA FUNCIONÁRIA
# =============================================================================

@app.route('/funcionaria', methods=['GET', 'POST'])
@login_required
def funcionaria():
    """
    Tela principal da funcionária.
    
    Funcionalidades:
    - Registrar entrada/saída (SEM validação Wi-Fi - removida)
    - Ver registro do dia
    - Ver histórico do mês
    - Ver solicitações de correção
    """
    if session.get('tipo') != 'funcionaria':
        flash('Acesso negado.')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    hoje = hoje_sp().isoformat()
    
    cleanup_old_records()
    
    if request.method == 'POST':
        try:
            # ✅ VALIDAÇÃO DE WI-FI REMOVIDA
            # Motivo: Não funciona com servidor externo (PythonAnywhere)
            # Segurança mantida via: Login + senha + revisão do admin
            
            acao = request.form.get('acao')
            now_time = agora_sp().strftime('%H:%M:%S')
            
            record = query_db(
                "SELECT * FROM records WHERE user_id = %s AND data = %s",
                (user_id, hoje),
                one=True
            )
            
            if acao == 'entrada':
                if record and record['hora_entrada']:
                    flash('Você já registrou entrada hoje.', 'warning')
                else:
                    if record:
                        execute_db(
                            "UPDATE records SET hora_entrada = %s WHERE id = %s",
                            (now_time, record['id'])
                        )
                    else:
                        execute_db(
                            "INSERT INTO records (user_id, data, hora_entrada) VALUES (%s, %s, %s)",
                            (user_id, hoje, now_time)
                        )
                    flash('✅ Entrada registrada com sucesso!', 'success')
            
            elif acao == 'saida':
                if not record or not record['hora_entrada']:
                    flash('Você ainda não registrou entrada hoje.', 'error')
                elif record['hora_saida']:
                    flash('Você já registrou saída hoje.', 'warning')
                else:
                    execute_db(
                        "UPDATE records SET hora_saida = %s WHERE id = %s",
                        (now_time, record['id'])
                    )
                    flash('✅ Saída registrada com sucesso!', 'success')
            
            return redirect(url_for('funcionaria'))
        
        except Exception as e:
            print(f"❌ ERRO AO REGISTRAR: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Erro ao registrar: {str(e)}', 'error')
            return redirect(url_for('funcionaria'))
    
    # GET - Buscar dados para exibir
    hoje_date = hoje_sp()
    
    # Registro de hoje
    record = query_db(
        "SELECT * FROM records WHERE user_id = %s AND data = %s",
        (user_id, hoje),
        one=True
    )
    
    entrada_fmt = format_hora(record['hora_entrada']) if record else None
    saida_fmt = format_hora(record['hora_saida']) if record else None
    
    # Pegar mês/ano da URL (se existir) ou usar mês atual
    mes_param = request.args.get('mes', type=int)
    ano_param = request.args.get('ano', type=int)
    
    if mes_param and ano_param:
        # Validar que não é futuro
        if ano_param > hoje_date.year or (ano_param == hoje_date.year and mes_param > hoje_date.month):
            mes_selecionado = hoje_date.month
            ano_selecionado = hoje_date.year
        else:
            mes_selecionado = mes_param
            ano_selecionado = ano_param
    else:
        mes_selecionado = hoje_date.month
        ano_selecionado = hoje_date.year
    
    # Buscar registros do mês selecionado
    registros_mes_raw = buscar_registros_mes(user_id, ano_selecionado, mes_selecionado)
    registros_mes = [processar_registro_para_exibicao(reg) for reg in registros_mes_raw]
    pendencias_count = contar_pendencias(registros_mes)
    
    # Nome do mês
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_atual = f"{meses[mes_selecionado - 1]} {ano_selecionado}"
    
    # Calcular mês anterior
    if mes_selecionado == 1:
        mes_anterior = 12
        ano_anterior = ano_selecionado - 1
    else:
        mes_anterior = mes_selecionado - 1
        ano_anterior = ano_selecionado
    
    # Calcular mês próximo
    if mes_selecionado == 12:
        mes_proximo = 1
        ano_proximo = ano_selecionado + 1
    else:
        mes_proximo = mes_selecionado + 1
        ano_proximo = ano_selecionado
    
    # Calcular limite de 13 meses atrás (395 dias)
    limite_dias = hoje_date - timedelta(days=395)
    limite_mes = limite_dias.month
    limite_ano = limite_dias.year
    
    # Verificar se pode voltar (não pode ir antes de 13 meses)
    data_anterior = date(ano_anterior, mes_anterior, 1)
    data_limite = date(limite_ano, limite_mes, 1)
    pode_voltar = data_anterior >= data_limite
    
    # Verificar se pode avançar (não pode ir para futuro)
    pode_avancar = (
        (ano_proximo < hoje_date.year) or
        (ano_proximo == hoje_date.year and mes_proximo <= hoje_date.month)
    )
    
    # Buscar solicitações da funcionária
    solicitacoes = query_db(
        """
        SELECT id, data_solicitacao, data_registro, tipo,
               horario_entrada, horario_saida, justificativa,
               status, observacao_admin, data_processamento
        FROM solicitacoes_correcao
        WHERE funcionaria_id = %s
        ORDER BY data_solicitacao DESC
        LIMIT 10
        """,
        (user_id,)
    )
    
    # Formatar solicitações para exibição
    solicitacoes_formatadas = []
    for sol in solicitacoes:
        # Formatar datas
        data_solic = sol['data_solicitacao']
        if isinstance(data_solic, str):
            data_solic = datetime.strptime(data_solic, '%Y-%m-%d %H:%M:%S')
        
        data_reg = sol['data_registro']
        if isinstance(data_reg, str):
            data_reg = datetime.strptime(data_reg, '%Y-%m-%d').date()
        
        data_proc = sol['data_processamento']
        if data_proc and isinstance(data_proc, str):
            data_proc = datetime.strptime(data_proc, '%Y-%m-%d %H:%M:%S')
        
        # Traduzir tipo
        tipo_label = {
            'entrada': 'Falta entrada',
            'saida': 'Falta saída',
            'ambos': 'Faltam Entrada e saída'
        }.get(sol['tipo'], sol['tipo'])
        
        # Status em português
        status_label = {
            'pendente': 'Pendente',
            'aprovado': 'Aprovado',
            'rejeitado': 'Rejeitado'
        }.get(sol['status'], sol['status'])
        
        # Formatar horários
        horario_entrada_fmt = format_hora(sol['horario_entrada']) if sol['horario_entrada'] else None
        horario_saida_fmt = format_hora(sol['horario_saida']) if sol['horario_saida'] else None
        
        solicitacoes_formatadas.append({
            'id': sol['id'],
            'data_solicitacao': data_solic.strftime('%d/%m/%Y às %H:%M'),
            'data_registro': data_reg.strftime('%d/%m/%Y'),
            'tipo': tipo_label,
            'status': sol['status'],
            'status_label': status_label,
            'horario_entrada': horario_entrada_fmt,
            'horario_saida': horario_saida_fmt,
            'observacao_admin': sol['observacao_admin'],
            'data_processamento': data_proc.strftime('%d/%m/%Y às %H:%M') if data_proc else None
        })
    
    return render_template(
        'func.html',
        nome=session['nome'],
        entrada=entrada_fmt,
        saida=saida_fmt,
        mes_atual=mes_atual,
        registros_mes=registros_mes,
        pendencias_count=pendencias_count,
        solicitacoes=solicitacoes_formatadas,
        mes_anterior=mes_anterior,
        ano_anterior=ano_anterior,
        mes_proximo=mes_proximo,
        ano_proximo=ano_proximo,
        pode_avancar=pode_avancar,
        pode_voltar=pode_voltar
    )
# =============================================================================
# FUNÇÕES AUXILIARES PARA HISTÓRICO DE PONTO
# =============================================================================

def buscar_registros_mes(user_id, ano, mes):
    """
    Busca todos os registros de ponto de um usuário em um mês específico.
    
    Args:
        user_id: ID do usuário
        ano: Ano (int)
        mes: Mês (int, 1-12)
    
    Returns:
        Lista de dicionários com os registros
    """
    primeiro_dia = date(ano, mes, 1)
    
    if mes == 12:
        ultimo_dia = date(ano, 12, 31)
    else:
        ultimo_dia = date(ano, mes + 1, 1) - timedelta(days=1)
    
    registros_raw = query_db("""
        SELECT data, hora_entrada, hora_saida
        FROM records
        WHERE user_id = %s AND data >= %s AND data <= %s
        ORDER BY data DESC
    """, (user_id, primeiro_dia.isoformat(), ultimo_dia.isoformat()))
    
    return registros_raw

def processar_registro_para_exibicao(registro):
    """
    Processa registro para exibição no template.
    Calcula status, ícone e horas trabalhadas.
    """
    data_obj = registro['data']
    if isinstance(data_obj, str):
        data_obj = datetime.strptime(data_obj, '%Y-%m-%d').date()
    
    if registro['hora_entrada'] and registro['hora_saida']:
        status_class = 'completo'
        icone = '✅'
        horas_trabalhadas = calcular_horas_trabalhadas(
            registro['hora_entrada'],
            registro['hora_saida']
        )
    elif registro['hora_entrada']:
        status_class = 'incompleto'
        icone = '⚠️'
        horas_trabalhadas = None
    else:
        status_class = 'ausente'
        icone = '❌'
        horas_trabalhadas = None
    
    return {
        'data': data_obj.strftime('%d/%m'),
        'entrada': format_hora(registro['hora_entrada']),
        'saida': format_hora(registro['hora_saida']),
        'horas_trabalhadas': horas_trabalhadas,
        'icone': icone,
        'status_class': status_class
    }

def calcular_horas_trabalhadas(hora_entrada, hora_saida):
    """
    Calcula diferença entre entrada e saída.
    Retorna string formatada 'Xh YYm' ou None.
    """
    try:
        if isinstance(hora_entrada, str):
            hora_entrada = datetime.strptime(hora_entrada, '%H:%M:%S').time()
        if isinstance(hora_saida, str):
            hora_saida = datetime.strptime(hora_saida, '%H:%M:%S').time()
        
        dt_entrada = datetime.combine(date.today(), hora_entrada)
        dt_saida = datetime.combine(date.today(), hora_saida)
        diff = dt_saida - dt_entrada
        
        horas = int(diff.total_seconds() // 3600)
        minutos = int((diff.total_seconds() % 3600) // 60)
        
        return f'{horas}h{minutos:02d}m'
    except:
        return None

def contar_pendencias(registros_processados):
    """
    Conta registros incompletos ou ausentes.
    """
    return sum(1 for r in registros_processados
               if r['status_class'] in ['incompleto', 'ausente'])

print("✅ Parte 5.1 carregada: Login e Funcionária")

# =============================================================================
# ROTAS DO ADMIN
# =============================================================================

@app.route('/admin')
@admin_required
def admin():
    """
    Dashboard do administrador.
    """
    try:
        pendentes = query_db(
            "SELECT COUNT(*) as total FROM solicitacoes_correcao WHERE status = 'pendente'",
            one=True
        )
        pendentes_count = pendentes['total'] if pendentes else 0
    except:
        pendentes_count = 0
    
    return render_template(
        'admin.html',
        nome=session['nome'],
        pendentes_count=pendentes_count
    )

@app.route('/admin/perfil', methods=['GET', 'POST'])
@admin_required
def editar_perfil_admin():
    """
    Editar perfil do administrador.
    """
    user_id = session['user_id']
    user = query_db(
        "SELECT * FROM users WHERE id = %s AND tipo = 'admin'",
        (user_id,),
        one=True
    )
    
    if not user:
        flash('Usuário admin não encontrado.')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        username = request.form['username'].strip()
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']
        
        if not nome or not username:
            flash('Nome e usuário são obrigatórios.')
            return redirect(url_for('editar_perfil_admin'))
        
        # Verificar se username já existe para outro usuário
        exists = query_db(
            "SELECT * FROM users WHERE username = %s AND id != %s",
            (username, user_id),
            one=True
        )
        if exists:
            flash('Nome de usuário já existe.')
            return redirect(url_for('editar_perfil_admin'))
        
        if senha:
            if senha != senha_confirm:
                flash('Senhas não conferem.')
                return redirect(url_for('editar_perfil_admin'))
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            execute_db(
                "UPDATE users SET nome = %s, username = %s, senha = %s WHERE id = %s",
                (nome, username, senha_hash, user_id)
            )
        else:
            execute_db(
                "UPDATE users SET nome = %s, username = %s WHERE id = %s",
                (nome, username, user_id)
            )
        
        # Atualizar sessão
        session['nome'] = nome
        session['username'] = username
        
        flash('Perfil atualizado com sucesso.')
        return redirect(url_for('admin'))
    
    return render_template('admin_perfil.html', user=user)

# =============================================================================
# ROTAS DE CONFIGURAÇÕES DO ADMIN
# =============================================================================

@app.route('/admin/configuracoes-pagamento', methods=['GET', 'POST'])
@admin_required
def configuracoes_pagamento():
    """
    Permite admin configurar valores de pagamento por dia da semana.
    
    GET: Exibe formulário com valores atuais
    POST: Salva novos valores no banco
    """
    if request.method == 'POST':
        try:
            dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
            valores_atualizados = 0
            
            for dia in dias:
                valor_form = request.form.get(f'valor_{dia}')
                
                if valor_form:
                    # Converter valor (aceita vírgula ou ponto)
                    valor_float = float(valor_form.replace(',', '.'))
                    
                    # Validar valor (entre 0.01 e 9999.99)
                    if valor_float < 0.01 or valor_float > 9999.99:
                        flash(f'❌ Valor inválido para {dia.capitalize()}: deve estar entre R$ 0,01 e R$ 9.999,99', 'error')
                        return redirect(url_for('configuracoes_pagamento'))
                    
                    # Atualizar no banco
                    execute_db(
                        """
                        UPDATE configuracoes_pagamento 
                        SET valor_hora = %s, 
                            atualizado_por = %s,
                            data_atualizacao = NOW()
                        WHERE tipo_dia = %s
                        """,
                        (valor_float, session['nome'], dia)
                    )
                    valores_atualizados += 1
            
            if valores_atualizados > 0:
                flash(f'✅ {valores_atualizados} valor(es) atualizado(s) com sucesso!', 'success')
            else:
                flash('⚠️ Nenhum valor foi alterado.', 'warning')
            
            return redirect(url_for('configuracoes_pagamento'))
        
        except ValueError as e:
            flash(f'❌ Erro ao processar valores: formato inválido. Use números com vírgula ou ponto.', 'error')
            return redirect(url_for('configuracoes_pagamento'))
        
        except Exception as e:
            flash(f'❌ Erro ao atualizar valores: {str(e)}', 'error')
            print(f"ERRO em configuracoes_pagamento: {e}")
            import traceback
            traceback.print_exc()
            return redirect(url_for('configuracoes_pagamento'))
    
    # GET - Buscar valores atuais do banco
    try:
        configuracoes = query_db("""
            SELECT 
                tipo_dia, 
                valor_hora, 
                DATE_FORMAT(data_atualizacao, '%%d/%%m/%%Y às %%H:%%i') as data_atualizacao_formatada,
                atualizado_por
            FROM configuracoes_pagamento 
            WHERE ativo = 1
            ORDER BY FIELD(tipo_dia, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo')
        """)
        
        # Se não tem dados no banco, criar registros padrão
        if not configuracoes:
            dias_padroes = [
                ('segunda', 6.90), ('terca', 6.90), ('quarta', 6.90), 
                ('quinta', 6.90), ('sexta', 6.90), ('sabado', 6.90), ('domingo', 10.00)
            ]
            
            for dia, valor in dias_padroes:
                execute_db(
                    "INSERT INTO configuracoes_pagamento (tipo_dia, valor_hora, atualizado_por) VALUES (%s, %s, %s)",
                    (dia, valor, 'Sistema - Inicialização')
                )
            
            
            return redirect(url_for('configuracoes_pagamento'))
        
        return render_template('admin_config_pagamento.html', configuracoes=configuracoes)

    except Exception as e:
        print(f"ERRO ao buscar configuracoes: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('admin'))

# =============================================================================
# ROTAS DE GERENCIAMENTO DE FUNCIONÁRIAS (CRUD)
# =============================================================================

@app.route('/admin/funcionarias')
@admin_required
def listar_funcionarias():
    """
    Lista todas as funcionárias.
    """
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    return render_template('funcionarias.html', users=users)

@app.route('/admin/funcionarias/novo', methods=['GET', 'POST'])
@admin_required
def nova_funcionaria():
    """
    Cria nova funcionária.
    """
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        username = request.form['username'].strip()
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']
        
        if not nome or not username or not senha:
            flash('Preencha todos os campos.')
            return redirect(url_for('nova_funcionaria'))
        
        if senha != senha_confirm:
            flash('Senhas não conferem.')
            return redirect(url_for('nova_funcionaria'))
        
        exists = query_db(
            "SELECT * FROM users WHERE username = %s",
            (username,),
            one=True
        )
        if exists:
            flash('Nome de usuário já existe.')
            return redirect(url_for('nova_funcionaria'))
        
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        execute_db(
            "INSERT INTO users (nome, username, senha, tipo) VALUES (%s, %s, %s, 'funcionaria')",
            (nome, username, senha_hash)
        )
        flash('Funcionária criada com sucesso.')
        return redirect(url_for('listar_funcionarias'))
    
    return render_template('funcionaria_form.html', acao='novo')

@app.route('/admin/funcionarias/editar/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def editar_funcionaria(user_id):
    """
    Edita funcionária existente.
    """
    user = query_db(
        "SELECT * FROM users WHERE id = %s AND tipo = 'funcionaria'",
        (user_id,),
        one=True
    )
    
    if not user:
        flash('Funcionária não encontrada.')
        return redirect(url_for('listar_funcionarias'))
    
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        username = request.form['username'].strip()  # ✅ NOVO
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']
        
        if not nome or not username:  # ✅ NOVO
            flash('Nome e usuário são obrigatórios.')
            return redirect(url_for('editar_funcionaria', user_id=user_id))
        
        # ✅ NOVO: Verificar se username já existe para outra funcionária
        exists = query_db(
            "SELECT * FROM users WHERE username = %s AND id != %s",
            (username, user_id),
            one=True
        )
        if exists:
            flash('Nome de usuário já existe.')
            return redirect(url_for('editar_funcionaria', user_id=user_id))
        
        if senha:
            if senha != senha_confirm:
                flash('Senhas não conferem.')
                return redirect(url_for('editar_funcionaria', user_id=user_id))
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            execute_db(
                "UPDATE users SET nome = %s, username = %s, senha = %s WHERE id = %s",  # ✅ NOVO
                (nome, username, senha_hash, user_id)
            )
        else:
            execute_db(
                "UPDATE users SET nome = %s, username = %s WHERE id = %s",  # ✅ NOVO
                (nome, username, user_id)
            )
        
        flash('Funcionária atualizada.')
        return redirect(url_for('listar_funcionarias'))
    
    return render_template('funcionaria_form.html', user=user, acao='editar')

@app.route('/admin/funcionarias/excluir/<int:user_id>', methods=['POST'])
@admin_required
def excluir_funcionaria(user_id):
    execute_db("DELETE FROM records WHERE user_id = %s", (user_id,))
    execute_db("DELETE FROM users WHERE id = %s AND tipo = 'funcionaria'", (user_id,))
    flash('Funcionária excluída.')
    return redirect(url_for('listar_funcionarias'))

print("✅ Parte 5.2 carregada: Admin e Funcionárias CRUD")

# =============================================================================
# ROTAS DE GERENCIAMENTO DE REGISTROS
# =============================================================================

@app.route('/admin/registros', methods=['GET', 'POST'])
@admin_required
def listar_registros():
    """
    Lista registros de ponto com filtro de período.
    """
    cleanup_old_records()
    
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    
    hoje = hoje_sp()
    data_fim_str = hoje.strftime('%Y-%m-%d')
    data_inicio_default = hoje - timedelta(days=89)
    data_inicio_str = data_inicio_default.strftime('%Y-%m-%d')
    
    def format_data(d):
        if d is None:
            return '-'
        if isinstance(d, (datetime, date)):
            return d.strftime('%d/%m/%Y')
        try:
            dt = datetime.strptime(d, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return d  # ✅ CORRIGIDO: retorna o valor original
    
    if request.method == 'POST':
        data_inicio_str = request.form.get('data_inicio')
        data_fim_str = request.form.get('data_fim')
        
        try:
            dt_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            dt_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            
            if dt_fim < dt_inicio:
                flash('Data fim deve ser maior ou igual à data início.')
                return redirect(url_for('listar_registros'))
            
            limite_min = hoje - timedelta(days=395)
            if dt_inicio < limite_min:
                dt_inicio = limite_min
                data_inicio_str = dt_inicio.strftime('%Y-%m-%d')
                flash('O período mínimo permitido é de até 13 meses atrás. Ajustado a data de início.')
            if dt_fim > hoje:
                dt_fim = hoje
                data_fim_str = dt_fim.strftime('%Y-%m-%d')
                flash('Data fim não pode ser depois de hoje. Ajustado.')
        except Exception:
            flash('Formato de data inválido.')
            return redirect(url_for('listar_registros'))
    else:
        dt_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        dt_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
    
    # ✅ CORRIGIDO: Query dentro do fluxo correto, sem vírgula extra
    registros_raw = query_db("""
        SELECT r.id, r.data, r.hora_entrada, r.hora_saida, r.observacoes, u.nome, u.id as user_id
        FROM records r
        JOIN users u ON r.user_id = u.id
        WHERE r.data BETWEEN %s AND %s
        ORDER BY u.nome ASC, r.data ASC
    """, (dt_inicio.isoformat(), dt_fim.isoformat()))
    
    registros_por_func = {}
    for r in registros_raw:
        user_nome = r['nome']
        if user_nome not in registros_por_func:
            registros_por_func[user_nome] = []
        
        data_fmt = format_data(r['data'])
        hora_entrada_fmt = format_hora(r['hora_entrada'])
        hora_saida_fmt = format_hora(r['hora_saida'])
        
        registros_por_func[user_nome].append({
            'id': r['id'],
            'data': data_fmt,
            'hora_entrada': hora_entrada_fmt,
            'hora_saida': hora_saida_fmt,
            'observacoes': r['observacoes'] or ''
        })
    
    return render_template('registros.html',
                           registros_por_func=registros_por_func,
                           data_inicio=data_inicio_str,
                           data_fim=data_fim_str)

@app.route('/admin/registro/editar/<int:record_id>', methods=['GET', 'POST'])
@admin_required
def editar_registro(record_id):
    """
    Edita registro existente.
    """
    record = query_db(
        "SELECT r.*, u.nome FROM records r JOIN users u ON r.user_id = u.id WHERE r.id = %s",
        (record_id,),
        one=True
    )
    
    if not record:
        flash('Registro não encontrado.')
        return redirect(url_for('listar_registros'))
    
    if request.method == 'POST':
        data = request.form['data']
        hora_entrada = request.form['hora_entrada'].strip() or None
        hora_saida = request.form['hora_saida'].strip() or None
        observacoes = request.form.get('observacoes', '').strip()
        
        # Validar e formatar horas
        def format_and_validate_time(t):
            if not t or t == '':
                return None
            try:
                if len(t) == 5 and ':' in t:
                    dt = datetime.strptime(t, '%H:%M')
                    return dt.strftime('%H:%M:%S')
                elif len(t) == 8 and t.count(':') == 2:
                    dt = datetime.strptime(t, '%H:%M:%S')
                    return dt.strftime('%H:%M:%S')
                else:
                    return None
            except:
                return None
        
        hora_entrada_formatted = format_and_validate_time(hora_entrada)
        hora_saida_formatted = format_and_validate_time(hora_saida)
        
        if hora_entrada and not hora_entrada_formatted:
            flash('Formato de entrada inválido. Use HH:MM ou HH:MM:SS (ex: 08:00)', 'error')
            return redirect(url_for('editar_registro', record_id=record_id))
        
        if hora_saida and not hora_saida_formatted:
            flash('Formato de saída inválido. Use HH:MM ou HH:MM:SS (ex: 18:00)', 'error')
            return redirect(url_for('editar_registro', record_id=record_id))
        
        # Validar que a data não é futura
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        if data_obj > hoje_sp():  # ✅ CORREÇÃO: usa hoje_sp()
            flash('Não é possível criar registro para data futura.', 'error')
            return redirect(url_for('editar_registro', record_id=record_id))
        
        try:
            execute_db(
                "UPDATE records SET data = %s, hora_entrada = %s, hora_saida = %s, observacoes = %s WHERE id = %s",
                (data, hora_entrada_formatted, hora_saida_formatted, observacoes, record_id)
            )
            flash('✅ Registro atualizado com sucesso!', 'success')
            return redirect(url_for('listar_registros'))
        except Exception as e:
            flash(f'❌ Erro ao atualizar registro: {str(e)}', 'error')
            return redirect(url_for('editar_registro', record_id=record_id))
    
    return render_template('registro_form.html', record=record)

@app.route('/admin/registro/excluir/<int:record_id>', methods=['POST'])
@admin_required
def excluir_registro(record_id):
    """
    Exclui registro.
    """
    execute_db("DELETE FROM records WHERE id = %s", (record_id,))
    flash('Registro excluído.')
    return redirect(url_for('listar_registros'))

@app.route('/admin/registro/novo', methods=['GET', 'POST'])
@admin_required
def novo_registro():
    """
    Cria novo registro manualmente.
    """
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        data = request.form['data']
        hora_entrada = request.form['hora_entrada'].strip() or None
        hora_saida = request.form['hora_saida'].strip() or None
        observacoes = request.form.get('observacoes', '').strip()
        
        # Validar e formatar horas
        def format_and_validate_time(t):
            if not t or t == '':
                return None
            try:
                if len(t) == 5 and ':' in t:
                    dt = datetime.strptime(t, '%H:%M')
                    return dt.strftime('%H:%M:%S')
                elif len(t) == 8 and t.count(':') == 2:
                    dt = datetime.strptime(t, '%H:%M:%S')
                    return dt.strftime('%H:%M:%S')
                else:
                    return None
            except:
                return None
        
        hora_entrada_formatted = format_and_validate_time(hora_entrada)
        hora_saida_formatted = format_and_validate_time(hora_saida)
        
        if not hora_entrada_formatted and not hora_saida_formatted:
            flash('Informe pelo menos entrada ou saída. Use formato HH:MM ou HH:MM:SS', 'error')
            return redirect(url_for('novo_registro'))
        
        if hora_entrada and not hora_entrada_formatted:
            flash('Formato de entrada inválido. Use HH:MM ou HH:MM:SS (ex: 08:00 ou 08:00:00)', 'error')
            return redirect(url_for('novo_registro'))
        
        if hora_saida and not hora_saida_formatted:
            flash('Formato de saída inválido. Use HH:MM ou HH:MM:SS (ex: 18:00 ou 18:00:00)', 'error')
            return redirect(url_for('novo_registro'))
        
        # Validar que a data não é futura
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        if data_obj > hoje_sp():  # ✅ CORREÇÃO: usa hoje_sp()
            flash('Não é possível criar registro para data futura.', 'error')
            return redirect(url_for('novo_registro'))
        
        try:
            execute_db(
                "INSERT INTO records (user_id, data, hora_entrada, hora_saida, observacoes) VALUES (%s, %s, %s, %s, %s)",
                (user_id, data, hora_entrada_formatted, hora_saida_formatted, observacoes)
            )
            flash('✅ Registro criado com sucesso!', 'success')
            return redirect(url_for('listar_registros'))
        except Exception as e:
            flash(f'❌ Erro ao criar registro: {str(e)}', 'error')
            return redirect(url_for('novo_registro'))
    
    return render_template('registro_form.html', users=users, novo=True)

# =============================================================================
# ROTA DE RELATÓRIO
# =============================================================================

@app.route('/admin/relatorio', methods=['GET', 'POST'])
@login_required
def relatorio():
    """
    Gera relatório de horas e valores para pagamento.
    """
    if session.get('tipo') != 'admin':
        flash('Acesso negado.')
        return redirect(url_for('login'))
    
    users = query_db("SELECT * FROM users WHERE tipo='funcionaria' ORDER BY nome")
    
    rel_data = None
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        
        dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        dt_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        delta = dt_fim - dt_inicio
        datas = [dt_inicio + timedelta(days=i) for i in range(delta.days + 1)]
        
        usuarios_rel = []
        
        for u in users:
            if user_id != 'todos' and str(u['id']) != user_id:
                continue
            
            linhas = []
            total_horas = timedelta()
            total_valor = 0
            
            for d in datas:
                registro = query_db(
                    "SELECT * FROM records WHERE user_id=%s AND data=%s",
                    (u['id'], d),
                    one=True
                )
                
                horas_trabalhadas = None
                valor = 0
                horas_str = '-'  # ✅ Valor padrão
                
                if registro and registro['hora_entrada'] and registro['hora_saida']:
                    h_entrada = registro['hora_entrada']
                    h_saida = registro['hora_saida']
                    
                    # MySQL retorna timedelta direto
                    horas_trabalhadas = h_saida - h_entrada
                    horas_dec = horas_trabalhadas.total_seconds() / 3600
                    
                    # ✅ USAR A FUNÇÃO HELPER para calcular valor/hora
                    valor_hora = calcular_valor_hora(d, u['nome'])
                    valor = round(horas_dec * valor_hora, 2)
                    
                    total_horas += horas_trabalhadas
                    total_valor += valor
                    
                    # ✅ CORREÇÃO: Formatar horas_trabalhadas como "Xh YYm"
                    total_seg = int(horas_trabalhadas.total_seconds())
                    h = total_seg // 3600
                    m = (total_seg % 3600) // 60
                    horas_str = f"{h}h{m:02d}m"
                
                linhas.append({
                    'data': d.strftime('%d/%m/%Y'),
                    'entrada': format_hora_banco(registro['hora_entrada']) if registro else '-',
                    'saida': format_hora_banco(registro['hora_saida']) if registro else '-',
                    'horas': horas_str,  # ✅ Agora usa o formato correto
                    'valor': f"{valor:.2f}"
                })
            
            # ✅ CORREÇÃO: Formatar total_horas como "XXhYYm" ao invés de "X days, H:M:S"
            if total_horas:
                total_segundos = int(total_horas.total_seconds())
                horas_totais = total_segundos // 3600
                minutos_totais = (total_segundos % 3600) // 60
                total_horas_str = f"{horas_totais}h{minutos_totais:02d}m"
            else:
                total_horas_str = "0h00m"
            
            usuarios_rel.append({
                'nome': u['nome'],
                'linhas': linhas,
                'total_horas': total_horas_str,
                'total_valor': f"{total_valor:.2f}"
            })
        
        rel_data = {
            'inicio': dt_inicio.strftime('%d/%m/%Y'),
            'fim': dt_fim.strftime('%d/%m/%Y'),
            'usuarios': usuarios_rel
        }
    
    return render_template('relatorio.html', users=users, rel_data=rel_data)

def format_hora_banco(h):
    """
    Formata hora do banco (pode vir como timedelta).
    """
    if h is None:
        return '-'
    if isinstance(h, timedelta):
        total_seg = int(h.total_seconds())
        horas = total_seg // 3600
        minutos = (total_seg % 3600) // 60
        return f"{horas:02d}:{minutos:02d}"
    if isinstance(h, (datetime, time)):
        return h.strftime('%H:%M')
    try:
        dt = datetime.strptime(str(h), '%H:%M:%S')
        return dt.strftime('%H:%M')
    except:
        return str(h)

print("✅ Parte 5.3 carregada: Registros e Relatórios")

# =============================================================================
# ROTAS DE SOLICITAÇÕES DE CORREÇÃO (COM PROTEÇÕES)
# =============================================================================

@app.route('/funcionaria/solicitar-correcao', methods=['GET', 'POST'])
@login_required
def solicitar_correcao():
    """
    Formulário para funcionária solicitar correção de ponto esquecido.
    O admin aprovará/rejeitará posteriormente.
    
    ✅ NOVO: Previne múltiplas solicitações pendentes para mesma data
    """
    if session.get('tipo') != 'funcionaria':
        flash('Acesso negado.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data_registro = request.form.get('data_registro')
        tipo = request.form.get('tipo')
        horario_entrada = request.form.get('horario_entrada') or None
        horario_saida = request.form.get('horario_saida') or None
        justificativa = request.form.get('justificativa', '').strip()
        
        if not data_registro or not tipo or not justificativa:
            flash('Preencha todos os campos obrigatórios.')
            return redirect(url_for('solicitar_correcao'))
        
        # Validar que a data não é futura
        data_obj = datetime.strptime(data_registro, '%Y-%m-%d').date()
        if data_obj > hoje_sp():
            flash('Não é possível solicitar correção para datas futuras.')
            return redirect(url_for('solicitar_correcao'))
        
        # ✅ NOVO: Verificar se já tem solicitação pendente para mesma data
        pendente = query_db("""
            SELECT * FROM solicitacoes_correcao
            WHERE funcionaria_id = %s 
            AND data_registro = %s 
            AND status = 'pendente'
        """, (session['user_id'], data_registro), one=True)
        
        if pendente:
            flash('❌ Você já tem uma solicitação pendente para esta data! Aguarde a aprovação do administrador.', 'warning')
            return redirect(url_for('funcionaria'))
        
        # Inserir solicitação
        execute_db("""
            INSERT INTO solicitacoes_correcao
            (funcionaria_id, data_registro, tipo, horario_entrada, horario_saida, justificativa)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (session['user_id'], data_registro, tipo, horario_entrada, horario_saida, justificativa))
        
        flash('Solicitação enviada com sucesso! Aguarde aprovação do administrador.')
        return redirect(url_for('funcionaria'))
    
    return render_template('solicitar_correcao.html')

# ✅ Rota Excluir solicitação pendente
@app.route('/funcionaria/solicitacao/excluir/<int:solicitacao_id>', methods=['POST'])
@login_required
def excluir_solicitacao(solicitacao_id):
    """
    Permite que funcionária exclua sua própria solicitação PENDENTE.
    
    Regras:
    - Só pode excluir próprias solicitações
    - Só pode excluir se status = 'pendente'
    - Não pode excluir aprovadas/rejeitadas
    """
    if session.get('tipo') != 'funcionaria':
        flash('Acesso negado.')
        return redirect(url_for('login'))
    
    # Buscar solicitação
    solicitacao = query_db(
        "SELECT * FROM solicitacoes_correcao WHERE id = %s",
        (solicitacao_id,),
        one=True
    )
    
    # Validações
    if not solicitacao:
        flash('❌ Solicitação não encontrada.', 'error')
        return redirect(url_for('funcionaria'))
    
    # Verificar se é da própria funcionária
    if solicitacao['funcionaria_id'] != session['user_id']:
        flash('❌ Você não pode excluir solicitações de outras pessoas!', 'error')
        return redirect(url_for('funcionaria'))
    
    # Verificar se está pendente
    if solicitacao['status'] != 'pendente':
        flash('❌ Não é possível excluir solicitações já processadas.', 'warning')
        return redirect(url_for('funcionaria'))
    
    # Excluir solicitação
    execute_db(
        "DELETE FROM solicitacoes_correcao WHERE id = %s",
        (solicitacao_id,)
    )
    
    flash('✅ Solicitação excluída com sucesso!', 'success')
    return redirect(url_for('funcionaria'))

@app.route('/admin/solicitacoes')
@admin_required
def listar_solicitacoes():
    """
    Página do admin para visualizar e gerenciar solicitações de correção.
    Mostra solicitações pendentes, aprovadas e rejeitadas.
    
    ✅ NOVO: Detecta e avisa quando já existe registro para a data
    """
    solicitacoes_raw = query_db("""
        SELECT s.*, u.nome as funcionaria_nome
        FROM solicitacoes_correcao s
        JOIN users u ON s.funcionaria_id = u.id
        ORDER BY
            CASE s.status
                WHEN 'pendente' THEN 1
                WHEN 'aprovado' THEN 2
                WHEN 'rejeitado' THEN 3
            END,
            s.data_solicitacao DESC
    """)
    
    solicitacoes_formatadas = []
    for sol in solicitacoes_raw:
        # Formatar datas
        data_solic = sol['data_solicitacao']
        if isinstance(data_solic, str):
            data_solic = datetime.strptime(data_solic, '%Y-%m-%d %H:%M:%S')
        
        data_reg = sol['data_registro']
        if isinstance(data_reg, str):
            data_reg = datetime.strptime(data_reg, '%Y-%m-%d').date()
        
        data_proc = sol['data_processamento']
        if data_proc and isinstance(data_proc, str):
            data_proc = datetime.strptime(data_proc, '%Y-%m-%d %H:%M:%S')
        
        # Traduzir tipo
        tipo_label = {
            'entrada': 'Falta entrada',
            'saida': 'Falta saída',
            'ambos': 'Faltam entrada e saída'
        }.get(sol['tipo'], sol['tipo'])
        
        # Status em português
        status_label = {
            'pendente': 'Pendente',
            'aprovado': 'Aprovado',
            'rejeitado': 'Rejeitado'
        }.get(sol['status'], sol['status'])
        
        # Formatar horários
        horario_entrada_fmt = format_hora(sol['horario_entrada']) if sol['horario_entrada'] else None
        horario_saida_fmt = format_hora(sol['horario_saida']) if sol['horario_saida'] else None
        
        # ✅ NOVO: Verificar se já existe registro para aquela data
        registro_existente = query_db("""
            SELECT hora_entrada, hora_saida
            FROM records
            WHERE user_id = %s AND data = %s
        """, (sol['funcionaria_id'], sol['data_registro']), one=True)
        
        tem_registro = bool(registro_existente)
        entrada_atual = format_hora(registro_existente['hora_entrada']) if registro_existente else None
        saida_atual = format_hora(registro_existente['hora_saida']) if registro_existente else None
        
        solicitacoes_formatadas.append({
            'id': sol['id'],
            'funcionaria_nome': sol['funcionaria_nome'],
            'data_solicitacao': data_solic.strftime('%d/%m/%Y às %H:%M'),
            'data_registro': data_reg.strftime('%d/%m/%Y'),
            'tipo': tipo_label,
            'status': sol['status'],
            'status_label': status_label,
            'horario_entrada': horario_entrada_fmt,
            'horario_saida': horario_saida_fmt,
            'justificativa': sol['justificativa'],
            'observacao_admin': sol['observacao_admin'],
            'data_processamento': data_proc.strftime('%d/%m/%Y às %H:%M') if data_proc else None,
            # ✅ NOVO: Dados do registro existente
            'tem_registro_existente': tem_registro,
            'entrada_atual': entrada_atual,
            'saida_atual': saida_atual
        })
    
    pendentes_count = sum(1 for s in solicitacoes_formatadas if s['status'] == 'pendente')
    
    return render_template('admin_solicitacoes.html',
                          solicitacoes=solicitacoes_formatadas,
                          pendentes_count=pendentes_count)

@app.route('/admin/solicitacoes/aprovar/<int:solicitacao_id>', methods=['POST'])
@admin_required
def aprovar_solicitacao(solicitacao_id):
    """
    Aprova uma solicitação de correção e atualiza/cria o registro de ponto.
    """
    solicitacao = query_db(
        "SELECT * FROM solicitacoes_correcao WHERE id = %s",
        (solicitacao_id,),
        one=True
    )
    
    if not solicitacao:
        flash('Solicitação não encontrada.')
        return redirect(url_for('listar_solicitacoes'))
    
    if solicitacao['status'] != 'pendente':
        flash('Esta solicitação já foi processada.')
        return redirect(url_for('listar_solicitacoes'))
    
    registro_existente = query_db("""
        SELECT * FROM records
        WHERE user_id = %s AND data = %s
    """, (solicitacao['funcionaria_id'], solicitacao['data_registro']), one=True)
    
    tipo = solicitacao['tipo']
    
    if registro_existente:
        # Atualizar registro existente
        if tipo == 'entrada':
            execute_db("UPDATE records SET hora_entrada = %s WHERE id = %s",
                      (solicitacao['horario_entrada'], registro_existente['id']))
        elif tipo == 'saida':
            execute_db("UPDATE records SET hora_saida = %s WHERE id = %s",
                      (solicitacao['horario_saida'], registro_existente['id']))
        elif tipo == 'ambos':
            execute_db("UPDATE records SET hora_entrada = %s, hora_saida = %s WHERE id = %s",
                      (solicitacao['horario_entrada'], solicitacao['horario_saida'],
                       registro_existente['id']))
    else:
        # Criar novo registro
        execute_db("""
            INSERT INTO records (user_id, data, hora_entrada, hora_saida)
            VALUES (%s, %s, %s, %s)
        """, (solicitacao['funcionaria_id'], solicitacao['data_registro'],
              solicitacao['horario_entrada'], solicitacao['horario_saida']))
    
    observacao = request.form.get('observacao', '').strip()
    execute_db("""
        UPDATE solicitacoes_correcao
        SET status = 'aprovado',
            observacao_admin = %s,
            data_processamento = NOW()
        WHERE id = %s
    """, (observacao if observacao else 'Aprovado', solicitacao_id))
    
    flash('Solicitação aprovada e registro atualizado com sucesso.')
    return redirect(url_for('listar_solicitacoes'))

@app.route('/admin/solicitacoes/rejeitar/<int:solicitacao_id>', methods=['POST'])
@admin_required
def rejeitar_solicitacao(solicitacao_id):
    """
    Rejeita uma solicitação de correção com observação do motivo.
    """
    solicitacao = query_db(
        "SELECT * FROM solicitacoes_correcao WHERE id = %s",
        (solicitacao_id,),
        one=True
    )
    
    if not solicitacao:
        flash('Solicitação não encontrada.')
        return redirect(url_for('listar_solicitacoes'))
    
    if solicitacao['status'] != 'pendente':
        flash('Esta solicitação já foi processada.')
        return redirect(url_for('listar_solicitacoes'))
    
    observacao = request.form.get('observacao', '').strip()
    if not observacao:
        flash('É necessário informar o motivo da rejeição.')
        return redirect(url_for('listar_solicitacoes'))
    
    execute_db("""
        UPDATE solicitacoes_correcao
        SET status = 'rejeitado',
            observacao_admin = %s,
            data_processamento = NOW()
        WHERE id = %s
    """, (observacao, solicitacao_id))
    
    flash('Solicitação rejeitada.')
    return redirect(url_for('listar_solicitacoes'))

@app.route('/admin/solicitacoes/aprovar-todas', methods=['POST'])
@admin_required
def aprovar_todas_solicitacoes():
    """
    Aprova todas as solicitações pendentes de uma vez.
    """
    pendentes = query_db("""
        SELECT * FROM solicitacoes_correcao
        WHERE status = 'pendente'
    """)
    
    if not pendentes:
        flash('Não há solicitações pendentes para aprovar.')
        return redirect(url_for('listar_solicitacoes'))
    
    aprovadas = 0
    erros = 0
    
    for solicitacao in pendentes:
        try:
            registro_existente = query_db("""
                SELECT * FROM records
                WHERE user_id = %s AND data = %s
            """, (solicitacao['funcionaria_id'], solicitacao['data_registro']), one=True)
            
            tipo = solicitacao['tipo']
            
            if registro_existente:
                if tipo == 'entrada':
                    execute_db("UPDATE records SET hora_entrada = %s WHERE id = %s",
                              (solicitacao['horario_entrada'], registro_existente['id']))
                elif tipo == 'saida':
                    execute_db("UPDATE records SET hora_saida = %s WHERE id = %s",
                              (solicitacao['horario_saida'], registro_existente['id']))
                elif tipo == 'ambos':
                    execute_db("UPDATE records SET hora_entrada = %s, hora_saida = %s WHERE id = %s",
                              (solicitacao['horario_entrada'], solicitacao['horario_saida'],
                               registro_existente['id']))
            else:
                execute_db("""
                    INSERT INTO records (user_id, data, hora_entrada, hora_saida)
                    VALUES (%s, %s, %s, %s)
                """, (solicitacao['funcionaria_id'], solicitacao['data_registro'],
                      solicitacao['horario_entrada'], solicitacao['horario_saida']))
            
            execute_db("""
                UPDATE solicitacoes_correcao
                SET status = 'aprovado',
                    observacao_admin = 'Aprovado em lote',
                    data_processamento = NOW()
                WHERE id = %s
            """, (solicitacao['id'],))
            
            aprovadas += 1
        
        except Exception as e:
            erros += 1
            continue
    
    if erros > 0:
        flash(f'{aprovadas} solicitação(ões) aprovada(s). {erros} erro(s) encontrado(s).')
    else:
        flash(f'✅ {aprovadas} solicitação(ões) aprovada(s) com sucesso!')
    
    return redirect(url_for('listar_solicitacoes'))

print("✅ Parte 5.4 carregada: Solicitações de Correção (COM PROTEÇÕES)")

# =============================================================================
# ✅ CORREÇÃO 12: DATAS ALTERADAS
# Funcionárias: Dia 1 e 2 (antes era 3 e 4)
# Admin pagamento: Dia 3 (antes era 5)
# =============================================================================

# =============================================================================
# FUNÇÕES DE AUTOMAÇÃO - LEMBRETES E ALERTAS
# =============================================================================

def lembrete_entrada():
    """
    Envia lembrete às 8h APENAS para quem trabalha hoje nesse horário.
    Usa timezone de São Paulo.
    """
    with app.app_context():
        funcionarias = query_db(
            "SELECT id, nome, telefone FROM users WHERE tipo = 'funcionaria' AND telefone IS NOT NULL"
        )
        
        hoje = hoje_sp()
        dias = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
        dia_semana = dias[hoje.weekday()]
        
        for func in funcionarias:
            horario = funcionaria_trabalha_hoje(func['nome'], dia_semana)
            
            if horario and horario['entrada'] == '08:00':
                mensagem = (
                    f"☀️ *Bom dia, {func['nome']}!*\n\n"
                    f"⏰ Hora de registrar sua *ENTRADA*\n\n"
                    f"🔗 Acesse: {URL_SITE}"
                )
                enviar_whatsapp(func['telefone'], mensagem)
                print(f"📤 Lembrete de entrada enviado para {func['nome']}")

def lembrete_saida():
    """
    Envia lembrete de saída baseado no horário.
    SÓ envia se bateu entrada hoje.
    """
    with app.app_context():
        hoje_str = hoje_sp().isoformat()
        funcionarias = query_db(
            "SELECT id, nome, telefone FROM users WHERE tipo = 'funcionaria' AND telefone IS NOT NULL"
        )
        
        hoje = hoje_sp()
        dias = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
        dia_semana = dias[hoje.weekday()]
        
        hora_atual = agora_sp().strftime('%H:%M')
        
        for func in funcionarias:
            horario = funcionaria_trabalha_hoje(func['nome'], dia_semana)
            
            if not horario:
                continue
            
            record = query_db(
                "SELECT * FROM records WHERE user_id = %s AND data = %s",
                (func['id'], hoje_str),
                one=True
            )
            
            if record and record['hora_entrada'] and not record['hora_saida']:
                hora_saida_esperada = horario['saida'][:5]
                if hora_atual == hora_saida_esperada:
                    mensagem = (
                        f"🌙 *Oi, {func['nome']}!*\n\n"
                        f"⏰ Lembra de registrar sua *SAÍDA*\n\n"
                        f"🔗 Acesse: {URL_SITE}"
                    )
                    enviar_whatsapp(func['telefone'], mensagem)
                    print(f"📤 Lembrete de saída enviado para {func['nome']}")

# ✅ CORREÇÃO 12: Dia 1 e 2 (antes era 3 e 4)
def alerta_pendencias_dia_01():
    """
    Dia 01 de cada mês - Alerta sobre pendências do mês anterior.
    Prazo: até dia 02.
    """
    with app.app_context():
        hoje = hoje_sp()
        mes_anterior_date = hoje - relativedelta(months=1)
        primeiro_dia = date(mes_anterior_date.year, mes_anterior_date.month, 1)
        ultimo_dia = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        nome_mes = meses[mes_anterior_date.month - 1]
        
        admin = query_db("SELECT telefone FROM users WHERE tipo = 'admin' LIMIT 1", one=True)
        funcionarias = query_db(
            "SELECT id, nome, telefone FROM users WHERE tipo = 'funcionaria' AND telefone IS NOT NULL"
        )
        
        resumo_admin = f"⚠️ *ALERTA DE PENDÊNCIAS - DIA 01*\n\n"
        resumo_admin += f"Mês: {nome_mes}/{mes_anterior_date.year}\n"
        resumo_admin += f"Prazo: ATÉ AMANHÃ (02)\n\n"
        
        tem_pendencias_geral = False
        
        for func in funcionarias:
            registros = query_db(
                "SELECT data, hora_entrada, hora_saida FROM records "
                "WHERE user_id = %s AND data >= %s AND data <= %s ORDER BY data",
                (func['id'], primeiro_dia.isoformat(), ultimo_dia.isoformat())
            )
            
            pendencias = []
            delta = ultimo_dia - primeiro_dia
            
            for i in range(delta.days + 1):
                dia = primeiro_dia + timedelta(days=i)
                dia_str = dia.isoformat()
                reg = next((r for r in registros if r['data'] == dia_str), None)
                
                if not reg or not reg['hora_entrada']:
                    pendencias.append(f"❌ {dia.strftime('%d/%m')}: Não registrado")
                elif not reg['hora_saida']:
                    pendencias.append(f"⚠️ {dia.strftime('%d/%m')}: Falta saída")
            
            if pendencias:
                tem_pendencias_geral = True
                mensagem = f"⚠️ *ATENÇÃO {func['nome']}!*\n\n"
                mensagem += f"📅 *{nome_mes}/{mes_anterior_date.year}*\n\n"
                mensagem += f"Você tem *{len(pendencias)} pendência(s)*:\n\n"
                
                for pend in pendencias[:10]:
                    mensagem += f"{pend}\n"
                
                if len(pendencias) > 10:
                    mensagem += f"\n... e mais {len(pendencias) - 10}\n"
                
                mensagem += f"\n🚨 *PRAZO: AMANHÃ (DIA 02)*\n\n"
                mensagem += f"Acesse: {URL_SITE}\n"
                mensagem += f"Clique em 'Solicitar Correção'"
                
                enviar_whatsapp(func['telefone'], mensagem)
                resumo_admin += f"*{func['nome']}:* {len(pendencias)} pendência(s)\n"
        
        if tem_pendencias_geral and admin and admin['telefone']:
            enviar_whatsapp(admin['telefone'], resumo_admin)

def alerta_pendencias_dia_02():
    """
    Dia 02 - Alerta FINAL (código similar ao dia 01, mas mais urgente).
    ÚLTIMO DIA para regularizar pendências antes do fechamento!
    """
    with app.app_context():
        hoje = hoje_sp()
        mes_anterior_date = hoje - relativedelta(months=1)
        primeiro_dia = date(mes_anterior_date.year, mes_anterior_date.month, 1)
        ultimo_dia = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        nome_mes = meses[mes_anterior_date.month - 1]
        
        admin = query_db("SELECT telefone FROM users WHERE tipo = 'admin' LIMIT 1", one=True)
        funcionarias = query_db(
            "SELECT id, nome, telefone FROM users WHERE tipo = 'funcionaria' AND telefone IS NOT NULL"
        )
        
        resumo_admin = f"🚨 *ALERTA URGENTE - ÚLTIMO DIA!*\n\n"
        resumo_admin += f"Mês: {nome_mes}/{mes_anterior_date.year}\n"
        resumo_admin += f"⚠️ PRAZO FINAL: HOJE (DIA 02)\n\n"
        
        tem_pendencias_geral = False
        
        for func in funcionarias:
            registros = query_db(
                "SELECT data, hora_entrada, hora_saida FROM records "
                "WHERE user_id = %s AND data >= %s AND data <= %s ORDER BY data",
                (func['id'], primeiro_dia.isoformat(), ultimo_dia.isoformat())
            )
            
            pendencias = []
            delta = ultimo_dia - primeiro_dia
            
            for i in range(delta.days + 1):
                dia = primeiro_dia + timedelta(days=i)
                dia_str = dia.isoformat()
                reg = next((r for r in registros if r['data'] == dia_str), None)
                
                if not reg or not reg['hora_entrada']:
                    pendencias.append(f"❌ {dia.strftime('%d/%m')}: Não registrado")
                elif not reg['hora_saida']:
                    pendencias.append(f"⚠️ {dia.strftime('%d/%m')}: Falta saída")
            
            if pendencias:
                tem_pendencias_geral = True
                mensagem = f"🚨 *URGENTE {func['nome']}!*\n\n"
                mensagem += f"📅 *{nome_mes}/{mes_anterior_date.year}*\n\n"
                mensagem += f"⚠️ *ÚLTIMO DIA* para regularizar!\n"
                mensagem += f"Você ainda tem *{len(pendencias)} pendência(s)*:\n\n"
                
                for pend in pendencias[:10]:
                    mensagem += f"{pend}\n"
                
                if len(pendencias) > 10:
                    mensagem += f"\n... e mais {len(pendencias) - 10}\n"
                
                mensagem += f"\n🔴 *PRAZO: HOJE ATÉ 23h59!*\n\n"
                mensagem += f"Acesse AGORA: {URL_SITE}\n"
                mensagem += f"→ Clique em 'Solicitar Correção'"
                
                enviar_whatsapp(func['telefone'], mensagem)
                resumo_admin += f"*{func['nome']}:* {len(pendencias)} pendência(s)\n"
        
        if tem_pendencias_geral and admin and admin['telefone']:
            enviar_whatsapp(admin['telefone'], resumo_admin)

# ✅ CORREÇÃO 12: Dia 3 (antes era 5)
def relatorio_mensal_pagamento():
    """
    Dia 03 de cada mês - Envia cálculo de pagamento para admin.
    """
    with app.app_context():
        admin = query_db("SELECT telefone FROM users WHERE tipo = 'admin' LIMIT 1", one=True)
        if not admin or not admin['telefone']:
            return
        
        hoje = hoje_sp()
        mes_anterior_date = hoje - relativedelta(months=1)
        primeiro_dia = date(mes_anterior_date.year, mes_anterior_date.month, 1)
        ultimo_dia = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        
        funcionarias = query_db("SELECT id, nome FROM users WHERE tipo = 'funcionaria'")
        
        mensagem = f"💰 *RELATÓRIO DE PAGAMENTO*\n\n"
        mensagem += f"Período: {primeiro_dia.strftime('%d/%m/%Y')} a {ultimo_dia.strftime('%d/%m/%Y')}\n\n"
        
        for func in funcionarias:
            registros = query_db(
                "SELECT data, hora_entrada, hora_saida FROM records "
                "WHERE user_id = %s AND data >= %s AND data <= %s "
                "AND hora_entrada IS NOT NULL AND hora_saida IS NOT NULL",
                (func['id'], primeiro_dia.isoformat(), ultimo_dia.isoformat())
            )
            
            total_horas = timedelta()
            total_valor = 0
            dias_normais = 0
            dias_domingo = 0
            
            for reg in registros:
                data_reg = datetime.strptime(reg['data'], '%Y-%m-%d').date() if isinstance(reg['data'], str) else reg['data']
                entrada = datetime.strptime(reg['hora_entrada'], '%H:%M:%S').time() if isinstance(reg['hora_entrada'], str) else reg['hora_entrada']
                saida = datetime.strptime(reg['hora_saida'], '%H:%M:%S').time() if isinstance(reg['hora_saida'], str) else reg['hora_saida']
                
                horas_dia, valor_dia = calcular_valor_dia(data_reg, entrada, saida, func['nome'])
                
                if horas_dia:
                    total_horas += horas_dia
                    total_valor += valor_dia
                    
                    if data_reg.weekday() == 6:
                        dias_domingo += 1
                    else:
                        dias_normais += 1
            
            total_segundos = total_horas.total_seconds()
            horas = int(total_segundos // 3600)
            minutos = int((total_segundos % 3600) // 60)
            
            mensagem += f"*{func['nome']}:*\n"
            mensagem += f"⏱️ Total: {horas}h{minutos:02d}m\n"
            if dias_normais > 0:
                mensagem += f"📅 Dias normais: {dias_normais}\n"
            if dias_domingo > 0:
                mensagem += f"☀️ Domingos: {dias_domingo}\n"
            mensagem += f"💵 *Valor: R$ {total_valor:.2f}*\n\n"
        
        mensagem += f"📊 Detalhes: {URL_SITE}"
        enviar_whatsapp(admin['telefone'], mensagem)
        print("💰 Relatório mensal enviado!")

# =============================================================================
# ✅ BACKUP AUTOMÁTICO VIA TELEGRAM (GRATUITO!)
# =============================================================================
def converter_hora_banco_para_time(hora):
    """
    Converte hora do banco (timedelta, time ou string) para time object.
    Helper para usar em funções de relatório e backup.
    
    Args:
        hora: Pode ser timedelta, time, string ou None
    
    Returns:
        time: Objeto time ou None
    """
    if hora is None:
        return None
    
    # Se já é time, retorna direto
    if isinstance(hora, time):
        return hora
    
    # Se é timedelta (retorno do MySQL para TIME)
    if isinstance(hora, timedelta):
        total_seg = int(hora.total_seconds())
        horas = total_seg // 3600
        minutos = (total_seg % 3600) // 60
        segundos = total_seg % 60
        return time(hour=horas, minute=minutos, second=segundos)
    
    # Se é string, converter
    if isinstance(hora, str):
        try:
            dt = datetime.strptime(hora, '%H:%M:%S')
            return dt.time()
        except:
            try:
                dt = datetime.strptime(hora, '%H:%M')
                return dt.time()
            except:
                return None
    
    return None

def backup_mensal_telegram():
    """
    Envia backup CSV via Telegram Bot.
    Executado dia 1º de cada mês (após alertas de pendências).
    
    Formato CSV: data,funcionaria,entrada,saida,horas,valor
    """
    if not BACKUP_ATIVADO:
        print("⚠️ Backup Telegram desativado (configure TELEGRAM_BOT_TOKEN)")
        return
    
    with app.app_context():
        hoje = hoje_sp()
        mes_anterior_date = hoje - relativedelta(months=1)
        primeiro_dia = date(mes_anterior_date.year, mes_anterior_date.month, 1)
        ultimo_dia = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        
        # Buscar todos os registros do mês anterior
        registros = query_db(
            "SELECT r.data, r.hora_entrada, r.hora_saida, u.nome "
            "FROM records r JOIN users u ON r.user_id = u.id "
            "WHERE r.data >= %s AND r.data <= %s "
            "ORDER BY u.nome, r.data",
            (primeiro_dia.isoformat(), ultimo_dia.isoformat())
        )
        
        # Gerar CSV
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Data', 'Funcionária', 'Entrada', 'Saída', 'Horas', 'Valor (R$)'])
        
        for reg in registros:
            data_obj = datetime.strptime(reg['data'], '%Y-%m-%d').date() if isinstance(reg['data'], str) else reg['data']
            
            if reg['hora_entrada'] and reg['hora_saida']:
                # ✅ USAR FUNÇÃO HELPER para converter
                entrada = converter_hora_banco_para_time(reg['hora_entrada'])
                saida = converter_hora_banco_para_time(reg['hora_saida'])
                
                if entrada and saida:
                    horas_dia, valor_dia = calcular_valor_dia(data_obj, entrada, saida, reg['nome'])
                    horas_str = format_hora(horas_dia)
                else:
                    horas_str = '-'
                    valor_dia = 0
            else:
                horas_str = '-'
                valor_dia = 0
            
            writer.writerow([
                data_obj.strftime('%d/%m/%Y'),
                reg['nome'],
                format_hora(reg['hora_entrada']),
                format_hora(reg['hora_saida']),
                horas_str,
                f"{valor_dia:.2f}"
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Salvar temporariamente
        filename = f"backup_{mes_anterior_date.strftime('%Y_%m')}.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        # Enviar via Telegram
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            with open(filename, 'rb') as f:
                response = requests.post(
                    url,
                    data={'chat_id': TELEGRAM_CHAT_ID},
                    files={'document': f}
                )
            
            if response.status_code == 200:
                print(f"✅ Backup enviado via Telegram: {filename}")
            else:
                print(f"❌ Erro ao enviar backup: {response.text}")
        
        except Exception as e:
            print(f"❌ Erro ao enviar backup: {e}")
        
        finally:
            # Remover arquivo temporário
            import os
            if os.path.exists(filename):
                os.remove(filename)

def relatorio_falhas_whatsapp():
    """
    Envia relatório diário de falhas para admin (23h50).
    """
    global falhas_whatsapp_hoje
    
    if not falhas_whatsapp_hoje:
        return
    
    with app.app_context():
        admin = query_db("SELECT telefone FROM users WHERE tipo = 'admin' LIMIT 1", one=True)
        
        if admin and admin['telefone']:
            mensagem = f"⚠️ *RELATÓRIO DE FALHAS WHATSAPP*\n\n"
            mensagem += f"Total hoje: {len(falhas_whatsapp_hoje)} falhas\n\n"
            
            for falha in falhas_whatsapp_hoje[:5]:
                mensagem += f"• {falha['telefone']}: {falha['erro'][:40]}...\n"
            
            if len(falhas_whatsapp_hoje) > 5:
                mensagem += f"\n... e mais {len(falhas_whatsapp_hoje) - 5} falhas\n"
            
            mensagem += f"\n📁 Veja logs/whatsapp_falhas.log para detalhes"
            enviar_whatsapp(admin['telefone'], mensagem)
    
    falhas_whatsapp_hoje = []

@app.errorhandler(500)
def erro_interno(e):
    """Envia erro crítico via Telegram"""
    erro_msg = f"🚨 ERRO CRÍTICO NO SISTEMA\n\n{str(e)}\n\n{traceback.format_exc()}"
    
    # Envia para admin via Telegram (se configurado)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={'chat_id': TELEGRAM_CHAT_ID, 'text': erro_msg[:4000]}
            )
        except:
            pass
    
    return "Erro interno", 500

# =============================================================================
# ROTAS PARA CRON EXTERNO (Cron-job.org)
# =============================================================================

@app.route('/cron/lembrete-entrada')
def cron_lembrete_entrada():
    """Chamado por cron externo às 8h"""
    try:
        lembrete_entrada()
        return "✅ Lembrete entrada enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/lembrete-saida')
def cron_lembrete_saida():
    """Chamado por cron externo nos horários de saída"""
    try:
        lembrete_saida()
        return "✅ Lembrete saída enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/alerta-dia-01')
def cron_alerta_dia_01():
    """Chamado dia 1 do mês às 9h"""
    try:
        alerta_pendencias_dia_01()
        return "✅ Alerta dia 01 enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/alerta-dia-02')
def cron_alerta_dia_02():
    """Chamado dia 2 do mês às 9h e 18h"""
    try:
        alerta_pendencias_dia_02()
        return "✅ Alerta dia 02 enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/relatorio-mensal')
def cron_relatorio_mensal():
    """Chamado dia 3 do mês às 9h"""
    try:
        relatorio_mensal_pagamento()
        return "✅ Relatório mensal enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/backup-telegram')
def cron_backup_telegram():
    """Chamado dia 1 do mês às 19h"""
    try:
        backup_mensal_telegram()
        return "✅ Backup enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/cron/relatorio-falhas')
def cron_relatorio_falhas():
    """Chamado diariamente às 23h50"""
    try:
        relatorio_falhas_whatsapp()
        return "✅ Relatório falhas enviado", 200
    except Exception as e:
        return f"Erro: {str(e)}", 500

print("✅ Rotas CRON configuradas!")

# =============================================================================
# INICIALIZAÇÃO DO FLASK
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    # ✅ Debug mode do .env
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*70)
    print("🎉 SISTEMA DE PONTO INICIADO COM SUCESSO!")
    print("="*70)
    print(f"📅 Data/Hora: {agora_sp().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🌍 Timezone: America/Sao_Paulo")
    print(f"💾 Retenção de dados: 13 meses (395 dias)")
    print(f"📱 WhatsApp: {'✅ Configurado' if any(CALLMEBOT_KEYS.values()) else '❌ Não configurado'}")
    print(f"🤖 Telegram Backup: {'✅ Ativado' if BACKUP_ATIVADO else '⚠️ Desativado'}")
    print(f"🔐 Debug Mode: {'⚠️ Ativado' if debug_mode else '✅ Desativado'}")
    print("="*70 + "\n")
    
    app.run(debug=debug_mode)