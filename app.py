import math
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from openpyxl import Workbook

import repo
from style import configurar_estilos


class AppCadastro(tk.Tk):
    def __init__(self, conexao):
        super().__init__()
        self.conexao = conexao
        self.codigo_original = None

        self.title("Cadastro de produtos")
        self.geometry("980x650")
        self.minsize(780, 540)
        configurar_estilos(self)
        self._montar_interface()
        self._atualizar_lista()
        self.protocol("WM_DELETE_WINDOW", self._fechar)

    def _montar_interface(self):
        principal = ttk.Frame(self, padding=20)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Cadastro de produtos",
            style="Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            principal,
            text="Catálogo simples para o supermercado",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        barra = ttk.Frame(principal)
        barra.pack(fill="x", pady=(0, 12))
        ttk.Label(barra, text="Pesquisar:").pack(side="left")
        self.busca_var = tk.StringVar()
        self.busca_var.trace_add("write", lambda *_: self._atualizar_lista())
        pesquisa = ttk.Entry(barra, textvariable=self.busca_var, width=38)
        pesquisa.pack(side="left", fill="x", expand=True, padx=(8, 12))
        pesquisa.bind("<Return>", lambda _evento: self._atualizar_lista())
        ttk.Button(
            barra,
            text="Exportar para Excel",
            command=self._exportar_excel,
        ).pack(side="right")

        formulario = ttk.LabelFrame(principal, text="Dados do produto", padding=12)
        formulario.pack(fill="x", pady=(0, 12))
        for coluna in (0, 2):
            formulario.columnconfigure(coluna, weight=1)

        self.codigo_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.estoque_var = tk.StringVar()
        self.preco_var = tk.StringVar()

        self._campo(formulario, "Código / EAN", self.codigo_var, 0, 0)
        self._campo(formulario, "Nome", self.nome_var, 0, 2)
        self._campo(formulario, "Categoria", self.categoria_var, 1, 0)
        self._campo(formulario, "Estoque", self.estoque_var, 1, 2)
        self._campo(formulario, "Preço de venda (R$)", self.preco_var, 2, 0)

        botoes = ttk.Frame(formulario)
        botoes.grid(row=5, column=2, sticky="e", padx=(8, 0), pady=(8, 0))
        self.salvar_botao = ttk.Button(
            botoes,
            text="Cadastrar produto",
            style="Acao.TButton",
            command=self._salvar,
        )
        self.salvar_botao.pack(side="left")
        self.cancelar_botao = ttk.Button(
            botoes,
            text="Cancelar edição",
            command=self._limpar_formulario,
            state="disabled",
        )
        self.cancelar_botao.pack(side="left", padx=(8, 0))
        self.excluir_botao = ttk.Button(
            botoes,
            text="Excluir selecionado",
            command=self._excluir,
            state="disabled",
        )
        self.excluir_botao.pack(side="left", padx=(8, 0))

        tabela_frame = ttk.Frame(principal)
        tabela_frame.pack(fill="both", expand=True)
        colunas = ("codigo", "nome", "categoria", "estoque", "preco")
        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse",
        )
        titulos = {
            "codigo": "Código / EAN",
            "nome": "Produto",
            "categoria": "Categoria",
            "estoque": "Estoque",
            "preco": "Preço",
        }
        larguras = {"codigo": 130, "nome": 260, "categoria": 180, "estoque": 90, "preco": 110}
        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(coluna, width=larguras[coluna], anchor="w")
        self.tabela.column("estoque", anchor="center")
        self.tabela.column("preco", anchor="e")
        barra_rolagem = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela.yview,
        )
        self.tabela.configure(yscrollcommand=barra_rolagem.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        barra_rolagem.pack(side="right", fill="y")
        self.tabela.bind("<<TreeviewSelect>>", self._carregar_selecao)

        self.status_var = tk.StringVar()
        ttk.Label(principal, textvariable=self.status_var).pack(anchor="w", pady=(8, 0))

    @staticmethod
    def _campo(pai, rotulo, variavel, linha, coluna):
        ttk.Label(pai, text=rotulo).grid(
            row=linha * 2,
            column=coluna,
            sticky="w",
            padx=(0, 10),
            pady=(0, 3),
        )
        entrada = ttk.Entry(pai, textvariable=variavel)
        entrada.grid(
            row=linha * 2 + 1,
            column=coluna,
            sticky="ew",
            padx=(0, 16),
            pady=(0, 8),
        )

    def _dados_do_formulario(self):
        codigo = self.codigo_var.get().strip()
        nome = self.nome_var.get().strip()
        categoria = self.categoria_var.get().strip()
        estoque_texto = self.estoque_var.get().strip()
        preco_texto = self.preco_var.get().strip().replace(",", ".")

        if not codigo or not nome or not categoria:
            raise ValueError("Código, nome e categoria são obrigatórios.")
        if not estoque_texto.isdecimal():
            raise ValueError("O estoque deve ser um número inteiro igual ou maior que zero.")

        try:
            preco = float(preco_texto)
        except ValueError as erro:
            raise ValueError("Informe um preço válido, por exemplo 12,50.") from erro
        if not math.isfinite(preco) or preco < 0:
            raise ValueError("O preço deve ser um número igual ou maior que zero.")

        return {
            "codigo": codigo,
            "nome": nome,
            "categoria": categoria,
            "estoque": int(estoque_texto),
            "preco": preco,
        }

    def _salvar(self):
        try:
            dados = self._dados_do_formulario()
            if self.codigo_original is None:
                repo.adicionar_produto(self.conexao, dados)
                acao = "cadastrado"
            else:
                repo.atualizar_produto(self.conexao, self.codigo_original, dados)
                acao = "atualizado"
        except ValueError as erro:
            messagebox.showwarning("Confira os dados", str(erro), parent=self)
            return
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Código já cadastrado",
                "Já existe um produto com esse código ou EAN.",
                parent=self,
            )
            return
        except sqlite3.Error as erro:
            messagebox.showerror("Erro no banco de dados", str(erro), parent=self)
            return

        self._limpar_formulario()
        self._atualizar_lista()
        self.status_var.set(f"Produto {acao} com sucesso.")

    def _atualizar_lista(self):
        if not hasattr(self, "tabela"):
            return
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        produtos = repo.listar_produtos(self.conexao, self.busca_var.get())
        for produto in produtos:
            self.tabela.insert(
                "",
                "end",
                iid=produto["codigo"],
                values=(
                    produto["codigo"],
                    produto["nome"],
                    produto["categoria"],
                    produto["estoque"],
                    f"R$ {produto['preco']:.2f}".replace(".", ","),
                ),
            )
        quantidade = len(produtos)
        self.status_var.set(
            f"{quantidade} produto cadastrado." if quantidade == 1
            else f"{quantidade} produtos cadastrados."
        )

    def _carregar_selecao(self, _evento=None):
        selecionados = self.tabela.selection()
        if not selecionados:
            return
        codigo = selecionados[0]
        produto = repo.buscar_produto(self.conexao, codigo)
        if produto is None:
            return
        self.codigo_original = codigo
        self.codigo_var.set(produto["codigo"])
        self.nome_var.set(produto["nome"])
        self.categoria_var.set(produto["categoria"])
        self.estoque_var.set(str(produto["estoque"]))
        self.preco_var.set(f"{produto['preco']:.2f}".replace(".", ","))
        self.salvar_botao.configure(text="Salvar alterações")
        self.cancelar_botao.configure(state="normal")
        self.excluir_botao.configure(state="normal")

    def _limpar_formulario(self):
        self.codigo_original = None
        for variavel in (
            self.codigo_var,
            self.nome_var,
            self.categoria_var,
            self.estoque_var,
            self.preco_var,
        ):
            variavel.set("")
        selecionados = self.tabela.selection()
        if selecionados:
            self.tabela.selection_remove(*selecionados)
        self.salvar_botao.configure(text="Cadastrar produto")
        self.cancelar_botao.configure(state="disabled")
        self.excluir_botao.configure(state="disabled")

    def _excluir(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            messagebox.showinfo(
                "Selecione um produto",
                "Escolha um produto na lista antes de excluir.",
                parent=self,
            )
            return
        codigo = selecionados[0]
        if not messagebox.askyesno(
            "Excluir produto",
            "Deseja excluir o produto selecionado?",
            parent=self,
        ):
            return
        try:
            repo.excluir_produto(self.conexao, codigo)
        except sqlite3.Error as erro:
            messagebox.showerror("Erro no banco de dados", str(erro), parent=self)
            return
        self._limpar_formulario()
        self._atualizar_lista()
        self.status_var.set("Produto excluído.")

    def _exportar_excel(self):
        produtos = repo.listar_produtos(self.conexao, self.busca_var.get())
        if not produtos:
            messagebox.showinfo(
                "Lista vazia",
                "Não há produtos para exportar.",
                parent=self,
            )
            return
        caminho = filedialog.asksaveasfilename(
            parent=self,
            title="Salvar catálogo",
            defaultextension=".xlsx",
            filetypes=[("Planilha do Excel", "*.xlsx")],
            initialfile="produtos-supermercado.xlsx",
        )
        if not caminho:
            return

        planilha = Workbook()
        aba = planilha.active
        aba.title = "Produtos"
        aba.append(["Código / EAN", "Produto", "Categoria", "Estoque", "Preço de venda (R$)"])
        for produto in produtos:
            aba.append([
                produto["codigo"],
                produto["nome"],
                produto["categoria"],
                produto["estoque"],
                produto["preco"],
            ])
        aba.freeze_panes = "A2"
        aba.auto_filter.ref = aba.dimensions
        aba.column_dimensions["A"].width = 20
        aba.column_dimensions["B"].width = 32
        aba.column_dimensions["C"].width = 24
        aba.column_dimensions["D"].width = 14
        aba.column_dimensions["E"].width = 22
        for celula in aba["E"][1:]:
            celula.number_format = '"R$" #,##0.00'

        try:
            planilha.save(caminho)
        except OSError as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self)
            return
        messagebox.showinfo("Exportação concluída", f"Planilha salva em:\n{caminho}", parent=self)

    def _fechar(self):
        self.conexao.close()
        self.destroy()


def appCadastro(conexao):
    return AppCadastro(conexao)
