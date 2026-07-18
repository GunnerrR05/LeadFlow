import tkinter as tk
from tkinter import ttk, messagebox

from componentes.campos import mascara_telefone

from servicos.leads import (
    listar_leads,
    atualizar_lead,
    excluir_lead,
)

from datetime import datetime


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


COLUNAS = (
    "data_cadastro",
    "proximo_contato",
    "ultima_interacao",
    "status",
    "telefone",
    "nome",
    "produto",
    "cidade_uf",
    "email",
    "aplicacao",
    "origem",
    "consultor",
    "observacao",
    "resumo",
    "whatsapp",
)


TITULOS = {
    "data_cadastro": "Data de Cadastro",
    "proximo_contato": "Próximo Contato",
    "ultima_interacao": "Última Interação",
    "status": "Status",
    "telefone": "Telefone",
    "nome": "Nome",
    "produto": "Produto",
    "cidade_uf": "Cidade / UF",
    "email": "E-mail",
    "aplicacao": "Aplicação",
    "origem": "Origem",
    "consultor": "Consultor",
    "observacao": "Observação",
    "resumo": "Resumo",
    "whatsapp": "Nome no WhatsApp",
}


LARGURAS = {
    "data_cadastro": 140,
    "proximo_contato": 130,
    "ultima_interacao": 140,
    "status": 190,
    "telefone": 120,
    "nome": 160,
    "produto": 170,
    "cidade_uf": 140,
    "email": 200,
    "aplicacao": 180,
    "origem": 140,
    "consultor": 140,
    "observacao": 250,
    "resumo": 350,
    "whatsapp": 400,
}


def abrir_lista():
    lead_selecionado = None
    leads_carregados = []

    janela_lista = tk.Toplevel()
    janela_lista.title("Leads Cadastrados")
    janela_lista.geometry("1400x650")

    try:
        janela_lista.state("zoomed")
    except tk.TclError:
        pass

    container = ttk.Frame(
        janela_lista,
        padding=10
    )
    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Leads Cadastrados",
        font=("Arial", 18, "bold")
    ).pack(pady=(0, 10))

    frame_filtros = ttk.Frame(container)

    frame_filtros.pack(
        fill="x",
        pady=(0, 10)
    )


    ttk.Label(
        frame_filtros,
        text="Pesquisar:"
    ).pack(
        side="left",
        padx=(0, 5)
    )


    campo_pesquisa = ttk.Entry(
        frame_filtros,
        width=35
    )

    campo_pesquisa.pack(
        side="left",
        padx=(0, 15)
    )


    ttk.Label(
        frame_filtros,
        text="Status:"
    ).pack(
        side="left",
        padx=(0, 5)
    )


    filtro_status = ttk.Combobox(
        frame_filtros,
        values=["TODOS"] + STATUS,
        state="readonly",
        width=24
    )

    filtro_status.set("TODOS")

    filtro_status.pack(
        side="left",
        padx=(0, 10)
    )

    frame_tabela = ttk.Frame(container)
    frame_tabela.pack(
        expand=True,
        fill="both"
    )

    barra_vertical = ttk.Scrollbar(
        frame_tabela,
        orient="vertical"
    )

    barra_horizontal = ttk.Scrollbar(
        frame_tabela,
        orient="horizontal"
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=COLUNAS,
        show="headings",
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set,
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
            text=TITULOS[coluna]
        )

        tabela.column(
            coluna,
            width=LARGURAS[coluna],
            minwidth=80,
            anchor="w",
            stretch=False
        )

    frame_botoes = ttk.Frame(container)
    frame_botoes.pack(pady=12)

    def preencher_tabela(lista_leads):
        nonlocal lead_selecionado

        lead_selecionado = None

        for item in tabela.get_children():
            tabela.delete(item)

        for lead in lista_leads:
            linha = lead.get("linha")

            tabela.insert(
                "",
                tk.END,
                iid=str(linha),
                values=(
                    lead.get("data_cadastro", ""),
                    lead.get("proximo_contato", ""),
                    lead.get("ultima_interacao", ""),
                    lead.get("status", ""),
                    lead.get("telefone", ""),
                    lead.get("nome", ""),
                    lead.get("produto", ""),
                    lead.get("cidade_uf", ""),
                    lead.get("email", ""),
                    lead.get("aplicacao", ""),
                    lead.get("origem", ""),
                    lead.get("consultor", ""),
                    lead.get("observacao", ""),
                    lead.get("resumo", ""),
                    lead.get("whatsapp", ""),
                )
            )

        botao_editar.configure(state="disabled")
        botao_excluir.configure(state="disabled")

    def carregar_tabela():
        nonlocal leads_carregados

        try:
            leads_carregados = listar_leads()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao listar",
                (
                    "Não foi possível carregar os leads."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        preencher_tabela(leads_carregados)

    def aplicar_filtros(evento=None):
        texto = campo_pesquisa.get().strip().casefold()
        status_escolhido = filtro_status.get()

        leads_filtrados = []

        for lead in leads_carregados:
            status_lead = str(
                lead.get("status", "")
            )

            corresponde_status = (
                status_escolhido == "TODOS"
                or status_lead == status_escolhido
            )

            campos_pesquisaveis = (
                lead.get("nome", ""),
                lead.get("telefone", ""),
                lead.get("produto", ""),
                lead.get("cidade_uf", ""),
                lead.get("email", ""),
                lead.get("origem", ""),
                lead.get("consultor", ""),
            )

            corresponde_texto = (
                not texto
                or any(
                    texto in str(valor).casefold()
                    for valor in campos_pesquisaveis
                )
            )

            if corresponde_status and corresponde_texto:
                leads_filtrados.append(lead)

    

        preencher_tabela(leads_filtrados)

    def limpar_filtros():
        campo_pesquisa.delete(0, tk.END)
        filtro_status.set("TODOS")

        preencher_tabela(leads_carregados)

    
    ordem_colunas = {}


    def converter_valor_ordenacao(coluna, valor):
        texto = str(valor).strip()

        if coluna in (
            "data_cadastro",
            "proximo_contato",
            "ultima_interacao",
        ):
            formatos = (
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y",
            )

            for formato in formatos:
                try:
                    return datetime.strptime(
                        texto,
                        formato
                    )
                except ValueError:
                    continue

            return datetime.min

        return texto.casefold()


    def ordenar_tabela(coluna):
        crescente = ordem_colunas.get(
            coluna,
            True
        )

        itens = []

        for item_id in tabela.get_children():
            valor = tabela.set(
                item_id,
                coluna
            )

            itens.append(
                (
                    converter_valor_ordenacao(
                        coluna,
                        valor
                    ),
                    item_id
                )
            )

        itens.sort(
            key=lambda item: item[0],
            reverse=not crescente
        )

        for posicao, (_, item_id) in enumerate(itens):
            tabela.move(
                item_id,
                "",
                posicao
            )

        ordem_colunas[coluna] = not crescente

        for nome_coluna in COLUNAS:
            tabela.heading(
                nome_coluna,
                text=TITULOS[nome_coluna],
                command=lambda coluna_atual=nome_coluna: (
                    ordenar_tabela(coluna_atual)
                )
            )

        simbolo = " ▲" if crescente else " ▼"

        tabela.heading(
            coluna,
            text=TITULOS[coluna] + simbolo,
            command=lambda: ordenar_tabela(coluna)
        )

    for coluna in COLUNAS:
        tabela.heading(
            coluna,
            text=TITULOS[coluna],
            command=lambda coluna_atual=coluna: (
                ordenar_tabela(coluna_atual)
            )
        )

    ttk.Button(
        frame_filtros,
        text="Filtrar",
        command=aplicar_filtros
    ).pack(side="left", padx=5)

    ttk.Button(
        frame_filtros,
        text="Limpar",
        command=limpar_filtros
    ).pack(side="left", padx=5)

    def selecionar_lead(evento=None):
        nonlocal lead_selecionado

        selecao = tabela.selection()

        if not selecao:
            lead_selecionado = None

            botao_editar.configure(state="disabled")
            botao_excluir.configure(state="disabled")
            return

        item = selecao[0]
        linha = int(item)

        lead_selecionado = next(
            (
                lead
                for lead in leads_carregados
                if lead.get("linha") == linha
            ),
            None
        )

        if lead_selecionado is not None:
            botao_editar.configure(state="normal")
            botao_excluir.configure(state="normal")

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_lead
    )

    def editar():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um lead primeiro.",
                parent=janela_lista
            )
            return

        janela_editar = tk.Toplevel(janela_lista)
        janela_editar.title("Editar Lead")
        janela_editar.geometry("540x720")
        janela_editar.resizable(False, False)
        janela_editar.transient(janela_lista)
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
            text=lead_selecionado.get(
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
            ("Próximo Contato", "proximo_contato"),
            ("Última Interação", "ultima_interacao"),
            ("Status", "status"),
            ("Telefone", "telefone"),
            ("Nome", "nome"),
            ("Produto", "produto"),
            ("Cidade / UF", "cidade_uf"),
            ("E-mail", "email"),
            ("Aplicação", "aplicacao"),
            ("Origem", "origem"),
            ("Consultor", "consultor"),
            ("Observação", "observacao"),
        ]

        for numero_linha, (texto, chave) in enumerate(
            campos,
            start=2
        ):
            ttk.Label(
                container_edicao,
                text=f"{texto}:"
            ).grid(
                row=numero_linha,
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
                    width=36
                )

                campo.set(
                    lead_selecionado.get(
                        chave,
                        "EM ANDAMENTO"
                    )
                )

            elif chave == "aplicacao":
                campo = ttk.Combobox(
                    container_edicao,
                    values=APLICACOES,
                    state="readonly",
                    width=36
                )

                campo.set(
                    lead_selecionado.get(
                        chave,
                        APLICACOES[0]
                    )
                )

            else:
                campo = ttk.Entry(
                    container_edicao,
                    width=39
                )

                campo.insert(
                    0,
                    lead_selecionado.get(
                        chave,
                        ""
                    )
                )

            campo.grid(
                row=numero_linha,
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

        def salvar_alteracoes():
            nonlocal lead_selecionado

            lead_atualizado = lead_selecionado.copy()

            for chave, campo in campos_edicao.items():
                lead_atualizado[chave] = (
                    campo.get().strip()
                )

            if not lead_atualizado["nome"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o nome do lead.",
                    parent=janela_editar
                )
                campos_edicao["nome"].focus_set()
                return

            if not lead_atualizado["telefone"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o telefone do lead.",
                    parent=janela_editar
                )
                campos_edicao["telefone"].focus_set()
                return

            if not lead_atualizado["produto"]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe o produto.",
                    parent=janela_editar
                )
                campos_edicao["produto"].focus_set()
                return

            try:
                atualizar_lead(lead_atualizado)

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao atualizar",
                    (
                        "Não foi possível atualizar o lead."
                        f"\n\n{erro}"
                    ),
                    parent=janela_editar
                )
                return

            janela_editar.destroy()
            carregar_tabela()

            messagebox.showinfo(
                "Sucesso",
                "Lead atualizado com sucesso!",
                parent=janela_lista
            )

        ttk.Button(
            container_edicao,
            text="Salvar Alterações",
            command=salvar_alteracoes
        ).grid(
            row=len(campos) + 2,
            column=0,
            columnspan=2,
            pady=20
        )

    def excluir():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um lead primeiro.",
                parent=janela_lista
            )
            return

        confirmacao = messagebox.askyesno(
            "Excluir Lead",
            (
                "Deseja realmente excluir este lead?"
                "\n\n"
                f"Nome: {lead_selecionado.get('nome', '')}\n"
                f"Telefone: "
                f"{lead_selecionado.get('telefone', '')}"
            ),
            parent=janela_lista
        )

        if not confirmacao:
            return

        try:
            excluir_lead(lead_selecionado)

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                (
                    "Não foi possível excluir o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        carregar_tabela()

        messagebox.showinfo(
            "Sucesso",
            "Lead excluído com sucesso!",
            parent=janela_lista
        )

    botao_atualizar = ttk.Button(
        frame_botoes,
        text="Atualizar Lista",
        command=carregar_tabela
    )
    botao_atualizar.pack(
        side="left",
        padx=5
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

    ttk.Button(
        frame_botoes,
        text="Fechar",
        command=janela_lista.destroy
    ).pack(
        side="left",
        padx=5
    )

    tabela.bind(
        "<Double-1>",
        lambda evento: editar()
        if tabela.selection()
        else None
    )


    campo_pesquisa.bind(
    "<KeyRelease>",
    aplicar_filtros
)

    filtro_status.bind(
        "<<ComboboxSelected>>",
        aplicar_filtros
    )

    carregar_tabela()