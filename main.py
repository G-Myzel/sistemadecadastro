from app import appCadastro
from db import conectar, criar_banco_e_tabela


def main():
    conexao = conectar()
    criar_banco_e_tabela(conexao)
    aplicativo = appCadastro(conexao)
    aplicativo.mainloop()


if __name__ == "__main__":
    main()
