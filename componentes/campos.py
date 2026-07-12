import tkinter as tk


def criar_campos(janela):

    campos = {}

    campos["nome"] = tk.Entry(janela)
    campos["telefone"] = tk.Entry(janela)
    campos["email"] = tk.Entry(janela)
    campos["interesse"] = tk.Entry(janela)
    campos["origem"] = tk.Entry(janela)
    campos["consultor"] = tk.Entry(janela)
    campos["observacao"] = tk.Entry(janela)

    return campos