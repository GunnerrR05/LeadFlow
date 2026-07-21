import tkinter as tk
from tkinter import (
    ttk,
    messagebox,
)
from datetime import (
    datetime,
    timedelta,
)

from servicos.leads import (
    obter_followups,
    atualizar_lead,
)

from componentes.acoes_lead import (
    copiar_resumo,
    copiar_whatsapp,
    abrir_whatsapp,
)


STATUS = [
    "EM ANDAMENTO",
    "NEGOCIAÇÃO",
    "DECLINADO",
    "CONQUISTADO - SUPRIM",
    "CONQUISTADO - EQUIP",
    "FUTURA",
    "CLIENTE ATIVO",
]


COLUNAS = (
    "prazo",
    "proximo_contato",
    "unidade",
    "status",
    "nome",
    "telefone",
    "produto",
    "cidade_uf",
    "consultor",
)


TITULOS = {
    "prazo": "Prazo",
    "proximo_contato": "Próximo Contato",
    "unidade": "Unidade",
    "status": "Status",
    "nome": "Nome",
    "telefone": "Telefone",
    "produto": "Produto",
    "cidade_uf": "Cidade / UF",
    "consultor": "Consultor",
}


LARGURAS = {
    "prazo": 130,
    "proximo_contato": 140,
    "unidade": 150,
    "status": 210,
    "nome": 190,
    "telefone": 140,
    "produto": 190,
    "cidade_uf": 150,
    "consultor": 150,
}


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


def calcular_prazo(valor):
    texto = str(
        valor
    ).strip()

    if not texto:
        return "Sem data"

    formatos = (
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
    )

    data_contato = None

    for formato in formatos:
        try:
            data_contato = (
                datetime.strptime(
                    texto,
                    formato
                ).date()
            )

            break

        except ValueError:
            continue

    if data_contato is None:
        return "Data inválida"

    hoje = (
        datetime.now().date()
    )

    diferenca = (
        data_contato - hoje
    ).days

    if diferenca < 0:
        quantidade = abs(
            diferenca
        )

        if quantidade == 1:
            return "1 dia atrasado"

        return (
            f"{quantidade} "
            "dias atrasado"
        )

    if diferenca == 0:
        return "Hoje"

    if diferenca == 1:
        return "Amanhã"

    return f"Em {diferenca} dias"


def abrir_followups():
    lead_selecionado = None
    leads_por_item = {}

    janela = tk.Toplevel()
    janela.title(
        "Follow-ups"
    )
    janela.geometry(
        "1350x720"
    )
    janela.minsize(
        1050,
        620
    )

    try:
        janela.state(
            "zoomed"
        )

    except tk.TclError:
        pass

    container = ttk.Frame(
        janela,
        padding=15
    )

    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Follow-ups",
        font=(
            "Arial",
            22,
            "bold"
        )
    ).pack(
        pady=(0, 5)
    )

    label_resumo = ttk.Label(
        container,
        text="",
        font=(
            "Arial",
            11
        )
    )

    label_resumo.pack(
        pady=(0, 15)
    )

    abas = ttk.Notebook(
        container
    )

    abas.pack(
        expand=True,
        fill="both"
    )

    configuracoes = {
        "atrasados": "Atrasados",
        "hoje": "Hoje",
        "proximos": "Próximos",
        "finalizados": "Finalizado",
        "invalidos": "Data Inválida",
    }

    tags_grupos = {
        "atrasados": "atrasado",
        "hoje": "hoje",
        "proximos": "proximo",
        "finalizados": "finalizado",
        "invalidos": "invalido",
    }

    tabelas = {}
    frames = {}

    for chave, titulo in (
        configuracoes.items()
    ):
        frame = ttk.Frame(
            abas,
            padding=8
        )

        abas.add(
            frame,
            text=titulo
        )

        frame_tabela = ttk.Frame(
            frame
        )

        frame_tabela.pack(
            expand=True,
            fill="both"
        )

        barra_vertical = ttk.Scrollbar(
            frame_tabela,
            orient="vertical"
        )

        barra_horizontal = (
            ttk.Scrollbar(
                frame_tabela,
                orient="horizontal"
            )
        )

        tabela = ttk.Treeview(
            frame_tabela,
            columns=COLUNAS,
            show="headings",
            yscrollcommand=(
                barra_vertical.set
            ),
            xscrollcommand=(
                barra_horizontal.set
            ),
            selectmode="browse"
        )

        barra_vertical.configure(
            command=tabela.yview
        )

        barra_horizontal.configure(
            command=tabela.xview
        )

        tabela.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        frame_tabela.rowconfigure(
            0,
            weight=1
        )

        frame_tabela.columnconfigure(
            0,
            weight=1
        )

        for coluna in COLUNAS:
            tabela.heading(
                coluna,
                text=TITULOS[
                    coluna
                ]
            )

            tabela.column(
                coluna,
                width=LARGURAS[
                    coluna
                ],
                minwidth=90,
                anchor="w",
                stretch=True
            )

        tabela.tag_configure(
            "atrasado",
            background="#FFDADA"
        )

        tabela.tag_configure(
            "hoje",
            background="#FFF2CC"
        )

        tabela.tag_configure(
            "proximo",
            background="#DDF4DD"
        )

        tabela.tag_configure(
            "finalizado",
            background="#E5E5E5"
        )

        tabela.tag_configure(
            "invalido",
            background="#E8DDF5"
        )

        tabelas[chave] = tabela
        frames[chave] = frame

    frame_botoes = ttk.Frame(
        container
    )

    frame_botoes.pack(
        pady=(12, 0)
    )

    botao_registrar = None
    botao_copiar = None
    botao_copiar_whatsapp = None
    botao_whatsapp = None

    def desabilitar_registro():
        if botao_registrar is not None:
            botao_registrar.configure(
                state="disabled"
            )

        if botao_copiar is not None:
            botao_copiar.configure(
                state="disabled"
            )

        if (
            botao_copiar_whatsapp
            is not None
        ):
            botao_copiar_whatsapp.configure(
                state="disabled"
            )

        if botao_whatsapp is not None:
            botao_whatsapp.configure(
                state="disabled"
            )

    def habilitar_registro():
        if botao_registrar is not None:
            botao_registrar.configure(
                state="normal"
            )

        if botao_copiar is not None:
            botao_copiar.configure(
                state="normal"
            )

        if (
            botao_copiar_whatsapp
            is not None
        ):
            botao_copiar_whatsapp.configure(
                state="normal"
            )

        if botao_whatsapp is not None:
            botao_whatsapp.configure(
                state="normal"
            )

    def limpar_selecao():
        nonlocal lead_selecionado

        lead_selecionado = None

        for tabela in (
            tabelas.values()
        ):
            selecao = (
                tabela.selection()
            )

            if selecao:
                tabela.selection_remove(
                    selecao
                )

        desabilitar_registro()

    def selecionar_lead(
        chave_aba
    ):
        nonlocal lead_selecionado

        tabela_atual = (
            tabelas[chave_aba]
        )

        selecao = (
            tabela_atual.selection()
        )

        if not selecao:
            lead_selecionado = None
            desabilitar_registro()
            return

        for (
            outra_chave,
            outra_tabela
        ) in tabelas.items():
            if (
                outra_chave
                == chave_aba
            ):
                continue

            outra_selecao = (
                outra_tabela.selection()
            )

            if outra_selecao:
                outra_tabela.selection_remove(
                    outra_selecao
                )

        item_id = selecao[0]

        lead_selecionado = (
            leads_por_item.get(
                (
                    chave_aba,
                    item_id
                )
            )
        )

        if lead_selecionado is None:
            desabilitar_registro()
            return

        habilitar_registro()

    def carregar():
        nonlocal leads_por_item

        limpar_selecao()

        leads_por_item = {}

        try:
            grupos = (
                obter_followups()
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível "
                    "carregar os follow-ups."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        for (
            chave,
            tabela
        ) in tabelas.items():
            for item in (
                tabela.get_children()
            ):
                tabela.delete(
                    item
                )

            lista_grupo = (
                grupos.get(
                    chave,
                    []
                )
            )

            for indice, lead in enumerate(
                lista_grupo,
                start=1
            ):
                linha = lead.get(
                    "linha"
                )

                if linha is not None:
                    item_id = str(
                        linha
                    )

                else:
                    item_id = (
                        f"{chave}_{indice}"
                    )

                leads_por_item[
                    (
                        chave,
                        item_id
                    )
                ] = lead

                if chave == "finalizados":
                    prazo = "Finalizado"

                else:
                    prazo = calcular_prazo(
                        lead.get(
                            "proximo_contato",
                            ""
                        )
                    )

                tabela.insert(
                    "",
                    tk.END,
                    iid=item_id,
                    tags=(
                        tags_grupos[
                            chave
                        ],
                    ),
                    values=(
                        prazo,
                        lead.get(
                            "proximo_contato",
                            ""
                        ),
                        lead.get(
                            "unidade",
                            ""
                        ),
                        lead.get(
                            "status",
                            ""
                        ),
                        lead.get(
                            "nome",
                            ""
                        ),
                        lead.get(
                            "telefone",
                            ""
                        ),
                        lead.get(
                            "produto",
                            ""
                        ),
                        lead.get(
                            "cidade_uf",
                            ""
                        ),
                        lead.get(
                            "consultor",
                            ""
                        ),
                    )
                )

            abas.tab(
                frames[chave],
                text=(
                    f"{configuracoes[chave]} "
                    f"({len(lista_grupo)})"
                )
            )

        label_resumo.configure(
            text=(
                "Atrasados: "
                f"{len(grupos.get('atrasados', []))}"
                "    |    "
                "Hoje: "
                f"{len(grupos.get('hoje', []))}"
                "    |    "
                "Próximos: "
                f"{len(grupos.get('proximos', []))}"
                "    |    "
                "Finalizados: "
                f"{len(grupos.get('finalizados', []))}"
                "    |    "
                "Datas inválidas: "
                f"{len(grupos.get('invalidos', []))}"
            )
        )

    def copiar_resumo_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela
            )
            return

        try:
            copiar_resumo(
                janela,
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível "
                    "copiar o resumo."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        messagebox.showinfo(
            "Resumo copiado",
            (
                "O resumo do lead "
                "foi copiado."
            ),
            parent=janela
        )

    def copiar_whatsapp_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela
            )
            return

        try:
            copiar_whatsapp(
                janela,
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível "
                    "copiar o nome "
                    "do WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        messagebox.showinfo(
            "WhatsApp copiado",
            (
                "O nome para o WhatsApp "
                "foi copiado."
            ),
            parent=janela
        )

    def abrir_whatsapp_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela
            )
            return

        try:
            abrir_whatsapp(
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir WhatsApp",
                (
                    "Não foi possível "
                    "abrir o WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela
            )

    def abrir_registro_contato():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela
            )
            return

        janela_registro = tk.Toplevel(
            janela
        )

        janela_registro.title(
            "Registrar Contato"
        )

        janela_registro.geometry(
            "720x720"
        )

        janela_registro.minsize(
            650,
            650
        )

        janela_registro.transient(
            janela
        )

        janela_registro.grab_set()

        container_registro = ttk.Frame(
            janela_registro,
            padding=20
        )

        container_registro.pack(
            expand=True,
            fill="both"
        )

        ttk.Label(
            container_registro,
            text="Registrar Contato",
            font=(
                "Arial",
                20,
                "bold"
            )
        ).pack(
            pady=(0, 5)
        )

        ttk.Label(
            container_registro,
            text=(
                f"{lead_selecionado.get('nome', '')}"
                "  |  "
                f"{lead_selecionado.get('telefone', '')}"
                "  |  "
                f"{lead_selecionado.get('unidade', '')}"
            ),
            font=(
                "Arial",
                11
            )
        ).pack(
            pady=(0, 15)
        )

        frame_dados = ttk.Frame(
            container_registro
        )

        frame_dados.pack(
            fill="x"
        )

        ttk.Label(
            frame_dados,
            text="Status:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=6
        )

        campo_status = ttk.Combobox(
            frame_dados,
            values=STATUS,
            state="readonly",
            width=35
        )

        campo_status.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=6
        )

        campo_status.set(
            lead_selecionado.get(
                "status",
                "EM ANDAMENTO"
            )
        )

        ttk.Label(
            frame_dados,
            text="Próximo Contato:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=6
        )

        campo_proximo_contato = (
            ttk.Entry(
                frame_dados,
                width=38
            )
        )

        campo_proximo_contato.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=6
        )

        campo_proximo_contato.insert(
            0,
            lead_selecionado.get(
                "proximo_contato",
                ""
            )
        )

        campo_proximo_contato.bind(
            "<KeyRelease>",
            mascara_data
        )

        frame_datas_rapidas = (
            ttk.Frame(
                frame_dados
            )
        )

        frame_datas_rapidas.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5,
            pady=(0, 8)
        )

        botoes_datas = []

        def definir_proximo_contato(
            dias=None
        ):
            status_atual = (
                campo_status
                .get()
                .strip()
                .upper()
            )

            if status_atual == "DECLINADO":
                campo_proximo_contato.configure(
                    state="normal"
                )

                campo_proximo_contato.delete(
                    0,
                    tk.END
                )

                campo_proximo_contato.configure(
                    state="disabled"
                )

                return

            campo_proximo_contato.delete(
                0,
                tk.END
            )

            if dias is None:
                return

            nova_data = (
                datetime.now().date()
                + timedelta(
                    days=dias
                )
            )

            campo_proximo_contato.insert(
                0,
                nova_data.strftime(
                    "%d/%m/%Y"
                )
            )

        def adicionar_botao_data(
            texto,
            dias
        ):
            botao = ttk.Button(
                frame_datas_rapidas,
                text=texto,
                command=lambda: (
                    definir_proximo_contato(
                        dias
                    )
                )
            )

            botao.pack(
                side="left",
                padx=4
            )

            botoes_datas.append(
                botao
            )

        adicionar_botao_data(
            "Hoje",
            0
        )

        adicionar_botao_data(
            "Amanhã",
            1
        )

        adicionar_botao_data(
            "+3 dias",
            3
        )

        adicionar_botao_data(
            "+7 dias",
            7
        )

        adicionar_botao_data(
            "Limpar",
            None
        )

        def verificar_status(
            evento=None
        ):
            status_atual = (
                campo_status
                .get()
                .strip()
                .upper()
            )

            if status_atual == "DECLINADO":
                campo_proximo_contato.configure(
                    state="normal"
                )

                campo_proximo_contato.delete(
                    0,
                    tk.END
                )

                campo_proximo_contato.configure(
                    state="disabled"
                )

                for botao in botoes_datas:
                    botao.configure(
                        state="disabled"
                    )

            else:
                campo_proximo_contato.configure(
                    state="normal"
                )

                for botao in botoes_datas:
                    botao.configure(
                        state="normal"
                    )

        campo_status.bind(
            "<<ComboboxSelected>>",
            verificar_status
        )

        verificar_status()

        ttk.Label(
            frame_dados,
            text="Última Interação:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=6
        )

        ultima_interacao = (
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

        ttk.Label(
            frame_dados,
            text=ultima_interacao
        ).grid(
            row=3,
            column=1,
            sticky="w",
            padx=5,
            pady=6
        )

        frame_dados.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            container_registro,
            text=(
                "Observações anteriores:"
            )
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        texto_anterior = tk.Text(
            container_registro,
            height=7,
            wrap="word",
            font=(
                "Arial",
                10
            )
        )

        texto_anterior.pack(
            fill="both"
        )

        texto_anterior.insert(
            "1.0",
            lead_selecionado.get(
                "observacao",
                ""
            )
        )

        texto_anterior.configure(
            state="disabled"
        )

        ttk.Label(
            container_registro,
            text=(
                "Novo acompanhamento:"
            )
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        texto_novo = tk.Text(
            container_registro,
            height=8,
            wrap="word",
            font=(
                "Arial",
                11
            )
        )

        texto_novo.pack(
            expand=True,
            fill="both"
        )

        def salvar_registro():
            nonlocal lead_selecionado

            novo_acompanhamento = (
                texto_novo.get(
                    "1.0",
                    tk.END
                ).strip()
            )

            if not novo_acompanhamento:
                messagebox.showwarning(
                    "Campo obrigatório",
                    (
                        "Digite uma observação "
                        "sobre o contato."
                    ),
                    parent=janela_registro
                )

                texto_novo.focus_set()
                return

            status_escolhido = (
                campo_status
                .get()
                .strip()
            )

            if (
                status_escolhido.upper()
                == "DECLINADO"
            ):
                proximo_contato = ""

            else:
                proximo_contato = (
                    campo_proximo_contato
                    .get()
                    .strip()
                )

            lead_atualizado = (
                lead_selecionado.copy()
            )

            observacao_anterior = str(
                lead_atualizado.get(
                    "observacao",
                    ""
                )
            ).strip()

            novo_registro = (
                f"[{ultima_interacao}]\n"
                f"{novo_acompanhamento}"
            )

            if observacao_anterior:
                observacao_completa = (
                    f"{observacao_anterior}"
                    f"\n\n{novo_registro}"
                )

            else:
                observacao_completa = (
                    novo_registro
                )

            lead_atualizado[
                "status"
            ] = status_escolhido

            lead_atualizado[
                "proximo_contato"
            ] = proximo_contato

            lead_atualizado[
                "ultima_interacao"
            ] = ultima_interacao

            lead_atualizado[
                "observacao"
            ] = observacao_completa

            try:
                atualizar_lead(
                    lead_atualizado
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao registrar",
                    (
                        "Não foi possível "
                        "registrar o contato."
                        f"\n\n{erro}"
                    ),
                    parent=janela_registro
                )
                return

            lead_selecionado = None

            janela_registro.destroy()

            carregar()

            messagebox.showinfo(
                "Contato registrado",
                (
                    "O contato foi registrado "
                    "com sucesso."
                ),
                parent=janela
            )

        frame_acoes = ttk.Frame(
            container_registro
        )

        frame_acoes.pack(
            pady=(15, 0)
        )

        ttk.Button(
            frame_acoes,
            text="Salvar Contato",
            command=salvar_registro
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_acoes,
            text="Cancelar",
            command=(
                janela_registro.destroy
            )
        ).pack(
            side="left",
            padx=5
        )

        texto_novo.bind(
            "<Control-Return>",
            lambda evento: (
                salvar_registro(),
                "break"
            )[1]
        )

        janela_registro.bind(
            "<Escape>",
            lambda evento: (
                janela_registro.destroy()
            )
        )

        texto_novo.focus_set()

    for (
        chave,
        tabela
    ) in tabelas.items():
        tabela.bind(
            "<<TreeviewSelect>>",
            lambda evento,
            chave_aba=chave: (
                selecionar_lead(
                    chave_aba
                )
            )
        )

        tabela.bind(
            "<Double-1>",
            lambda evento: (
                abrir_registro_contato()
            )
        )

    ttk.Button(
        frame_botoes,
        text="Atualizar",
        command=carregar
    ).pack(
        side="left",
        padx=5
    )

    botao_registrar = ttk.Button(
        frame_botoes,
        text="Registrar Contato",
        command=(
            abrir_registro_contato
        ),
        state="disabled"
    )

    botao_registrar.pack(
        side="left",
        padx=5
    )

    botao_copiar = ttk.Button(
        frame_botoes,
        text="Copiar Resumo",
        command=(
            copiar_resumo_selecionado
        ),
        state="disabled"
    )

    botao_copiar.pack(
        side="left",
        padx=5
    )

    botao_copiar_whatsapp = (
        ttk.Button(
            frame_botoes,
            text="Copiar WhatsApp",
            command=(
                copiar_whatsapp_selecionado
            ),
            state="disabled"
        )
    )

    botao_copiar_whatsapp.pack(
        side="left",
        padx=5
    )

    botao_whatsapp = ttk.Button(
        frame_botoes,
        text="Abrir WhatsApp",
        command=(
            abrir_whatsapp_selecionado
        ),
        state="disabled"
    )

    botao_whatsapp.pack(
        side="left",
        padx=5
    )

    ttk.Button(
        frame_botoes,
        text="Fechar",
        command=janela.destroy
    ).pack(
        side="left",
        padx=5
    )

    carregar()