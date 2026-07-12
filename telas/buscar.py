import tkinter as tk
from tkinter import messagebox

from excel import buscar_lead_por_telefone


def abrir_busca():

    janela_busca = tk.Toplevel()

    janela_busca.title("Buscar Lead")
    janela_busca.geometry("500x500")


    tk.Label(
        janela_busca,
        text="Digite o telefone:"
    ).pack()


    campo_telefone = tk.Entry(janela_busca)
    campo_telefone.pack()


    resultado = tk.Text(janela_busca)

    resultado.pack(
        padx=10,
        pady=10
    )


    def buscar():

        telefone = campo_telefone.get()

        lead = buscar_lead_por_telefone(telefone)


        resultado.delete(
            1.0,
            tk.END
        )


        if lead:

            texto = (
                f"Nome: {lead['nome']}\n"
                f"Telefone: {lead['telefone']}\n"
                f"E-mail: {lead['email']}\n"
                f"Interesse: {lead['interesse']}\n"
                f"Origem: {lead['origem']}\n"
                f"Consultor: {lead['consultor']}\n"
                f"Observação: {lead['observacao']}"
            )

            resultado.insert(
                tk.END,
                texto
            )

        else:

            messagebox.showwarning(
                "Não encontrado",
                "Nenhum lead encontrado."
            )


    botao = tk.Button(
        janela_busca,
        text="Buscar",
        command=buscar
    )

    botao.pack(
        pady=10
    )

    