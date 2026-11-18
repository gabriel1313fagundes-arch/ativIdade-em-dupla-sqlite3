import sqlite3

conexao = sqlite3.connect("bliblioteca.db")

cursor = conexao.cursor()

print("Banco conectado!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT NOT NULL,
autor TEXT NOT NULL,
ano INTEGER,
disponivel INTEGER 1 = disponivel, 0 = emprestado
)
""")
