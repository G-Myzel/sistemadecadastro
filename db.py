import sqlite3

from config import DB_PATH


def conectar(caminho=DB_PATH):
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco_e_tabela(conexao):
    with conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                codigo TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                estoque INTEGER NOT NULL CHECK (estoque >= 0),
                preco REAL NOT NULL CHECK (preco >= 0)
            )
        """)
