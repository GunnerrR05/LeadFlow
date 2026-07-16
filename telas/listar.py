import tkinter as tk
from tkinter import ttk, messagebox

from servicos.leads import listar_leads, excluir_lead


def abrir_lista():

    janela_lista = tk.Toplevel()

    janela_lista.title("Leads cadastrados")
    janela_lista.geometry("1000x400")

    janela_lista.lead_selecionado = None

    tabela = ttk.Treeview(
        janela_lista,
        columns=(
            "nome",
            "telefone",
            "email",
            "interesse",
            "origem",
            "consultor",
            "observacao"
        ),
        show="headings"
    )


    tabela.heading("nome", text="Nome")
    tabela.heading("telefone", text="Telefone")
    tabela.heading("email", text="E-mail")
    tabela.heading("interesse", text="Interesse")
    tabela.heading("origem", text="Origem")
    tabela.heading("consultor", text="Consultor")
    tabela.heading("observacao", text="Observação")


    tabela.column("nome", width=120)
    tabela.column("telefone", width=100)
    tabela.column("email", width=150)
    tabela.column("interesse", width=120)
    tabela.column("origem", width=100)
    tabela.column("consultor", width=120)
    tabela.column("observacao", width=200)


    tabela.pack(
        expand=True,
        fill="both"
    )

    def carregar_tabela():
    
        for item in tabela.get_children():
            tabela.delete(item)

        leads = listar_leads()

        for lead in leads:
            tabela.insert(
                "",
                tk.END,
                values=(
                    lead["nome"],
                    lead["telefone"],
                    lead["email"],
                    lead["interesse"],
                    lead["origem"],
                    lead["consultor"],
                    lead["observacao"]
                )
            )

    carregar_tabela()



    
    
    def selecionar_lead(event):

        item = tabela.selection()

        if item:
            item = item[0]

            valores = tabela.item(item)["values"]

            janela_lista.lead_selecionado = {
                "linha": tabela.index(item) + 2,
                "nome": valores[0],
                "telefone": valores[1],
                "email": valores[2],
                "interesse": valores[3],
                "origem": valores[4],
                "consultor": valores[5],
                "observacao": valores[6]
            }



    
    tabela.bind(
        "<<TreeviewSelect>>", 
        selecionar_lead
    )

    
    def editar():

        if janela_lista.lead_selecionado:

            janela_editar = tk.Toplevel()
            janela_editar.title("Editar Lead")
            janela_editar.geometry("400x400")

            campos = {}

            for campo, valor in janela_lista.lead_selecionado.items():

                if campo != "linha":

                    tk.Label(
                        janela_editar,
                        text=campo.capitalize()
                    ).pack()

                    entrada = tk.Entry(janela_editar)
                    entrada.insert(
                        0,
                        valor
                    )
                    entrada.pack()

                    campos[campo] = entrada


            def salvar():

                lead_atualizado = janela_lista.lead_selecionado.copy()

                for campo in campos:
                    lead_atualizado[campo] = campos[campo].get()

                from servicos.leads import atualizar_lead

                atualizar_lead(lead_atualizado)

                messagebox.showinfo(
                    "Sucesso",
                    "Lead atualizado!"
                )

                carregar_tabela()
                janela_editar.destroy()


            tk.Button(
                janela_editar,
                text="Salvar Alterações",
                command=salvar
            ).pack(pady=10)


        else:

            messagebox.showwarning(
                "Atenção",
                "Selecione um lead primeiro."
            )
    
    
    def excluir():

        if janela_lista.lead_selecionado:

            excluir_lead(
                janela_lista.lead_selecionado
            )

            messagebox.showinfo(
                "Sucesso",
                "Lead excluído!"
            )

            carregar_tabela()            


        else:
            messagebox.showwarning(
                "Atenção",
                "Selecione um lead primeiro."
            )


    botao_excluir = tk.Button(
        janela_lista,
        text="Excluir Lead",
        command=lambda: excluir()
    )

    botao_excluir.pack(pady=5)


    botao_editar = tk.Button(
        janela_lista,
        text="Editar Lead",
        command=editar
    )

    botao_editar.pack(pady=5)