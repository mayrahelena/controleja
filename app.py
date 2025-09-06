import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, date, timedelta, time
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import bcrypt

app = Flask(__name__)
app.secret_key = 'troque_esta_chave_para_uma_secreta_e_segura'

# Configurações MySQL
MYSQL_HOST = 'localhost'  # ou IP/hostname do servidor MySQL
MYSQL_USER = 'root'
MYSQL_PASSWORD = '021998@Amor'
MYSQL_DB = 'ponto_db'

# --- Banco de dados ---
def get_db():
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
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(query, args)
        rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(query, args)
        db.commit()
        return cur.lastrowid

# --- Inicialização do banco ---
def init_db():
    # Conectar sem banco para criar banco se não existir
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        cursorclass=DictCursor,
        autocommit=True,
        charset='utf8mb4'
    )
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.close()

    # Agora conecta ao banco criado
    db = get_db()
    with db.cursor() as cur:
        # Criar tabelas se não existirem
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        for statement in schema_sql.split(';'):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)
        db.commit()

        # Verificar se já existe usuário admin
        cur.execute("SELECT * FROM users WHERE tipo = 'admin' LIMIT 1")
        admin = cur.fetchone()
        if not admin:
            senha_admin = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
            cur.execute(
                "INSERT INTO users (nome, username, senha, tipo) VALUES (%s, %s, %s, 'admin')",
                ('Administrador', 'admin', senha_admin)
            )
            db.commit()

# --- Autenticação ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('tipo') != 'admin':
            flash('Acesso negado.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Limpar registros com mais de 90 dias ---
def cleanup_old_records():
    cutoff = date.today() - timedelta(days=90)
    execute_db("DELETE FROM records WHERE data < %s", (cutoff.isoformat(),))

# --- Rotas ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        senha = request.form['senha'].encode()
        user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
        if user and bcrypt.checkpw(senha, user['senha'].encode() if isinstance(user['senha'], str) else user['senha']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nome'] = user['nome']
            session['tipo'] = user['tipo']
            return redirect(url_for('funcionaria') if user['tipo'] == 'funcionaria' else url_for('admin'))
        else:
            flash('Usuário ou senha inválidos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Funcionária ---

@app.route('/funcionaria', methods=['GET', 'POST'])
@login_required
def funcionaria():
    if session.get('tipo') != 'funcionaria':
        flash('Acesso negado.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    hoje = date.today().isoformat()

    cleanup_old_records()

    record = query_db("SELECT * FROM records WHERE user_id = %s AND data = %s", (user_id, hoje), one=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        now_time = datetime.now().strftime('%H:%M:%S')

        if acao == 'entrada':
            if record and record['hora_entrada'] and not record['hora_saida']:
                flash('Você já registrou entrada e ainda não registrou saída. Informe a saída antes de nova entrada.')
            else:
                if record:
                    execute_db("UPDATE records SET hora_entrada = %s, hora_saida = NULL WHERE id = %s", (now_time, record['id']))
                else:
                    execute_db("INSERT INTO records (user_id, data, hora_entrada) VALUES (%s, %s, %s)", (user_id, hoje, now_time))
                flash(f'Entrada registrada às {now_time}')
                return redirect(url_for('funcionaria'))

        elif acao == 'saida':
            if not record or not record['hora_entrada']:
                flash('Não há registro de entrada para hoje. Informe manualmente a entrada antes de registrar saída.')
            elif record['hora_saida']:
                flash('Você já registrou saída para hoje.')
            else:
                execute_db("UPDATE records SET hora_saida = %s WHERE id = %s", (now_time, record['id']))
                flash(f'Saída registrada às {now_time}')
                return redirect(url_for('funcionaria'))

    entrada = record['hora_entrada'] if record else None
    saida = record['hora_saida'] if record else None

    # Formatar hora para exibição ou "-"
    def format_hora(h):
        if h is None:
            return '-'
        if isinstance(h, (datetime, time)):
            return h.strftime('%H:%M')
        # Caso venha string (ex: 'HH:MM:SS'), formatar para HH:MM
        try:
            dt = datetime.strptime(h, '%H:%M:%S')
            return dt.strftime('%H:%M')
        except:
            return h

    entrada_fmt = format_hora(entrada)
    saida_fmt = format_hora(saida)

    return render_template('func.html', nome=session['nome'], entrada=entrada_fmt, saida=saida_fmt)

# --- Administrador ---

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html', nome=session['nome'])

# --- Alterar dados Admin - Administrador ---
@app.route('/admin/perfil', methods=['GET', 'POST'])
@admin_required
def editar_perfil_admin():
    user_id = session['user_id']
    user = query_db("SELECT * FROM users WHERE id = %s AND tipo = 'admin'", (user_id,), one=True)
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
        exists = query_db("SELECT * FROM users WHERE username = %s AND id != %s", (username, user_id), one=True)
        if exists:
            flash('Nome de usuário já existe.')
            return redirect(url_for('editar_perfil_admin'))

        if senha:
            if senha != senha_confirm:
                flash('Senhas não conferem.')
                return redirect(url_for('editar_perfil_admin'))
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            execute_db("UPDATE users SET nome = %s, username = %s, senha = %s WHERE id = %s",
                       (nome, username, senha_hash, user_id))
        else:
            execute_db("UPDATE users SET nome = %s, username = %s WHERE id = %s",
                       (nome, username, user_id))

        # Atualizar sessão com novos dados
        session['nome'] = nome
        session['username'] = username

        flash('Perfil atualizado com sucesso.')
        return redirect(url_for('admin'))

    return render_template('admin_perfil.html', user=user)


# Gerenciar funcionárias (CRUD)

@app.route('/admin/funcionarias')
@admin_required
def listar_funcionarias():
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    return render_template('funcionarias.html', users=users)

@app.route('/admin/funcionarias/novo', methods=['GET', 'POST'])
@admin_required
def nova_funcionaria():
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

        exists = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
        if exists:
            flash('Nome de usuário já existe.')
            return redirect(url_for('nova_funcionaria'))

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        execute_db("INSERT INTO users (nome, username, senha, tipo) VALUES (%s, %s, %s, 'funcionaria')",
                   (nome, username, senha_hash))
        flash('Funcionária criada com sucesso.')
        return redirect(url_for('listar_funcionarias'))

    return render_template('funcionaria_form.html', acao='novo')

@app.route('/admin/funcionarias/editar/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def editar_funcionaria(user_id):
    user = query_db("SELECT * FROM users WHERE id = %s AND tipo = 'funcionaria'", (user_id,), one=True)
    if not user:
        flash('Funcionária não encontrada.')
        return redirect(url_for('listar_funcionarias'))

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']

        if not nome:
            flash('Nome é obrigatório.')
            return redirect(url_for('editar_funcionaria', user_id=user_id))

        if senha:
            if senha != senha_confirm:
                flash('Senhas não conferem.')
                return redirect(url_for('editar_funcionaria', user_id=user_id))
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            execute_db("UPDATE users SET nome = %s, senha = %s WHERE id = %s", (nome, senha_hash, user_id))
        else:
            execute_db("UPDATE users SET nome = %s WHERE id = %s", (nome, user_id))

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

# Listar registros

@app.route('/admin/registros', methods=['GET', 'POST'])
@admin_required
def listar_registros():
    cleanup_old_records()

    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")

    hoje = date.today()
    data_fim_str = hoje.strftime('%Y-%m-%d')
    data_inicio_default = hoje - timedelta(days=29)
    data_inicio_str = data_inicio_default.strftime('%Y-%m-%d')

    # Corrigido para receber date diretamente e formatar
    def format_data(d):
        if d is None:
            return '-'
        if isinstance(d, (datetime, date)):
            return d.strftime('%d/%m/%Y')
        # Caso venha string, tentar converter
        try:
            dt = datetime.strptime(d, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return d

    if request.method == 'POST':
        data_inicio_str = request.form.get('data_inicio')
        data_fim_str = request.form.get('data_fim')

        try:
            dt_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            dt_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

            if dt_fim < dt_inicio:
                flash('Data fim deve ser maior ou igual à data início.')
                return redirect(url_for('listar_registros'))

            limite_min = hoje - timedelta(days=90)
            if dt_inicio < limite_min:
                dt_inicio = limite_min
                data_inicio_str = dt_inicio.strftime('%Y-%m-%d')
                flash('O período mínimo permitido é de até 90 dias atrás. Ajustado a data de início.')
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

        # Formatar horas e data
        data_fmt = format_data(r['data'])

        def format_hora(h):
            if h is None:
                return '-'
            if isinstance(h, (datetime, time)):
                return h.strftime('%H:%M')
            try:
                dt = datetime.strptime(h, '%H:%M:%S')
                return dt.strftime('%H:%M')
            except:
                return h

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

# Editar/Incluir/Excluir registros

@app.route('/admin/registro/editar/<int:record_id>', methods=['GET', 'POST'])
@admin_required
def editar_registro(record_id):
    record = query_db("SELECT r.*, u.nome FROM records r JOIN users u ON r.user_id = u.id WHERE r.id = %s", (record_id,), one=True)
    if not record:
        flash('Registro não encontrado.')
        return redirect(url_for('listar_registros'))

    if request.method == 'POST':
        data = request.form['data']
        hora_entrada = request.form['hora_entrada'] or None
        hora_saida = request.form['hora_saida'] or None
        observacoes = request.form.get('observacoes', '').strip()

        def valid_time(t):
            if t is None or t == '':
                return True
            try:
                datetime.strptime(t, '%H:%M:%S')
                return True
            except:
                return False

        if not valid_time(hora_entrada) or not valid_time(hora_saida):
            flash('Horário inválido. Use formato HH:MM:SS ou deixe vazio.')
            return redirect(url_for('editar_registro', record_id=record_id))

        execute_db("UPDATE records SET data = %s, hora_entrada = %s, hora_saida = %s, observacoes = %s WHERE id = %s",
                   (data, hora_entrada, hora_saida, observacoes, record_id))
        flash('Registro atualizado.')
        return redirect(url_for('listar_registros'))

    return render_template('registro_form.html', record=record)

@app.route('/admin/registro/excluir/<int:record_id>', methods=['POST'])
@admin_required
def excluir_registro(record_id):
    execute_db("DELETE FROM records WHERE id = %s", (record_id,))
    flash('Registro excluído.')
    return redirect(url_for('listar_registros'))

@app.route('/admin/registro/novo', methods=['GET', 'POST'])
@admin_required
def novo_registro():
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    if request.method == 'POST':
        user_id = request.form['user_id']
        data = request.form['data']
        hora_entrada = request.form['hora_entrada'] or None
        hora_saida = request.form['hora_saida'] or None
        observacoes = request.form.get('observacoes', '').strip()

        def valid_time(t):
            if t is None or t == '':
                return True
            try:
                datetime.strptime(t, '%H:%M:%S')
                return True
            except:
                return False

        if not valid_time(hora_entrada) or not valid_time(hora_saida):
            flash('Horário inválido. Use formato HH:MM:SS ou deixe vazio.')
            return redirect(url_for('novo_registro'))

        execute_db("INSERT INTO records (user_id, data, hora_entrada, hora_saida, observacoes) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, data, hora_entrada, hora_saida, observacoes))
        flash('Registro criado.')
        return redirect(url_for('listar_registros'))

    return render_template('registro_form.html', users=users, novo=True)

# Relatórios (mantidos)

@app.route('/admin/relatorio', methods=['GET', 'POST'])
@admin_required
def relatorio():
    users = query_db("SELECT * FROM users WHERE tipo = 'funcionaria' ORDER BY nome")
    rel_data = None

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        if not data_inicio or not data_fim:
            flash('Informe o período.')
            return redirect(url_for('relatorio'))

        try:
            dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            dt_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            if dt_fim < dt_inicio:
                flash('Data fim deve ser maior ou igual à data início.')
                return redirect(url_for('relatorio'))
        except:
            flash('Formato de data inválido.')
            return redirect(url_for('relatorio'))

        if user_id == 'todos':
            registros = query_db("""
                SELECT r.*, u.nome FROM records r
                JOIN users u ON r.user_id = u.id
                WHERE r.data BETWEEN %s AND %s
                ORDER BY r.data, u.nome
            """, (data_inicio, data_fim))
        else:
            registros = query_db("""
                SELECT r.*, u.nome FROM records r
                JOIN users u ON r.user_id = u.id
                WHERE r.user_id = %s AND r.data BETWEEN %s AND %s
                ORDER BY r.data
            """, (user_id, data_inicio, data_fim))

        dias = []
        delta = (dt_fim - dt_inicio).days + 1
        for i in range(delta):
            dias.append(dt_inicio + timedelta(days=i))

        registros_dict = {}
        for r in registros:
            key = (r['user_id'], r['data'])
            registros_dict[key] = r

        def calcular_horas_valor(data_obj, entrada, saida):
            if not entrada or not saida:
                return 0, 0.0
            # entrada e saida podem ser time ou string
            def parse_time(t):
                if isinstance(t, time):
                    return datetime.combine(date.min, t)
                try:
                    return datetime.strptime(t, '%H:%M:%S')
                except:
                    return None

            h_entrada = parse_time(entrada)
            h_saida = parse_time(saida)
            if h_entrada is None or h_saida is None:
                return 0, 0.0

            if h_saida < h_entrada:
                h_saida += timedelta(days=1)
            diff = h_saida - h_entrada
            horas = diff.total_seconds() / 3600

            # Domingo = R$ 100 fixos
            if data_obj.weekday() == 6:
                valor = 100.0
            else:
                valor = horas * 6.90
            return horas, valor

        usuarios_rel = []
        if user_id == 'todos':
            user_ids = list(set([r['user_id'] for r in registros]))
            if not user_ids:
                user_ids = [u['id'] for u in users]
        else:
            user_ids = [int(user_id)]

        for uid in user_ids:
            user_nome = next((u['nome'] for u in users if u['id'] == uid), 'Desconhecido')
            linhas = []
            total_horas = 0.0
            total_valor = 0.0
            for d in dias:
                r = registros_dict.get((uid, d))
                if r:
                    horas, valor = calcular_horas_valor(d, r['hora_entrada'], r['hora_saida'])
                    entrada = r['hora_entrada'] or '-'
                    saida = r['hora_saida'] or '-'
                    # Formatar horas para exibição HH:MM
                    def format_hora(h):
                        if h is None:
                            return '-'
                        if isinstance(h, (datetime, time)):
                            return h.strftime('%H:%M')
                        try:
                            dt = datetime.strptime(h, '%H:%M:%S')
                            return dt.strftime('%H:%M')
                        except:
                            return h
                    entrada = format_hora(entrada)
                    saida = format_hora(saida)
                else:
                    entrada = '-'
                    saida = '-'
                    horas = 0
                    valor = 0
                linhas.append({
                    'data': d.strftime('%d/%m/%Y'),
                    'entrada': entrada,
                    'saida': saida,
                    'horas': round(horas, 2),
                    'valor': round(valor, 2),
                    'sem_registro': (entrada == '-' and saida == '-')
                })
                total_horas += horas
                total_valor += valor
            usuarios_rel.append({
                'nome': user_nome,
                'linhas': linhas,
                'total_horas': round(total_horas, 2),
                'total_valor': round(total_valor, 2)
            })

        rel_data = {
            'inicio': data_inicio,
            'fim': data_fim,
            'usuarios': usuarios_rel
        }

    return render_template('relatorio.html', users=users, rel_data=rel_data)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
