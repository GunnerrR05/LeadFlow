from excel import salvar_lead
from tkinter import messagebox, END


def cadastrar(
    campo_nome,
    campo_telefone,
    campo_email,
    campo_interesse,
    campo_origem,
    campo_consultor,
    campo_observacao
):
    nome = campo_nome.get()
    telefone = campo_telefone.get()
    email = campo_email.get()
    interesse = campo_interesse.get()
    origem = campo_origem.get()
    consultor = campo_consultor.get()
    observacao = campo_observacao.get()

    lead = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "interesse": interesse,
        "origem": origem,
        "consultor": consultor,
        "observacao": observacao,
        "status": "Novo",
        "prioridade": "Morno",
        "proximo_contato": "",
        "ultima_interacao": ""
    }

    salvar_lead(lead)
    
    messagebox.showinfo(
        "Sucesso",
        "Lead cadastrado com sucesso!"
    )
    
    campo_nome.delete(0, END)
    campo_telefone.delete(0, END)
    campo_email.delete(0, END)
    campo_interesse.delete(0, END)
    campo_origem.delete(0, END)
    campo_consultor.delete(0, END)
    campo_observacao.delete(0, END)