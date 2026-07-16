import tkinter as tk
from tkinter import messagebox


from servicos.leads import (
    buscar_lead,
    atualizar_lead,
    excluir_lead
)

from servicos.leads import excluir_lead


def abrir_busca():

    global lead_encontrado
    lead_encontrado = None

    janela_busca = tk.Toplevel()

    janela_busca.title("Buscar Lead")
    janela_busca.geometry("500x600")


    tk.Label(
        janela_busca,
        text="Digite o telefone:"
    ).pack()


    campo_telefone = tk.Entry(janela_busca)
    campo_telefone.pack()


    resultado = tk.Text(
        janela_busca,
        height=15,
        width=40
        )

    resultado.pack(
        pady=10
    )


    def buscar():

        telefone = campo_telefone.get()

        global lead_encontrado
        lead_encontrado = buscar_lead(telefone)


        resultado.delete(
            1.0,
            tk.END
        )


        if lead_encontrado:

            texto = (
                f"Nome: {lead_encontrado['nome']}\n"
                f"Telefone: {lead_encontrado['telefone']}\n"
                f"E-mail: {lead_encontrado['email']}\n"
                f"Interesse: {lead_encontrado['interesse']}\n"
                f"Origem: {lead_encontrado['origem']}\n"
                f"Consultor: {lead_encontrado['consultor']}\n"
                f"Data cadastro: {lead_encontrado.get('data','')}\n"
                f"Observação: {lead_encontrado['observacao']}\n"
                f"Status: {lead_encontrado.get('status','Novo')}\n"
                f"Prioridade: {lead_encontrado.get('prioridade','Morno')}\n"
                f"Próximo contato: {lead_encontrado.get('proximo_contato','')}\n"
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
        pady=5
        )


    def editar():

        if lead_encontrado:

            janela_editar = tk.Toplevel()

            janela_editar.title("Editar Lead")
            janela_editar.geometry("350x550")


            campos_edicao = {}


            for campo in [
                "nome",
                "telefone",
                "email",
                "interesse",
                "origem",
                "consultor",
                "observacao",
                "status",
                "prioridade",
                "proximo_contato"
            ]:

                tk.Label(
                    janela_editar,
                    text=campo.capitalize()
                ).pack()

                entrada = tk.Entry(janela_editar)

                entrada.insert(
                    0,
                    lead_encontrado[campo]
                )

                entrada.pack()

                campos_edicao[campo] = entrada


            def salvar_edicao():

                for campo in campos_edicao:

                    lead_encontrado[campo] = campos_edicao[campo].get()


                atualizar_lead(lead_encontrado)


                messagebox.showinfo(
                    "Sucesso",
                    "Lead atualizado!"
                )


                janela_editar.destroy()


            tk.Button(
                janela_editar,
                text="Salvar Alterações",
                command=salvar_edicao
            ).pack(pady=10)

        else:

            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro"
            )

    botao_editar = tk.Button(
        janela_busca,
        text="Editar Lead",
        command=editar
    )

    botao_editar.pack(pady=5)


    botao_excluir = tk.Button(
        janela_busca,
        text="Excluir Lead",
        command=excluir
        )

    botao_excluir.pack(pady=5)



def excluir():

    if lead_encontrado:

        excluir_lead(lead_encontrado)

        messagebox.showinfo(
            "Sucesso",
            "Lead excluído com sucesso!"
        )

    else:

        messagebox.showwarning(
            "Atenção",
            "Nenhum lead selecionado."
        )


    