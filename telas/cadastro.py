from tkinter import messagebox, END
from servicos.leads import cadastrar_lead


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