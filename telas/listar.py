import tkinter as tk
from servicos.leads import listar_leads


def abrir_lista():

    janela_lista = tk.Toplevel()

    janela_lista.title("Leads cadastrados")
    janela_lista.geometry("500x400")


    caixa_texto = tk.Text(janela_lista)

    caixa_texto.pack(
        expand=True,
        fill="both"
    )


    leads = listar_leads()


    for numero, lead in enumerate(leads, start=1):

        texto = (
            f"LEAD {numero}\n"
            f"Nome: {lead['nome']}\n"
            f"Telefone: {lead['telefone']}\n"
            f"E-mail: {lead['email']}\n"
            f"Interesse: {lead['interesse']}\n"
            f"Origem: {lead['origem']}\n"
            f"Consultor: {lead['consultor']}\n"
            f"Observação: {lead['observacao']}\n"
            "\n----------------------\n"
        )


        caixa_texto.insert(
            tk.END,
            texto
        )