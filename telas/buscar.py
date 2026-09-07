import tkinter as tk
from tkinter import ttk, messagebox

from componentes.campos import (
    mascara_telefone,
    inserir_quebra_linha,
    STATUS,
    APLICACOES,
    UNIDADES,
    OPCOES_EMAIL,
    OPCAO_EMAIL_MANUAL,
    OPCAO_EMAIL_NAO_INFORMADO,
)

from componentes.acoes_lead import (
    copiar_resumo,
    copiar_whatsapp,
    abrir_whatsapp,
)
from componentes.detalhes_lead import PainelDetalhesLead

from servicos.leads import (
    buscar_lead,
    atualizar_lead,
    excluir_lead,
)

from servicos.backup import criar_backup


def mascara_data(evento):
    campo = evento.widget

    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:8]

    texto = numeros

    if len(numeros) > 2:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:]}"
        )

    if len(numeros) > 4:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:4]}/"
            f"{numeros[4:]}"
        )

    campo.delete(
        0,
        tk.END
    )

    campo.insert(
        0,
        texto
    )


def mascara_data_hora(evento):
    campo = evento.widget

    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:12]

    texto = numeros

    if len(numeros) > 2:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:]}"
        )

    if len(numeros) > 4:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:4]}/"
            f"{numeros[4:]}"
        )

    if len(numeros) > 8:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:4]}/"
            f"{numeros[4:8]} "
            f"{numeros[8:]}"
        )

    if len(numeros) > 10:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:4]}/"
            f"{numeros[4:8]} "
            f"{numeros[8:10]}:"
            f"{numeros[10:]}"
        )

    campo.delete(
        0,
        tk.END
    )

    campo.insert(
        0,
        texto
    )


def abrir_busca():
    lead_encontrado = None

    janela_busca = tk.Toplevel()
    janela_busca.title(
        "Buscar Lead"
    )
    janela_busca.geometry(
        "1100x780"
    )
    janela_busca.minsize(
        900,
        650
    )

    try:
        janela_busca.state(
            "zoomed"
        )
    except tk.TclError:
        pass

    container = ttk.Frame(
        janela_busca,
        padding=10
    )

    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Buscar Lead",
        font=(
            "Arial",
            18,
            "bold"
        )
    ).pack(
        pady=(0, 10)
    )

    frame_busca = ttk.LabelFrame(
        container,
        text="Localizar lead",
        padding=10
    )

    frame_busca.pack(
        fill="x",
        pady=(0, 10)
    )

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

    frame_resultado = ttk.LabelFrame(
        container,
        text="Dados do lead encontrado",
        padding=8
    )

    frame_resultado.pack(
        fill="both",
        expand=True
    )

    painel_detalhes = PainelDetalhesLead(
        frame_resultado
    )

    painel_detalhes.pack(
        fill="both",
        expand=True,
        pady=0,
    )

    frame_botoes = ttk.Frame(
        container
    )

    frame_botoes.pack(
        pady=(12, 0)
    )

    def limpar_resultado():
        painel_detalhes.limpar()

    def habilitar_acoes():
        botao_editar.configure(
            state="normal"
        )

        botao_excluir.configure(
            state="normal"
        )

        botao_copiar_resumo.configure(
            state="normal"
        )

        botao_copiar_whatsapp.configure(
            state="normal"
        )

        botao_whatsapp.configure(
            state="normal"
        )

    def desabilitar_acoes():
        botao_editar.configure(
            state="disabled"
        )

        botao_excluir.configure(
            state="disabled"
        )

        botao_copiar_resumo.configure(
            state="disabled"
        )

        botao_copiar_whatsapp.configure(
            state="disabled"
        )

        botao_whatsapp.configure(
            state="disabled"
        )

    def mostrar_lead(lead):
        painel_detalhes.exibir(lead)

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
                    "Não foi possível copiar "
                    "o resumo."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        messagebox.showinfo(
            "Resumo copiado",
            (
                "O resumo do lead "
                "foi copiado."
            ),
            parent=janela_busca
        )

    def copiar_whatsapp_lead():
        if lead_encontrado is None:
            messagebox.showwarning(
                "Atenção",
                "Busque um lead primeiro.",
                parent=janela_busca
            )
            return

        try:
            copiar_whatsapp(
                janela_busca,
                lead_encontrado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível copiar "
                    "o nome do WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )
            return

        messagebox.showinfo(
            "WhatsApp copiado",
            (
                "O nome para o WhatsApp "
                "foi copiado."
            ),
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
                    "Não foi possível abrir "
                    "o WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela_busca
            )

    def buscar():
        nonlocal lead_encontrado

        telefone = (
            campo_telefone
            .get()
            .strip()
        )

        if not telefone:
            messagebox.showwarning(
                "Campo obrigatório",
                "Digite o telefone do lead.",
                parent=janela_busca
            )

            campo_telefone.focus_set()
            return

        try:
            lead_encontrado = (
                buscar_lead(
                    telefone
                )
            )

        except Exception as erro:
            lead_encontrado = None

            limpar_resultado()
            desabilitar_acoes()

            messagebox.showerror(
                "Erro na busca",
                (
                    "Não foi possível buscar "
                    "o lead."
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

    botao_buscar.pack(
        side="left"
    )

    def editar():
        nonlocal lead_encontrado

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

        janela_editar.title(
            "Editar Lead"
        )

        janela_editar.geometry(
            "540x930"
        )

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
            font=(
                "Arial",
                18,
                "bold"
            )
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
                "Unidade",
                "unidade"
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

        for linha, (
            texto,
            chave
        ) in enumerate(
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

            valor_atual = (
                lead_encontrado.get(
                    chave,
                    ""
                )
            )

            if chave == "unidade":
                campo = ttk.Combobox(
                    container_edicao,
                    values=UNIDADES,
                    state="readonly",
                    width=35
                )

                campo.set(
                    valor_atual
                )

            elif chave == "status":
                campo = ttk.Combobox(
                    container_edicao,
                    values=STATUS,
                    state="readonly",
                    width=35
                )

                campo.set(
                    valor_atual
                    or "EM ANDAMENTO"
                )

            elif chave == "email":
                campo = ttk.Combobox(
                    container_edicao,
                    values=OPCOES_EMAIL,
                    state="normal",
                    width=35
                )

                campo.set(
                    valor_atual
                    or OPCAO_EMAIL_NAO_INFORMADO
                )

            elif chave == "aplicacao":
                campo = ttk.Combobox(
                    container_edicao,
                    values=APLICACOES,
                    state="readonly",
                    width=35
                )

                campo.set(
                    valor_atual
                    or APLICACOES[0]
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
                    valor_atual
                )

                campo.bind(
                    "<Shift-Return>",
                    inserir_quebra_linha
                )

            else:
                campo = ttk.Entry(
                    container_edicao,
                    width=38
                )

                campo.insert(
                    0,
                    valor_atual
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

            elif chave == "proximo_contato":
                campo.bind(
                    "<KeyRelease>",
                    mascara_data
                )

            elif chave == "ultima_interacao":
                campo.bind(
                    "<KeyRelease>",
                    mascara_data_hora
                )

            campos_edicao[
                chave
            ] = campo

        def verificar_status(
            evento=None
        ):
            status = (
                campos_edicao[
                    "status"
                ]
                .get()
                .strip()
                .upper()
            )

            if status == "DECLINADO":
                campos_edicao[
                    "proximo_contato"
                ].delete(
                    0,
                    tk.END
                )

        def selecionar_email(
            evento=None
        ):
            opcao = (
                campos_edicao[
                    "email"
                ]
                .get()
                .strip()
            )

            if (
                opcao
                == OPCAO_EMAIL_MANUAL
            ):
                campos_edicao[
                    "email"
                ].set("")

                campos_edicao[
                    "email"
                ].focus_set()

                campos_edicao[
                    "email"
                ].icursor(
                    tk.END
                )

            elif (
                opcao
                == OPCAO_EMAIL_NAO_INFORMADO
            ):
                campos_edicao[
                    "email"
                ].set(
                    OPCAO_EMAIL_NAO_INFORMADO
                )

        campos_edicao[
            "status"
        ].bind(
            "<<ComboboxSelected>>",
            verificar_status
        )

        campos_edicao[
            "email"
        ].bind(
            "<<ComboboxSelected>>",
            selecionar_email
        )

        container_edicao.columnconfigure(
            1,
            weight=1
        )

        def salvar_edicao():
            nonlocal lead_encontrado

            dados_atualizados = (
                lead_encontrado.copy()
            )

            for chave, campo in (
                campos_edicao.items()
            ):
                if isinstance(
                    campo,
                    tk.Text
                ):
                    dados_atualizados[
                        chave
                    ] = campo.get(
                        "1.0",
                        tk.END
                    ).strip()

                else:
                    dados_atualizados[
                        chave
                    ] = (
                        campo
                        .get()
                        .strip()
                    )

            if not dados_atualizados[
                "nome"
            ]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o nome do lead.",
                    parent=janela_editar
                )

                campos_edicao[
                    "nome"
                ].focus_set()

                return

            if not dados_atualizados[
                "telefone"
            ]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o telefone do lead.",
                    parent=janela_editar
                )

                campos_edicao[
                    "telefone"
                ].focus_set()

                return

            if not dados_atualizados[
                "produto"
            ]:
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
                lead_atualizado = (
                    atualizar_lead(
                        dados_atualizados
                    )
                )

                if lead_atualizado:
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

            mostrar_lead(
                lead_encontrado
            )

            janela_editar.destroy()

            messagebox.showinfo(
                "Sucesso",
                (
                    "Lead atualizado "
                    "com sucesso!"
                ),
                parent=janela_busca
            )

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

        confirmacao = (
            messagebox.askyesno(
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
            (
                "Lead excluído "
                "com sucesso!"
            ),
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
        padx=4
    )

    botao_excluir = ttk.Button(
        frame_botoes,
        text="Excluir Lead",
        command=excluir,
        state="disabled"
    )

    botao_excluir.pack(
        side="left",
        padx=4
    )

    botao_copiar_resumo = ttk.Button(
        frame_botoes,
        text="Copiar Resumo",
        command=copiar_resumo_lead,
        state="disabled"
    )

    botao_copiar_resumo.pack(
        side="left",
        padx=4
    )

    botao_copiar_whatsapp = ttk.Button(
        frame_botoes,
        text="Copiar WhatsApp",
        command=copiar_whatsapp_lead,
        state="disabled"
    )

    botao_copiar_whatsapp.pack(
        side="left",
        padx=4
    )

    botao_whatsapp = ttk.Button(
        frame_botoes,
        text="Abrir WhatsApp",
        command=abrir_whatsapp_lead,
        state="disabled"
    )

    botao_whatsapp.pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_botoes,
        text="Fechar",
        command=janela_busca.destroy
    ).pack(
        side="left",
        padx=4
    )

    janela_busca.bind(
        "<Return>",
        lambda evento: buscar()
    )

    campo_telefone.focus_set()
