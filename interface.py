import tkinter as tk
from tkinter import messagebox

from telas.cadastro import cadastrar
from telas.listar import abrir_lista
from telas.buscar import abrir_busca

from componentes.campos import criar_campos
from componentes.botoes import criar_botoes

from servicos.leads import cadastrar_lead
from servicos.leads import cadastrar_lead, atualizar_lead

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




#--------------------------------------#


def atualizar():

    global lead_selecionado

    if lead_selecionado is not None:

        atualizar_lead(
            lead_selecionado,
            campos
        )

        messagebox.showinfo(
            "Sucesso",
            "Lead atualizado com sucesso!"
        )



#--------------------------------------#


def limpar():
    campos["nome"].delete(0, tk.END)
    campos["telefone"].delete(0, tk.END)
    campos["email"].delete(0, tk.END)
    campos["interesse"].delete(0, tk.END)
    campos["origem"].delete(0, tk.END)
    campos["consultor"].delete(0, tk.END)
    campos["observacao"].delete(0, tk.END)



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



def cadastrar():

    cadastrar_lead(campos)

    messagebox.showinfo(
        "Sucesso",
        "Lead cadastrado com sucesso!"
    )


botoes = criar_botoes(
    janela,
    cadastrar,
    limpar,
    abrir_lista,
    abrir_busca,
    campos
)

    
janela.mainloop()