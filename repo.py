def adicionar_produto(conexao, produto):
    with conexao:
        conexao.execute(
            """
            INSERT INTO produtos (codigo, nome, categoria, estoque, preco)
            VALUES (:codigo, :nome, :categoria, :estoque, :preco)
            """,
            produto,
        )


def atualizar_produto(conexao, codigo_original, produto):
    with conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET codigo = :codigo,
                nome = :nome,
                categoria = :categoria,
                estoque = :estoque,
                preco = :preco
            WHERE codigo = :codigo_original
            """,
            {**produto, "codigo_original": codigo_original},
        )


def excluir_produto(conexao, codigo):
    with conexao:
        conexao.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))


def buscar_produto(conexao, codigo):
    return conexao.execute(
        """
        SELECT codigo, nome, categoria, estoque, preco
        FROM produtos
        WHERE codigo = ?
        """,
        (codigo,),
    ).fetchone()


def listar_produtos(conexao, busca=""):
    termo = f"%{busca.strip()}%"
    return conexao.execute(
        """
        SELECT codigo, nome, categoria, estoque, preco
        FROM produtos
        WHERE codigo LIKE ? OR nome LIKE ? OR categoria LIKE ?
        ORDER BY nome COLLATE NOCASE, codigo
        """,
        (termo, termo, termo),
    ).fetchall()
