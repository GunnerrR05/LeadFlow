import tkinter as tk
from tkinter import messagebox

from telas.cadastro import cadastrar
from telas.listar import abrir_lista
from telas.buscar import abrir_busca

from excel import (
    salvar_lead,
    pegar_leads, 
    buscar_lead_por_telefone, 
    atualizar_lead, 
    excluir_lead
    )

lead_selecionado = None

janela = tk.Tk()
janela.title("LeadFlow")
janela.geometry("600x600")


titulo = tk.Label(
    janela,
    text="Sistema de Leads",
    font=("Arial", 20)
    )
titulo.pack()

######################################

label_busca = tk.Label(
    janela,
    text="Buscar por telefone"
)
label_busca.pack()
campo_busca = tk.Entry(janela)
campo_busca.pack()

######################################

label_nome = tk.Label(
    janela,
    text="Nome"
    )
label_nome.pack()
campo_nome = tk.Entry(janela)
campo_nome.pack()

######################################

label_telefone = tk.Label(
    janela,
    text="Telefone"
    )
label_telefone.pack()
campo_telefone = tk.Entry(janela)
campo_telefone.pack()

######################################

label_email = tk.Label(
    janela,
    text="E-mail"
    )
label_email.pack()
campo_email = tk.Entry(janela)
campo_email.pack()

######################################

label_interesse = tk.Label(
    janela,
    text="Interesse"
    )
label_interesse.pack()
campo_interesse = tk.Entry(janela)
campo_interesse.pack()

######################################

label_origem = tk.Label(
    janela,
    text="Origem"
    )
label_origem.pack()
campo_origem = tk.Entry(janela)
campo_origem.pack()

######################################

label_consultor = tk.Label(
    janela,
    text="Consultor"
    )
label_consultor.pack()
campo_consultor = tk.Entry(janela)
campo_consultor.pack()

######################################

label_observacao = tk.Label(
    janela,
    text="Observações"
    )
label_observacao.pack()
campo_observacao = tk.Entry(janela)
campo_observacao.pack()

#--------------------------------------#


botao_cadastrar = tk.Button(
    janela,
    text="Cadastrar Lead",
    command=lambda: cadastrar(
        campo_nome,
        campo_telefone,
        campo_email,
        campo_interesse,
        campo_origem,
        campo_consultor,
        campo_observacao
    )
)

botao_cadastrar.pack()


#--------------------------------------#


def atualizar():
    if lead_selecionado is not None:

        lead_selecionado["nome"] = campo_nome.get()
        lead_selecionado["telefone"] = campo_telefone.get()
        lead_selecionado["email"] = campo_email.get()
        lead_selecionado["interesse"] = campo_interesse.get()
        lead_selecionado["origem"] = campo_origem.get()
        lead_selecionado["consultor"] = campo_consultor.get()
        lead_selecionado["observacao"] = campo_observacao.get()

        atualizar_lead(lead_selecionado)

        messagebox.showinfo(
            "Sucesso",
            "Lead atualizado com sucesso!"
        )

botao_atualizar = tk.Button(
    janela,
    text="Atualizar Lead",
    command=atualizar
    )

botao_atualizar.pack()


#--------------------------------------#


def limpar():
    campo_nome.delete(0, tk.END)
    campo_telefone.delete(0, tk.END)
    campo_email.delete(0, tk.END)
    campo_interesse.delete(0, tk.END)
    campo_origem.delete(0, tk.END)
    campo_consultor.delete(0, tk.END)
    campo_observacao.delete(0, tk.END)
    campo_busca.delete(0, tk.END)

botao_limpar = tk.Button(
    janela,
    text="Limpar",
    command=limpar
    )

botao_limpar.pack()


#--------------------------------------#


botao_listar = tk.Button(
    janela,
    text="Listar Leads",
    command=abrir_lista
    )

botao_listar.pack()


#--------------------------------------#



botao_buscar = tk.Button(
    janela,
    text="Buscar",
    command=abrir_busca
)

botao_buscar.pack()


#--------------------------------------#


def excluir():
    global lead_selecionado

    if lead_selecionado is not None:
        confirmacao = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este lead?"
        )

        if confirmacao:
            excluir_lead(lead_selecionado["linha"])
            
            messagebox.showinfo(
                "Sucesso",
                "Lead excluído com sucesso!"
            )

            limpar()
            lead_selecionado = None

botao_excluir = tk.Button(
    janela,
    text="Excluir Lead",
    command=excluir
)

botao_excluir.pack()


janela.mainloop()