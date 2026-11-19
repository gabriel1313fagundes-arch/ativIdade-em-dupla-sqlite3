import sqlite3

banco = None

try:
    # Abre o banco e cria o cursor para executar os comandos SQL
    banco = sqlite3.connect("petshop.db")
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT,
            tutor TEXT,
            idade INTEGER
        )
    """)

    # 1. CREATE - Cadastra cinco pets se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM pets")
    quantidade = cursor.fetchone()[0]

    if quantidade == 0:
        pets = [
            ("Rex", "cachorro", "murilo", 4),
            ("Luna", "gato", "Mirella", 2),
            ("Pipoca", "coelho", "Kennad", 1),
            ("Mel", "cachorro", "Gabriel", 3),
            ("Louro", "papagaio", "davis", 6)
        ]

        cursor.executemany("""
            INSERT INTO pets (nome, especie, tutor, idade)
            VALUES (?, ?, ?, ?)
        """, pets)

    # 2. READ - Mostra todos os pets e depois apenas os cachorros
    print("\nTodos os pets:")
    cursor.execute("SELECT id, nome, especie, tutor, idade FROM pets ORDER BY id")

    for id_pet, nome, especie, tutor, idade in cursor.fetchall():
        print(f"{id_pet} - {nome} | {especie} | Tutor: {tutor} | Idade: {idade}")

    print("\nApenas os cachorros:")
    cursor.execute("SELECT nome FROM pets WHERE especie = ? ORDER BY id", ("cachorro",))

    for nome, in cursor.fetchall():
        print(nome)

    # 3. UPDATE - Altera a tutora da Luna de Mirella para Carla
    cursor.execute("""
        UPDATE pets SET tutor = ?
        WHERE nome = ? AND especie = ? AND tutor = ?
    """, ("Carla", "Luna", "gato", "Mirella"))

    # 4. DELETE - Exclui o coelho Pipoca, do tutor 
    cursor.execute("""
        DELETE FROM pets
        WHERE nome = ? AND especie = ? AND tutor = ?
    """, ("Pipoca", "coelho", "Kennad"))

    banco.commit()  # Salva os cadastros, a atualização e a exclusão

    # 5. EXTRA - Mostra somente o nome e o tutor de cada pet restante
    print("\nNome do pet | Tutor")
    cursor.execute("SELECT nome, tutor FROM pets ORDER BY id")

    for nome, tutor in cursor.fetchall():
        print(f"{nome} | {tutor}")

except sqlite3.Error as erro:
    print("Erro no banco de dados:", erro)

finally:
    # Fecha a conexão mesmo se algum comando der erro.
    if banco is not None:
        banco.close()
