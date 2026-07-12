import tkinter as tk
from tkinter import messagebox
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
janela.geometry("400x300")


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

def cadastrar():
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
        "observacao": observacao
    }

    salvar_lead(lead)
    
    messagebox.showinfo(
        "Sucesso",
        "Lead cadastrado com sucesso!"
    )
    
    campo_nome.delete(0, tk.END)
    campo_telefone.delete(0, tk.END)
    campo_email.delete(0, tk.END)
    campo_interesse.delete(0, tk.END)
    campo_origem.delete(0, tk.END)
    campo_consultor.delete(0, tk.END)
    campo_observacao.delete(0, tk.END)

botao_cadastrar = tk.Button(
janela,
text="Cadastrar Lead",
command=cadastrar
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


def listar():
    janela_lista = tk.Toplevel()

    janela_lista.title("Leads cadastrados")

    janela_lista.geometry("400x300")

    caixa_texto = tk.Text(janela_lista)

    caixa_texto.pack()

    leads = pegar_leads()


    for numero, lead in enumerate(leads, start=1):
        texto = (
            f"LEAD {numero}\n"
            f"================\n"
            f"Nome: {lead['nome']}\n"
            f"Telefone: {lead['telefone']}\n"
            f"E-mail: {lead['email']}\n"
            f"Interesse: {lead['interesse']}\n"
            f"Origem: {lead['origem']}\n"
            f"Consultor: {lead['consultor']}\n"
            f"Data de cadastro: {lead['data']}\n"
            f"Observações: {lead['observacao']}\n"
            f"\n"
        )

        caixa_texto.insert(tk.END, texto)
    


botao_listar = tk.Button(
    janela,
    text="Listar Leads",
    command=listar
    )

botao_listar.pack()


#--------------------------------------#


def buscar():
    telefone = campo_busca.get()

    lead = buscar_lead_por_telefone(telefone)

    global lead_selecionado

    lead_selecionado = lead


    if lead is not None:
        campo_nome.delete(0, tk.END)
        campo_nome.insert(0, lead["nome"])

        campo_telefone.delete(0, tk.END)
        campo_telefone.insert(0, lead["telefone"])

        campo_email.delete(0, tk.END)
        campo_email.insert(0, lead["email"])

        campo_interesse.delete(0, tk.END)
        campo_interesse.insert(0, lead["interesse"])

        campo_origem.delete(0, tk.END)
        campo_origem.insert(0, lead["origem"])

        campo_consultor.delete(0, tk.END)
        campo_consultor.insert(0, lead["consultor"])

        campo_observacao.delete(0, tk.END)
        campo_observacao.insert(0, lead["observacao"])

    else:
        messagebox.showwarning(
            "Não encontrado",
            "Nenhum lead encontrado com esse telefone."
    )

botao_buscar = tk.Button(
    janela,
    text="Buscar",
    command=buscar
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