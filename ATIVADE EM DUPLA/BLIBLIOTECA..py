import sqlite3

conexao = None

try:
    # Abre o banco da biblioteca e cria o cursor para executar SQL
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    # Cria a tabela livros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            ano INTEGER,
            -- 1 = disponível e 0 = emprestado
            disponivel INTEGER NOT NULL CHECK (disponivel IN (0, 1))
        )
    """)

    # 1. CREATE: cadastra cinco livros se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM livros")
    quantidade = cursor.fetchone()[0]

    if quantidade == 0:
        livros = [
            ("Dom Casmurro", "Machado de Assis", 1899, 1),
            ("O Cortiço", "Aluísio Azevedo", 1890, 1),
            ("Jogos Vorazes", "Suzanne Collins", 2008, 1),
            ("A Culpa é das Estrelas", "John Green", 2012, 0),
            ("Extraordinário", "R. J. Palacio", 2012, 1)
        ]

        cursor.executemany(
            "INSERT INTO livros (titulo, autor, ano, disponivel) VALUES (?, ?, ?, ?)",
            livros
        )
        conexao.commit()

    # 2. : mostra todos os livros e a situação de cada um
    print("\nTodos os livros:")
    cursor.execute("SELECT id, titulo, autor, ano, disponivel FROM livros ORDER BY id")

    for id_livro, titulo, autor, ano, disponivel in cursor.fetchall():
        if disponivel == 1:
            situacao = "1 = disponível"
        else:
            situacao = "0 = emprestado"

        print(f"{id_livro} - {titulo} | {autor} | {ano} | {situacao}")

    # Mostra apenas os livros disponíveis
    print("\nLivros disponíveis:")
    cursor.execute("SELECT titulo FROM livros WHERE disponivel = ?", (1,))

    for livro in cursor.fetchall():
        print(livro[0])

    # 3. UPDATE: simula o empréstimo de Jogos Vorazes
    cursor.execute(
        "UPDATE livros SET disponivel = ? WHERE titulo = ? AND disponivel = ?",
        (0, "Jogos Vorazes", 1)
    )
    conexao.commit()

    if cursor.rowcount > 0:
        print("\nEmpréstimo registrado: Jogos Vorazes.")

    # 4. DELETE: remove o livro doado para outra escola
    cursor.execute("DELETE FROM livros WHERE titulo = ?", ("O Cortiço",))
    conexao.commit()

    if cursor.rowcount > 0:
        print("\nO Cortiço foi doado e removido da biblioteca.")

    # 5. EXTRA: lista os livros publicados depois de 2000
    print("\nLivros publicados depois de 2000:")
    cursor.execute(
        "SELECT titulo, ano FROM livros WHERE ano > ? ORDER BY ano, titulo",
        (2000,)
    )

    for titulo, ano in cursor.fetchall():
        print(f"{titulo} - {ano}")

    # Menu: permite escolher um livro e consultar a situação atual no banco
    while True:
        print("\nEscolha um livro pelo ID:")
        cursor.execute("SELECT id, titulo FROM livros ORDER BY id")

        for id_livro, titulo in cursor.fetchall():
            print(f"{id_livro} - {titulo}")

        print("0 - Sair")
        escolha = input("Digite o ID do livro: ").strip()

        if escolha == "0":
            print("Consulta encerrada.")
            break

        # Busca apenas o livro que a pessoa escolheu
        cursor.execute(
            "SELECT titulo, disponivel FROM livros WHERE id = ?",
            (escolha,)
        )
        livro = cursor.fetchone()

        if livro is None:
            print("Livro não encontrado. Escolha um ID da lista.")
        else:
            titulo, disponivel = livro

            if disponivel == 1:
                print(f"{titulo} está disponível (1).")
            else:
                print(f"{titulo} está emprestado (0).")

except sqlite3.Error as erro:
    print("Erro no banco de dados:", erro)

finally:
    # Fecha a conexão ao sair do programa
    if conexao is not None:
        conexao.close()
