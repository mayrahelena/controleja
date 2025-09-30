import bcrypt
import mysql.connector

# Configurações de conexão com o MySQL
config = {
    "host": "localhost",
    "user": "root",
    "password": "021998@Amor",  # sua senha do MySQL
    "database": "ponto_db"
}

# Defina a nova senha que deseja
nova_senha = "admin123"   # trocar por outra

# Gerar hash da senha com bcrypt
hashed = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt())
hash_str = hashed.decode("utf-8")

try:
    # Conectar ao MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Atualizar senha do usuário admin (id = 1)
    cursor.execute("UPDATE users SET senha = %s WHERE id = 1", (hash_str,))
    conn.commit()

    print("✅ Senha do administrador redefinida com sucesso!")
    print(f"Agora você pode entrar com: {nova_senha}")

except Exception as e:
    print("❌ Erro:", e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
