from tkinter import ttk


def configurar_estilos(janela):
    janela.configure(background="#f2f4f7")
    estilos = ttk.Style(janela)
    estilos.theme_use("clam")
    estilos.configure("TFrame", background="#f2f4f7")
    estilos.configure("TLabel", background="#f2f4f7", foreground="#243247")
    estilos.configure(
        "Titulo.TLabel",
        background="#f2f4f7",
        foreground="#153b5b",
        font=("TkDefaultFont", 20, "bold"),
    )
    estilos.configure(
        "Subtitulo.TLabel",
        background="#f2f4f7",
        foreground="#5b6777",
        font=("TkDefaultFont", 10),
    )
    estilos.configure("TLabelframe", background="#f2f4f7")
    estilos.configure(
        "TLabelframe.Label",
        background="#f2f4f7",
        foreground="#153b5b",
        font=("TkDefaultFont", 10, "bold"),
    )
    estilos.configure("TButton", padding=(10, 6))
    estilos.configure(
        "Acao.TButton",
        background="#19764a",
        foreground="white",
        font=("TkDefaultFont", 9, "bold"),
    )
    estilos.map(
        "Acao.TButton",
        background=[("active", "#145f3b"), ("disabled", "#a6b4ac")],
    )
    estilos.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        rowheight=28,
        borderwidth=0,
    )
    estilos.configure(
        "Treeview.Heading",
        background="#e3e9ef",
        foreground="#243247",
        font=("TkDefaultFont", 9, "bold"),
    )
    estilos.map("Treeview", background=[("selected", "#cfe3f4")])
