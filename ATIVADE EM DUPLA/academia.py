
import sqlite3

try:
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conexao = sqlite3.connect("academia.db")
    cursor = conexao.cursor()

    # Criação das tabelas alunos e treinos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        plano TEXT,
        ativo INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno TEXT NOT NULL,
        exercicio TEXT,
        series INTEGER
    )
    """)

    # 1. CREATE: Cadastrar 6 alunos e 4 treinos usando listas e executemany
    cursor.execute("SELECT COUNT(*) FROM alunos")
    if cursor.fetchone() == 0:
        lista_alunos = [
            ("João Silva", "Mensal", 1),
            ("Maria Oliveira", "Anual", 1),
            ("Pedro Santos", "Trimestral", 1),
            ("Ana Costa", "Mensal", 0),
            ("Lucas Lima", "Anual", 1),
            ("Carla Souza", "Mensal", 0)
        ]
        cursor.executemany(
            "INSERT INTO alunos (nome, plano, ativo) VALUES (?, ?, ?)",
            lista_alunos
        )

    cursor.execute("SELECT COUNT(*) FROM treinos")
    if cursor.fetchone() == 0:
        lista_treinos = [
            ("João Silva", "Supino Reto", 4),
            ("Maria Oliveira", "Agachamento Livre", 4),
            ("Pedro Santos", "Puxada Frontal", 3),
            ("Lucas Lima", "Leg Press", 4)
        ]
        cursor.executemany(
            "INSERT INTO treinos (aluno, exercicio, series) VALUES (?, ?, ?)",
            lista_treinos
        )
    conexao.commit()

    # 2. READ: Listar todos os alunos e depois só os ativos
    print("--- TODOS OS ALUNOS ---")
    cursor.execute("SELECT * FROM alunos")
    for aluno in cursor.fetchall():
        print(aluno)

    print("\n--- APENAS ALUNOS ATIVOS ---")
    cursor.execute("SELECT * FROM alunos WHERE ativo = ?", (1,))
    for ativo in cursor.fetchall():
        print(ativo)

    # 3. UPDATE: Atualizar o plano de um aluno
    cursor.execute(
        "UPDATE alunos SET plano = ? WHERE nome = ?",
        ("Anual", "João Silva")
    )
    conexao.commit()
    print("\n[Info] Plano de João Silva atualizado para Anual.")

    # 4. DELETE: Cancelar/excluir um treino da tabela treinos
    cursor.execute("DELETE FROM treinos WHERE id = ?", (2,))
    conexao.commit()
    print("[Info] Treino de ID 2 cancelado e removido.")

    # 5. EXTRA: Menu interativo com while e input()
    while True:
        print("\n=== MENU DA ACADEMIA (TREINOS) ===")
        print("1 - Cadastrar novo treino")
        print("2 - Listar treinos")
        print("3 - Atualizar séries de um treino")
        print("4 - Excluir treino")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            aluno = input("Nome do aluno: ")
            exercicio = input("Nome do exercício: ")
            series = int(input("Número de séries: "))
            cursor.execute(
                "INSERT INTO treinos (aluno, exercicio, series) VALUES (?, ?, ?)",
                (aluno, exercicio, series)
            )
            conexao.commit()
            print("Treino cadastrado com sucesso!")

        elif opcao == "2":
            print("\n--- LISTA DE TREINOS ATUAIS ---")
            cursor.execute("SELECT * FROM treinos")
            for treino in cursor.fetchall():
                print(treino)

        elif opcao == "3":
            id_treino = int(input("Digite o ID do treino que deseja alterar: "))
            novas_series = int(input("Digite a nova quantidade de séries: "))
            cursor.execute(
                "UPDATE treinos SET series = ? WHERE id = ?",
                (novas_series, id_treino)
            )
            conexao.commit()
            print("Treino atualizado com sucesso!")

        elif opcao == "4":
            id_treino = int(input("Digite o ID do treino que deseja excluir: "))
            cursor.execute("DELETE FROM treinos WHERE id = ?", (id_treino,))
            conexao.commit()
            print("Treino excluído com sucesso!")

        elif opcao == "5":
            print("Encerrando o sistema da academia...")
            break

        else:
            print("Opção inválida! Tente novamente.")

    # Encerra a conexão com o banco
    conexao.close()

except sqlite3.Error as erro:
    print("Erro no banco de dados:", erro)
except ValueError:
    print("Erro de digitação: você inseriu um texto onde era esperado um número.")
