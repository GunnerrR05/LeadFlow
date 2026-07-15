import tkinter as tk

from tkinter import messagebox, END

from servicos.leads import cadastrar_lead

from componentes.campos import criar_campos


def cadastrar(
    campo_nome,
    campo_telefone,
    campo_email,
    campo_interesse,
    campo_origem,
    campo_consultor,
    campo_observacao
):

    campos = {
        "nome": campo_nome,
        "telefone": campo_telefone,
        "email": campo_email,
        "interesse": campo_interesse,
        "origem": campo_origem,
        "consultor": campo_consultor,
        "observacao": campo_observacao
    }

    cadastrar_lead(campos)

    messagebox.showinfo(
        "Sucesso",
        "Lead cadastrado com sucesso!"
    )

    for campo in campos.values():
        campo.delete(0, END)



def abrir_cadastro():

    janela_cadastro = tk.Toplevel()

    janela_cadastro.title("Cadastrar Lead")
    janela_cadastro.geometry("400x500")


    campos = criar_campos(janela_cadastro)


    def salvar():

        cadastrar_lead(campos)

        messagebox.showinfo(
            "Sucesso",
            "Lead cadastrado com sucesso!"
        )

        for campo in campos.values():
            campo.delete(0, END)


    botao = tk.Button(
        janela_cadastro,
        text="Cadastrar Lead",
        command=salvar
    )

    botao.pack(pady=10)