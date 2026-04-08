import sqlite3
import os

# • get_db_connection() — retorna uma conexão configurada com row_factory
def get_db_connection():
    conn = sqlite3.connect('dados.db', timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000') # espera até 5s
    conn.row_factory = sqlite3.Row
    return conn

# • init_db() — cria as tabelas se não existirem (executa o schema.sql)
def init_db():
    if not os.path.exists('dados.db'):
        with get_db_connection() as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())

# • inserir_leitura(temperatura, umidade, pressao=None) — INSERT
def inserir_leitura(temperatura, umidade, pressao=None):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
            (temperatura, umidade, pressao)
        )
        return cursor.lastrowid
    
# • listar_leituras(limite=50, offset=0) — SELECT com paginação básica
def listar_leituras(limite=50, offset=0):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ? OFFSET ?',
            (limite, offset)
        )
        return [dict(row) for row in cursor.fetchall()]

# • contar_leituras() — retorna total de leituras no banco
def contar_leituras():
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT COUNT(*) as total FROM leituras')
        row = cursor.fetchone()
        return row['total'] if row else 0

# • buscar_leitura(id) — SELECT por id    
def buscar_leitura(id): 
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM leituras WHERE id = ?',
            (id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

# • atualizar_leitura(id, dados) — UPDATE
def atualizar_leitura(id, dados):
    with get_db_connection() as conn:
        conn.execute(
            'UPDATE leituras SET temperatura = ?, umidade = ?, pressao = ? WHERE id = ?',
            (dados['temperatura'], dados['umidade'], dados.get('pressao'), id)
        )
        return buscar_leitura(id)

# • deletar_leitura(id) — DELETE    
def deletar_leitura(id):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
