from pathlib import Path

# O banco fica ao lado dos arquivos do programa.
DB_PATH = Path(__file__).with_name("produtos.sqlite3")
