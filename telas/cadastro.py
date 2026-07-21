import tkinter as tk
from tkinter import (
    ttk,
    messagebox,
)

from componentes.campos import (
    criar_campos,
    OPCAO_EMAIL_NAO_INFORMADO,
)

from servicos.leads import (
    cadastrar_lead,
)


def abrir_cadastro():
    janela_cadastro = tk.Toplevel()

    janela_cadastro.title(
        "Cadastrar Lead"
    )

    janela_cadastro.geometry(
        "500x900"
    )

    janela_cadastro.resizable(
        False,
        False
    )

    campos = criar_campos(
        janela_cadastro
    )

    def limpar_campos():
        for chave, campo in (
            campos.items()
        ):
            if isinstance(
                campo,
                tk.Text
            ):
                campo.delete(
                    "1.0",
                    tk.END
                )

            elif isinstance(
                campo,
                ttk.Combobox
            ):
                if chave == "unidade":
                    campo.set("")

                elif chave == "status":
                    campo.set(
                        "EM ANDAMENTO"
                    )

                elif chave == "email":
                    campo.set(
                        OPCAO_EMAIL_NAO_INFORMADO
                    )

                elif chave == "aplicacao":
                    campo.set(
                        "S, F, DTF, DTG E UV"
                    )

                else:
                    campo.set("")

            else:
                campo.delete(
                    0,
                    tk.END
                )

    def salvar():
        dados = {}

        for chave, campo in (
            campos.items()
        ):
            if isinstance(
                campo,
                tk.Text
            ):
                dados[chave] = (
                    campo.get(
                        "1.0",
                        tk.END
                    ).strip()
                )

            else:
                dados[chave] = (
                    campo.get().strip()
                )

        if not dados["nome"]:
            messagebox.showwarning(
                "Campo obrigatório",
                "Informe o nome do lead.",
                parent=janela_cadastro
            )

            campos[
                "nome"
            ].focus_set()

            return

        if not dados["telefone"]:
            messagebox.showwarning(
                "Campo obrigatório",
                "Informe o telefone do lead.",
                parent=janela_cadastro
            )

            campos[
                "telefone"
            ].focus_set()

            return

        if not dados["produto"]:
            messagebox.showwarning(
                "Campo obrigatório",
                "Informe o produto.",
                parent=janela_cadastro
            )

            campos[
                "produto"
            ].focus_set()

            return

        try:
            cadastrar_lead(
                dados
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao cadastrar",
                (
                    "Não foi possível cadastrar "
                    "o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_cadastro
            )

            return

        messagebox.showinfo(
            "Sucesso",
            (
                "Lead cadastrado "
                "com sucesso!"
            ),
            parent=janela_cadastro
        )

        limpar_campos()

        campos[
            "proximo_contato"
        ].focus_set()

    ttk.Button(
        janela_cadastro,
        text="Cadastrar Lead",
        command=salvar
    ).pack(
        pady=15
    )

    janela_cadastro.bind(
        "<Return>",
        lambda evento: salvar()
    )

    campos[
        "proximo_contato"
    ].focus_set()