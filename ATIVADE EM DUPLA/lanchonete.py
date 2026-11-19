
import sqlite3

try:
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conexao = sqlite3.connect("lanchonete.db")
    cursor = conexao.cursor()

    # Criação das tabelas cardapio e pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cardapio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        categoria TEXT,
        preco REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        item TEXT,
        quantidade INTEGER
    )
    """)

    # 1. CREATE: Cadastrar 6 itens no cardápio e 4 pedidos
    # (Verificamos se já existem dados para não duplicar ao rodar o menu várias vezes)
    cursor.execute("SELECT COUNT(*) FROM cardapio")
    if cursor.fetchone()[0] == 0:
        itens_cardapio = [
            ("X-Burguer", "Lanche", 18.50),
            ("X-Salada", "Lanche", 20.00),
            ("Suco de Laranja", "Bebida", 8.00),
            ("Refrigerante Lata", "Bebida", 6.00),
            ("Água Mineral", "Bebida", 4.00),
            ("Pudim", "Sobremesa", 9.50)
        ]
        cursor.executemany(
            "INSERT INTO cardapio (item, categoria, preco) VALUES (?, ?, ?)",
            itens_cardapio
        )

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    if cursor.fetchone()[0] == 0:
        lista_pedidos = [
            ("Carlos", "X-Burguer", 2),
            ("Mariana", "Suco de Laranja", 1),
            ("Lucas", "X-Salada", 1),
            ("Fernanda", "Pudim", 2)
        ]
        cursor.executemany(
            "INSERT INTO pedidos (cliente, item, quantidade) VALUES (?, ?, ?)",
            lista_pedidos
        )
    conexao.commit()

    # 2. READ: Listar o cardápio inteiro e depois só as bebidas
    print("--- CARDÁPIO COMPLETO ---")
    cursor.execute("SELECT * FROM cardapio")
    for prato in cursor.fetchall():
        print(prato)

    print("\n--- APENAS BEBIDAS ---")
    cursor.execute("SELECT * FROM cardapio WHERE categoria = ?", ("Bebida",))
    for bebida in cursor.fetchall():
        print(bebida)

    # 3. UPDATE: Reajustar o preço de um item do cardápio (Ex: X-Burguer para 19.90)
    cursor.execute(
        "UPDATE cardapio SET preco = ? WHERE item = ?",
        (19.90, "X-Burguer")
    )
    conexao.commit()
    print("\n[Info] Preço do X-Burguer atualizado para R$ 19.90.")

    # 4. DELETE: Cancelar um pedido, excluindo-o da tabela pedidos (Ex: id = 2)
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (2,))
    conexao.commit()
    print("[Info] Pedido de ID 2 cancelado e removido.")

    # 5. EXTRA: Menu interativo com while e input()
    while True:
        print("\n=== MENU DO ATENDENTE (PEDIDOS) ===")
        print("1 - Cadastrar novo pedido")
        print("2 - Listar pedidos")
        print("3 - Atualizar quantidade de um pedido")
        print("4 - Excluir pedido")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente = input("Nome do cliente: ")
            item = input("Nome do item pedido: ")
            quantidade = int(input("Quantidade: "))
            cursor.execute(
                "INSERT INTO pedidos (cliente, item, quantidade) VALUES (?, ?, ?)",
                (cliente, item, quantidade)
            )
            conexao.commit()
            print("Pedido cadastrado com sucesso!")

        elif opcao == "2":
            print("\n--- LISTA DE PEDIDOS ATUAIS ---")
            cursor.execute("SELECT * FROM pedidos")
            for pedido in cursor.fetchall():
                print(pedido)

        elif opcao == "3":
            id_pedido = int(input("Digite o ID do pedido que deseja alterar: "))
            nova_qtd = int(input("Digite a nova quantidade: "))
            cursor.execute(
                "UPDATE pedidos SET quantidade = ? WHERE id = ?",
                (nova_qtd, id_pedido)
            )
            conexao.commit()
            print("Pedido atualizado com sucesso!")

        elif opcao == "4":
            id_pedido = int(input("Digite o ID do pedido que deseja cancelar: "))
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
            conexao.commit()
            print("Pedido excluído com sucesso!")

        elif opcao == "5":
            print("Encerrando o sistema da lanchonete...")
            break

        else:
            print("Opção inválida! Tente novamente.")

    # Encerra a conexão com o banco
    conexao.close()

except sqlite3.Error as erro:
    print("Erro no banco de dados:", erro)
except ValueError:
    print("Erro de digitação: você inseriu um texto onde era esperado um número.")


















