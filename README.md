# Cadastro de produtos do supermercado

Aplicativo de estudo em Python para manter um catálogo local de produtos. A interface é feita com Tkinter, os dados ficam em SQLite e a lista pode ser exportada para uma planilha Excel.

## Recursos

- Cadastrar produto com código ou EAN, nome, categoria, estoque e preço de venda.
- Editar ou excluir um produto selecionado.
- Pesquisar por código, nome ou categoria.
- Validar campos obrigatórios, estoque e preço.
- Exportar os produtos encontrados na pesquisa para `.xlsx`.

## Como executar

Requer Python 3.10 ou mais recente. O Tkinter costuma vir com Python; no Linux, pode ser necessário instalar o pacote `python3-tk`.

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale a dependência:

- Windows: `.venv\Scripts\activate`
- macOS ou Linux: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
python main.py
```

O banco `produtos.sqlite3` é criado automaticamente na primeira execução e fica na pasta do projeto. O código/EAN identifica cada produto e não pode se repetir. Não há conexão com serviços externos.
