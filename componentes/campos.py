import tkinter as tk


def criar_campos(janela):

    campos = {}


    tk.Label(janela, text="Nome").pack()
    campos["nome"] = tk.Entry(janela)
    campos["nome"].pack()


    tk.Label(janela, text="Telefone").pack()
    campos["telefone"] = tk.Entry(janela)
    campos["telefone"].pack()


    tk.Label(janela, text="E-mail").pack()
    campos["email"] = tk.Entry(janela)
    campos["email"].pack()


    tk.Label(janela, text="Interesse").pack()
    campos["interesse"] = tk.Entry(janela)
    campos["interesse"].pack()


    tk.Label(janela, text="Origem").pack()
    campos["origem"] = tk.Entry(janela)
    campos["origem"].pack()


    tk.Label(janela, text="Consultor").pack()
    campos["consultor"] = tk.Entry(janela)
    campos["consultor"].pack()


    tk.Label(janela, text="Observação").pack()
    campos["observacao"] = tk.Entry(janela)
    campos["observacao"].pack()


    tk.Label(janela, text="Status").pack()
    campos["status"] = tk.Entry(janela)
    campos["status"].pack()


    tk.Label(janela, text="Prioridade").pack()
    campos["prioridade"] = tk.Entry(janela)
    campos["prioridade"].pack()


    tk.Label(janela, text="Próximo contato").pack()
    campos["proximo_contato"] = tk.Entry(janela)
    campos["proximo_contato"].pack()

    return campos