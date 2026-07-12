import tkinter as tk
from tkinter import messagebox

from telas.cadastro import cadastrar
from telas.listar import abrir_lista
from telas.buscar import abrir_busca

from componentes.campos import criar_campos

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

campos = criar_campos(janela)


######################################


botao_cadastrar = tk.Button(
    janela,
    text="Cadastrar Lead",
    command=lambda: cadastrar(
        campos["nome"],
        campos["telefone"],
        campos["email"],
        campos["interesse"],
        campos["origem"],
        campos["consultor"],
        campos["observacao"]
    )
)

botao_cadastrar.pack()


#--------------------------------------#


def atualizar():
    if lead_selecionado is not None:

        lead_selecionado["nome"] = campos["nome"].get()
        lead_selecionado["telefone"] = campos["telefone"].get()
        lead_selecionado["email"] = campos["email"].get()
        lead_selecionado["interesse"] = campos["interesse"].get()
        lead_selecionado["origem"] = campos["origem"].get()
        lead_selecionado["consultor"] = campos["consultor"].get()
        lead_selecionado["observacao"] = campos["observacao"].get()

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
    campos["nome"].delete(0, tk.END)
    campos["telefone"].delete(0, tk.END)
    campos["email"].delete(0, tk.END)
    campos["interesse"].delete(0, tk.END)
    campos["origem"].delete(0, tk.END)
    campos["consultor"].delete(0, tk.END)
    campos["observacao"].delete(0, tk.END)

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