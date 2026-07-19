import tkinter as tk
from tkinter import ttk, messagebox

from componentes.campos import (
    mascara_telefone,
    inserir_quebra_linha,
)

from componentes.acoes_lead import (
    copiar_resumo,
    abrir_whatsapp,
)

from servicos.leads import (
    buscar_lead,
    atualizar_lead,
    excluir_lead,
)

from servicos.backup import criar_backup


STATUS = [
    "EM ANDAMENTO",
    "NEGOCIAÇÃO",
    "DECLINADO",
    "CONQUISTADO - SUPRIM",
    "CONQUISTADO - EQUIP",
    "FUTURA",
    "CLIENTE ATIVO",
]


APLICACOES = [
    "S, F, DTF, DTG E UV",
    "OUTROS",
]


def abrir_busca():
    lead_encontrado = None

    janela_busca = tk.Toplevel()
    janela_busca.title("Buscar Lead")
    janela_busca.geometry("720x700")
    janela_busca.resizable(False, False)

    container = ttk.Frame(
        janela_busca,
        padding=20
    )
    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Buscar Lead",
        font=("Arial", 20, "bold")
    ).pack(pady=(0, 20))

    frame_busca = ttk.Frame(container)
    frame_busca.pack(fill="x")

    ttk.Label(
        frame_busca,
        text="Telefone:"
    ).pack(
        side="left",
        padx=(0, 8)
    )

    campo_telefone = ttk.Entry(
        frame_busca,
        width=30
    )
    campo_telefone.pack(
        side="left",
        padx=(0, 8)
    )

    campo_telefone.bind(
        "<KeyRelease>",
        mascara_telefone
    )

    resultado = tk.Text(
        container,
        height=25,
        width=80,
        wrap="word"
    )
    resultado.pack(
        fill="both",
        expand=True,
        pady=20
    )
    resultado.configure(state="disabled")

    frame_botoes = ttk.Frame(container)
    frame_botoes.pack()

    def limpar_resultado():
        resultado.configure(state="normal")
        resultado.delete("1.0", tk.END)
        resultado.configure(state="disabled")

    def habilitar_acoes():
        botao_editar.configure(state="normal")
        botao_excluir.configure(state="normal")
        botao_copiar.configure(state="normal")
        botao_whatsapp.configure(state="normal")

    def desabilitar_acoes():
        botao_editar.configure(state="disabled")
        botao_excluir.configure(state="disabled")
        botao_copiar.configure(state="disabled")
        botao_whatsapp.configure(state="disabled")

    def mostrar_lead(lead):
        limpar_resultado()

        texto = (
            f"Data de Cadastro: "
            f"{lead.get('data_cadastro', '')}\n\n"

            f"Próximo Contato: "
            f"{lead.get('proximo_contato', '')}\n"

            f"Última Interação: "
            f"{lead.get('ultima_interacao', '')}\n"

            f"Status: "
            f"{lead.get('status', '')}\n\n"

            f"Telefone: "
            f"{lead.get('telefone', '')}\n"

            f"Nome: "
            f"{lead.get('nome', '')}\n"

            f"Produto: "
            f"{lead.get('produto', '')}\n"

            f"Cidade / UF: "
            f"{lead.get('cidade_uf', '')}\n"

            f"E-mail: "
            f"{lead.get('email', '')}\n"

            f"Aplicação: "
            f"{lead.get('aplicacao', '')}\n"

            f"Origem: "
            f"{lead.get('origem', '')}\n"

            f"Consultor: "
            f"{lead.get('consultor', '')}\n"

            f"Observação: "
            f"{lead.get('observacao', '')}\n\n"

            f"Resumo:\n"
            f"{lead.get('resumo', '')}\n\n"

            f"Nome no WhatsApp:\n"
            f"{lead.get('whatsapp', '')}"
        )

        resultado.configure(state="normal")
        resultado.insert("1.0", texto)
        resultado.configure(state="disabled")

    def copiar_resumo_lead():
        if lead_encontrado is None:
            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro.",
                parent=janela_busca
            )
            return

        try:
            copiar_resumo(
                janela_busca,
                lead_encontrado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível copiar o resumo."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        messagebox.showinfo(
            "Resumo copiado",
            "O resumo do lead foi copiado.",
            parent=janela_busca
        )

    def abrir_whatsapp_lead():
        if lead_encontrado is None:
            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro.",
                parent=janela_busca
            )
            return

        try:
            abrir_whatsapp(
                lead_encontrado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir WhatsApp",
                (
                    "Não foi possível abrir o WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )

    def buscar():
        nonlocal lead_encontrado

        telefone = campo_telefone.get().strip()

        if not telefone:
            messagebox.showwarning(
                "Campo obrigatório",
                "Digite o telefone do lead.",
                parent=janela_busca
            )
            campo_telefone.focus_set()
            return

        try:
            lead_encontrado = buscar_lead(
                telefone
            )

        except Exception as erro:
            lead_encontrado = None

            limpar_resultado()
            desabilitar_acoes()

            messagebox.showerror(
                "Erro na busca",
                (
                    "Não foi possível buscar o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        if lead_encontrado is None:
            limpar_resultado()
            desabilitar_acoes()

            messagebox.showwarning(
                "Lead não encontrado",
                (
                    "Nenhum lead foi encontrado "
                    "com esse telefone."
                ),
                parent=janela_busca
            )
            return

        mostrar_lead(
            lead_encontrado
        )

        habilitar_acoes()

    botao_buscar = ttk.Button(
        frame_busca,
        text="Buscar",
        command=buscar
    )
    botao_buscar.pack(side="left")

    def editar():
        if lead_encontrado is None:
            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro.",
                parent=janela_busca
            )
            return

        janela_editar = tk.Toplevel(
            janela_busca
        )
        janela_editar.title("Editar Lead")
        janela_editar.geometry("520x830")
        janela_editar.resizable(
            False,
            False
        )
        janela_editar.transient(
            janela_busca
        )
        janela_editar.grab_set()

        container_edicao = ttk.Frame(
            janela_editar,
            padding=20
        )
        container_edicao.pack(
            expand=True,
            fill="both"
        )

        ttk.Label(
            container_edicao,
            text="Editar Lead",
            font=("Arial", 18, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 15)
        )

        ttk.Label(
            container_edicao,
            text="Data de Cadastro:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        ttk.Label(
            container_edicao,
            text=lead_encontrado.get(
                "data_cadastro",
                ""
            )
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        campos_edicao = {}

        campos = [
            (
                "Próximo Contato",
                "proximo_contato"
            ),
            (
                "Última Interação",
                "ultima_interacao"
            ),
            (
                "Status",
                "status"
            ),
            (
                "Telefone",
                "telefone"
            ),
            (
                "Nome",
                "nome"
            ),
            (
                "Produto",
                "produto"
            ),
            (
                "Cidade / UF",
                "cidade_uf"
            ),
            (
                "E-mail",
                "email"
            ),
            (
                "Aplicação",
                "aplicacao"
            ),
            (
                "Origem",
                "origem"
            ),
            (
                "Consultor",
                "consultor"
            ),
            (
                "Observação",
                "observacao"
            ),
        ]

        for linha, (texto, chave) in enumerate(
            campos,
            start=2
        ):
            ttk.Label(
                container_edicao,
                text=f"{texto}:"
            ).grid(
                row=linha,
                column=0,
                sticky="w",
                padx=5,
                pady=5
            )

            if chave == "status":
                campo = ttk.Combobox(
                    container_edicao,
                    values=STATUS,
                    state="readonly",
                    width=35
                )

                campo.set(
                    lead_encontrado.get(
                        chave,
                        "EM ANDAMENTO"
                    )
                )

            elif chave == "aplicacao":
                campo = ttk.Combobox(
                    container_edicao,
                    values=APLICACOES,
                    state="readonly",
                    width=35
                )

                campo.set(
                    lead_encontrado.get(
                        chave,
                        APLICACOES[0]
                    )
                )

            elif chave == "observacao":
                campo = tk.Text(
                    container_edicao,
                    width=38,
                    height=4,
                    wrap="word"
                )

                campo.insert(
                    "1.0",
                    lead_encontrado.get(
                        chave,
                        ""
                    )
                )

                campo.bind(
                    "<Shift-Return>",
                    inserir_quebra_linha
                )

                campo.insert(
                    "1.0",
                    lead_encontrado.get(
                        chave,
                        ""
                    )
                )

            else:
                campo = ttk.Entry(
                    container_edicao,
                    width=38
                )

                campo.insert(
                    0,
                    lead_encontrado.get(
                        chave,
                        ""
                    )
                )

            campo.grid(
                row=linha,
                column=1,
                sticky="ew",
                padx=5,
                pady=5
            )

            if chave == "telefone":
                campo.bind(
                    "<KeyRelease>",
                    mascara_telefone
                )

            campos_edicao[chave] = campo

        container_edicao.columnconfigure(
            1,
            weight=1
        )

        def salvar_edicao():
            nonlocal lead_encontrado

            dados_atualizados = (
                lead_encontrado.copy()
            )

            for chave, campo in campos_edicao.items():

                if isinstance(campo, tk.Text):
                    dados_atualizados[chave] = campo.get(
                        "1.0",
                        tk.END
                    ).strip()

                else:
                    dados_atualizados[chave] = (
                        campo.get().strip()
                    )

            if not dados_atualizados["nome"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o nome do lead.",
                    parent=janela_editar
                )

                campos_edicao[
                    "nome"
                ].focus_set()

                return

            if not dados_atualizados["telefone"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o telefone do lead.",
                    parent=janela_editar
                )

                campos_edicao[
                    "telefone"
                ].focus_set()

                return

            if not dados_atualizados["produto"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o produto.",
                    parent=janela_editar
                )

                campos_edicao[
                    "produto"
                ].focus_set()

                return

            try:
                atualizar_lead(
                    dados_atualizados
                )

                lead_atualizado = buscar_lead(
                    dados_atualizados[
                        "telefone"
                    ]
                )

                if lead_atualizado is not None:
                    lead_encontrado = (
                        lead_atualizado
                    )
                else:
                    lead_encontrado = (
                        dados_atualizados
                    )

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao atualizar",
                    (
                        "Não foi possível atualizar "
                        "o lead."
                        f"\n\n{erro}"
                    ),
                    parent=janela_editar
                )
                return

            mostrar_lead(
                lead_encontrado
            )

            campo_telefone.delete(
                0,
                tk.END
            )

            campo_telefone.insert(
                0,
                lead_encontrado.get(
                    "telefone",
                    ""
                )
            )

            habilitar_acoes()

            messagebox.showinfo(
                "Sucesso",
                "Lead atualizado com sucesso!",
                parent=janela_editar
            )

            janela_editar.destroy()

        ttk.Button(
            container_edicao,
            text="Salvar Alterações",
            command=salvar_edicao
        ).grid(
            row=len(campos) + 2,
            column=0,
            columnspan=2,
            pady=20
        )

    def excluir():
        nonlocal lead_encontrado

        if lead_encontrado is None:
            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro.",
                parent=janela_busca
            )
            return

        confirmacao = messagebox.askyesno(
            "Excluir Lead",
            (
                "Deseja realmente excluir "
                "este lead?\n\n"

                f"Nome: "
                f"{lead_encontrado.get('nome', '')}\n"

                f"Telefone: "
                f"{lead_encontrado.get('telefone', '')}"
            ),
            parent=janela_busca
        )

        if not confirmacao:
            return

        try:
            criar_backup()

            excluir_lead(
                lead_encontrado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                (
                    "Não foi possível criar o backup "
                    "ou excluir o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                (
                    "Não foi possível excluir o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        lead_encontrado = None

        limpar_resultado()
        desabilitar_acoes()

        campo_telefone.delete(
            0,
            tk.END
        )
        campo_telefone.focus_set()

        messagebox.showinfo(
            "Sucesso",
            "Lead excluído com sucesso!",
            parent=janela_busca
        )

    botao_editar = ttk.Button(
        frame_botoes,
        text="Editar Lead",
        command=editar,
        state="disabled"
    )
    botao_editar.pack(
        side="left",
        padx=5
    )

    botao_excluir = ttk.Button(
        frame_botoes,
        text="Excluir Lead",
        command=excluir,
        state="disabled"
    )
    botao_excluir.pack(
        side="left",
        padx=5
    )

    botao_copiar = ttk.Button(
        frame_botoes,
        text="Copiar Resumo",
        command=copiar_resumo_lead,
        state="disabled"
    )
    botao_copiar.pack(
        side="left",
        padx=5
    )

    botao_whatsapp = ttk.Button(
        frame_botoes,
        text="Abrir WhatsApp",
        command=abrir_whatsapp_lead,
        state="disabled"
    )
    botao_whatsapp.pack(
        side="left",
        padx=5
    )

    janela_busca.bind(
        "<Return>",
        lambda evento: buscar()
    )

    campo_telefone.focus_set()