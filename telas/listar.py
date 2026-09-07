import tkinter as tk
from functools import partial
from tkinter import (
    ttk,
    messagebox,
    filedialog,
)
from datetime import datetime

from componentes.campos import (
    mascara_telefone,
    inserir_quebra_linha,
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

from servicos.leads import (
    listar_leads,
    atualizar_lead,
    excluir_lead,
)

from servicos.backup import criar_backup
from servicos.exportacao import exportar_leads
from tema import aplicar_tema_carteira


_ttk_padrao = ttk


class _ComponentesCarteira:
    """Cria componentes ttk usando apenas os estilos da carteira."""

    Frame = partial(
        _ttk_padrao.Frame,
        style="Carteira.TFrame",
    )
    Label = partial(
        _ttk_padrao.Label,
        style="Carteira.TLabel",
    )
    LabelFrame = partial(
        _ttk_padrao.LabelFrame,
        style="Carteira.TLabelframe",
    )
    Button = partial(
        _ttk_padrao.Button,
        style="Carteira.TButton",
    )
    Entry = partial(
        _ttk_padrao.Entry,
        style="Carteira.TEntry",
    )
    Combobox = partial(
        _ttk_padrao.Combobox,
        style="Carteira.TCombobox",
    )
    Treeview = partial(
        _ttk_padrao.Treeview,
        style="Carteira.Treeview",
    )
    Scrollbar = _ttk_padrao.Scrollbar


ttk = _ComponentesCarteira()


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
    "unidade",
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
    "unidade": "Unidade",
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
    "unidade": 150,
    "status": 190,
    "telefone": 140,
    "nome": 170,
    "produto": 170,
    "cidade_uf": 140,
    "email": 200,
    "aplicacao": 180,
    "origem": 140,
    "consultor": 140,
    "observacao": 280,
    "resumo": 350,
    "whatsapp": 400,
}


def abrir_lista():
    lead_selecionado = None
    leads_carregados = []
    leads_exibidos = []

    botao_editar = None
    botao_excluir = None
    botao_copiar = None
    botao_copiar_whatsapp = None
    botao_whatsapp = None
    botao_acompanhamento = None

    campo_status_rapido = None
    botao_status_rapido = None

    janela_lista = tk.Toplevel()
    aplicar_tema_carteira(
        _ttk_padrao.Style(janela_lista)
    )
    janela_lista.title(
        "Leads Cadastrados"
    )
    janela_lista.geometry(
        "1400x850"
    )
    janela_lista.minsize(
        1100,
        700
    )

    try:
        janela_lista.state(
            "zoomed"
        )
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
        font=(
            "Arial",
            18,
            "bold"
        )
    ).pack(
        pady=(0, 10)
    )

    # =========================================================
    # FILTROS
    # =========================================================

    frame_filtros = ttk.Frame(
        container
    )
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
        values=[
            "TODOS"
        ] + STATUS,
        state="readonly",
        width=24
    )
    filtro_status.set(
        "TODOS"
    )
    filtro_status.pack(
        side="left",
        padx=(0, 10)
    )

    label_quantidade = ttk.Label(
        container,
        text="",
        font=(
            "Arial",
            10,
            "bold"
        )
    )
    label_quantidade.pack(
        anchor="w",
        pady=(0, 8)
    )

    # =========================================================
    # TABELA
    # =========================================================

    frame_tabela = ttk.Frame(
        container
    )
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
            text=TITULOS[coluna]
        )

        tabela.column(
            coluna,
            width=LARGURAS[coluna],
            minwidth=80,
            anchor="w",
            stretch=False
        )

    tabela.tag_configure(
        "em_andamento",
        background="#FFF2CC"
    )

    tabela.tag_configure(
        "negociacao",
        background="#DDEBFF"
    )

    tabela.tag_configure(
        "declinado",
        background="#FFDADA"
    )

    tabela.tag_configure(
        "conquistado",
        background="#DDF4DD"
    )

    tabela.tag_configure(
        "futura",
        background="#E8DDF5"
    )

    tabela.tag_configure(
        "cliente_ativo",
        background="#D9F0F0"
    )

    # =========================================================
    # ÁREAS INFERIORES
    # =========================================================

    frame_botoes = ttk.Frame(
        container
    )
    frame_botoes.pack(
        pady=(12, 8)
    )

    frame_status_rapido = (
        ttk.LabelFrame(
            container,
            text=(
                "Alteração rápida "
                "de status"
            ),
            padding=8
        )
    )
    frame_status_rapido.pack(
        fill="x",
        pady=(0, 10)
    )

    frame_observacao = (
        ttk.LabelFrame(
            container,
            text=(
                "Observação do Lead "
                "Selecionado"
            ),
            padding=8,
            height=300
        )
    )
    frame_observacao.pack(
        fill="x",
        pady=(0, 5)
    )

    frame_observacao.pack_propagate(
        False
    )

    texto_observacao = tk.Text(
        frame_observacao,
        wrap="word",
        font=(
            "Arial",
            11
        )
    )
    texto_observacao.pack(
        expand=True,
        fill="both"
    )
    texto_observacao.configure(
        state="disabled"
    )

    # =========================================================
    # FUNÇÕES AUXILIARES
    # =========================================================

    def mostrar_observacao(
        texto=""
    ):
        texto_observacao.configure(
            state="normal"
        )

        texto_observacao.delete(
            "1.0",
            tk.END
        )

        texto_observacao.insert(
            "1.0",
            texto
        )

        texto_observacao.configure(
            state="disabled"
        )

    def desabilitar_acoes():
        if botao_editar is not None:
            botao_editar.configure(
                state="disabled"
            )

        if botao_excluir is not None:
            botao_excluir.configure(
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

        if (
            botao_acompanhamento
            is not None
        ):
            botao_acompanhamento.configure(
                state="disabled"
            )

        if (
            campo_status_rapido
            is not None
        ):
            campo_status_rapido.set(
                ""
            )

            campo_status_rapido.configure(
                state="disabled"
            )

        if (
            botao_status_rapido
            is not None
        ):
            botao_status_rapido.configure(
                state="disabled"
            )

    def habilitar_acoes():
        if botao_editar is not None:
            botao_editar.configure(
                state="normal"
            )

        if botao_excluir is not None:
            botao_excluir.configure(
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

        if (
            botao_acompanhamento
            is not None
        ):
            botao_acompanhamento.configure(
                state="normal"
            )

        if (
            campo_status_rapido
            is not None
        ):
            campo_status_rapido.configure(
                state="readonly"
            )

        if (
            botao_status_rapido
            is not None
        ):
            botao_status_rapido.configure(
                state="normal"
            )

    def obter_tag_status(
        status
    ):
        status = str(
            status
        ).strip().upper()

        if status == "EM ANDAMENTO":
            return "em_andamento"

        if status == "NEGOCIAÇÃO":
            return "negociacao"

        if status == "DECLINADO":
            return "declinado"

        if status in (
            "CONQUISTADO - SUPRIM",
            "CONQUISTADO - EQUIP",
        ):
            return "conquistado"

        if status == "FUTURA":
            return "futura"

        if status == "CLIENTE ATIVO":
            return "cliente_ativo"

        return ""

    # =========================================================
    # CARREGAMENTO E FILTROS
    # =========================================================

    def preencher_tabela(
        lista_leads
    ):
        nonlocal lead_selecionado
        nonlocal leads_exibidos

        lead_selecionado = None

        leads_exibidos = list(
            lista_leads
        )

        quantidade_exibida = len(
            leads_exibidos
        )

        quantidade_total = len(
            leads_carregados
        )

        if quantidade_exibida == 1:
            texto_exibidos = (
                "1 lead exibido"
            )
        else:
            texto_exibidos = (
                f"{quantidade_exibida} "
                "leads exibidos"
            )

        label_quantidade.configure(
            text=(
                f"{texto_exibidos} "
                f"de {quantidade_total} "
                "cadastrados"
            )
        )

        mostrar_observacao()
        desabilitar_acoes()

        for item in (
            tabela.get_children()
        ):
            tabela.delete(
                item
            )

        for lead in leads_exibidos:
            linha = lead.get(
                "linha"
            )

            if linha is None:
                continue

            tag_status = (
                obter_tag_status(
                    lead.get(
                        "status",
                        ""
                    )
                )
            )

            observacao_tabela = str(
                lead.get(
                    "observacao",
                    ""
                )
            ).replace(
                "\n",
                " | "
            )

            tabela.insert(
                "",
                tk.END,
                iid=str(linha),
                tags=(
                    tag_status,
                ),
                values=(
                    lead.get(
                        "data_cadastro",
                        ""
                    ),
                    lead.get(
                        "proximo_contato",
                        ""
                    ),
                    lead.get(
                        "ultima_interacao",
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
                        "telefone",
                        ""
                    ),
                    lead.get(
                        "nome",
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
                        "email",
                        ""
                    ),
                    lead.get(
                        "aplicacao",
                        ""
                    ),
                    lead.get(
                        "origem",
                        ""
                    ),
                    lead.get(
                        "consultor",
                        ""
                    ),
                    observacao_tabela,
                    lead.get(
                        "resumo",
                        ""
                    ),
                    lead.get(
                        "whatsapp",
                        ""
                    ),
                )
            )

    def carregar_tabela():
        nonlocal leads_carregados

        try:
            leads_carregados = (
                listar_leads()
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao listar",
                (
                    "Não foi possível "
                    "carregar os leads."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        preencher_tabela(
            leads_carregados
        )

    def aplicar_filtros(
        evento=None
    ):
        texto = (
            campo_pesquisa
            .get()
            .strip()
            .casefold()
        )

        status_escolhido = (
            filtro_status.get()
        )

        leads_filtrados = []

        for lead in (
            leads_carregados
        ):
            status_lead = str(
                lead.get(
                    "status",
                    ""
                )
            )

            corresponde_status = (
                status_escolhido
                == "TODOS"
                or status_lead
                == status_escolhido
            )

            campos_pesquisaveis = (
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
                    "unidade",
                    ""
                ),
                lead.get(
                    "email",
                    ""
                ),
                lead.get(
                    "origem",
                    ""
                ),
                lead.get(
                    "consultor",
                    ""
                ),
            )

            corresponde_texto = (
                not texto
                or any(
                    texto
                    in str(
                        valor
                    ).casefold()
                    for valor
                    in campos_pesquisaveis
                )
            )

            if (
                corresponde_status
                and corresponde_texto
            ):
                leads_filtrados.append(
                    lead
                )

        preencher_tabela(
            leads_filtrados
        )

    def limpar_filtros():
        campo_pesquisa.delete(
            0,
            tk.END
        )

        filtro_status.set(
            "TODOS"
        )

        preencher_tabela(
            leads_carregados
        )

    # =========================================================
    # EXPORTAÇÃO
    # =========================================================

    def exportar_relatorio():
        if not leads_exibidos:
            messagebox.showwarning(
                "Nenhum lead",
                (
                    "Não existem leads "
                    "visíveis para exportar."
                ),
                parent=janela_lista
            )
            return

        caminho = (
            filedialog
            .asksaveasfilename(
                title=(
                    "Salvar Relatório"
                ),
                defaultextension=(
                    ".xlsx"
                ),
                filetypes=[
                    (
                        "Planilha do Excel",
                        "*.xlsx"
                    )
                ],
                initialfile=(
                    "relatorio_leads.xlsx"
                ),
                parent=janela_lista
            )
        )

        if not caminho:
            return

        try:
            arquivo = exportar_leads(
                leads_exibidos,
                caminho
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao exportar",
                (
                    "Não foi possível "
                    "exportar o relatório."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        messagebox.showinfo(
            "Relatório exportado",
            (
                "O relatório foi salvo "
                "com sucesso!"
                f"\n\n{arquivo}"
            ),
            parent=janela_lista
        )

    # =========================================================
    # ORDENAÇÃO
    # =========================================================

    ordem_colunas = {}

    def converter_valor_ordenacao(
        coluna,
        valor
    ):
        texto = str(
            valor
        ).strip()

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
                    return (
                        datetime.strptime(
                            texto,
                            formato
                        )
                    )

                except ValueError:
                    continue

            return datetime.min

        return texto.casefold()

    def ordenar_tabela(
        coluna
    ):
        crescente = (
            ordem_colunas.get(
                coluna,
                True
            )
        )

        itens = []

        for item_id in (
            tabela.get_children()
        ):
            valor = tabela.set(
                item_id,
                coluna
            )

            valor_convertido = (
                converter_valor_ordenacao(
                    coluna,
                    valor
                )
            )

            itens.append(
                (
                    valor_convertido,
                    item_id
                )
            )

        itens.sort(
            key=lambda item: item[0],
            reverse=not crescente
        )

        for posicao, (
            _,
            item_id
        ) in enumerate(
            itens
        ):
            tabela.move(
                item_id,
                "",
                posicao
            )

        ordem_colunas[coluna] = (
            not crescente
        )

        for nome_coluna in COLUNAS:
            tabela.heading(
                nome_coluna,
                text=TITULOS[
                    nome_coluna
                ],
                command=(
                    lambda
                    coluna_atual=nome_coluna:
                    ordenar_tabela(
                        coluna_atual
                    )
                )
            )

        simbolo = (
            " ▲"
            if crescente
            else " ▼"
        )

        tabela.heading(
            coluna,
            text=(
                TITULOS[coluna]
                + simbolo
            ),
            command=lambda: (
                ordenar_tabela(
                    coluna
                )
            )
        )

    for coluna in COLUNAS:
        tabela.heading(
            coluna,
            text=TITULOS[coluna],
            command=(
                lambda
                coluna_atual=coluna:
                ordenar_tabela(
                    coluna_atual
                )
            )
        )

    # =========================================================
    # SELEÇÃO
    # =========================================================

    def selecionar_lead(
        evento=None
    ):
        nonlocal lead_selecionado

        selecao = (
            tabela.selection()
        )

        if not selecao:
            lead_selecionado = None
            desabilitar_acoes()
            mostrar_observacao()
            return

        item_id = selecao[0]

        try:
            linha = int(
                item_id
            )

        except ValueError:
            lead_selecionado = None
            desabilitar_acoes()
            mostrar_observacao()
            return

        lead_selecionado = next(
            (
                lead
                for lead
                in leads_carregados
                if int(
                    lead.get(
                        "linha",
                        0
                    )
                ) == linha
            ),
            None
        )

        if lead_selecionado is None:
            desabilitar_acoes()
            mostrar_observacao()
            return

        habilitar_acoes()

        campo_status_rapido.set(
            lead_selecionado.get(
                "status",
                "EM ANDAMENTO"
            )
        )

        mostrar_observacao(
            lead_selecionado.get(
                "observacao",
                ""
            )
        )

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_lead
    )

    # =========================================================
    # COPIAR E WHATSAPP
    # =========================================================

    def copiar_resumo_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        try:
            copiar_resumo(
                janela_lista,
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível copiar "
                    "o resumo."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        messagebox.showinfo(
            "Resumo copiado",
            (
                "O resumo do lead "
                "foi copiado."
            ),
            parent=janela_lista
        )

    def copiar_whatsapp_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        try:
            copiar_whatsapp(
                janela_lista,
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao copiar",
                (
                    "Não foi possível copiar "
                    "o nome do WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        messagebox.showinfo(
            "WhatsApp copiado",
            (
                "O nome para o WhatsApp "
                "foi copiado."
            ),
            parent=janela_lista
        )

    def abrir_whatsapp_selecionado():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
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
                    "Não foi possível abrir "
                    "o WhatsApp."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )

    # =========================================================
    # ALTERAÇÃO RÁPIDA DE STATUS
    # =========================================================

    def atualizar_status_rapido():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        novo_status = (
            campo_status_rapido
            .get()
            .strip()
        )

        if not novo_status:
            messagebox.showwarning(
                "Status",
                (
                    "Selecione o novo "
                    "status."
                ),
                parent=janela_lista
            )
            return

        status_atual = str(
            lead_selecionado.get(
                "status",
                ""
            )
        ).strip()

        if novo_status == status_atual:
            messagebox.showinfo(
                "Status",
                (
                    "O lead já possui "
                    "esse status."
                ),
                parent=janela_lista
            )
            return

        lead_atualizado = (
            lead_selecionado.copy()
        )

        lead_atualizado[
            "status"
        ] = novo_status

        if (
            novo_status
            .strip()
            .upper()
            == "DECLINADO"
        ):
            lead_atualizado[
                "proximo_contato"
            ] = ""

        try:
            atualizar_lead(
                lead_atualizado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                (
                    "Não foi possível alterar "
                    "o status do lead."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        carregar_tabela()
        aplicar_filtros()

        messagebox.showinfo(
            "Status atualizado",
            (
                "O status do lead foi "
                "alterado com sucesso."
            ),
            parent=janela_lista
        )

    # =========================================================
    # ACOMPANHAMENTO
    # =========================================================

    def adicionar_acompanhamento():
        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        janela_acompanhamento = (
            tk.Toplevel(
                janela_lista
            )
        )
        janela_acompanhamento.title(
            "Adicionar Acompanhamento"
        )
        janela_acompanhamento.geometry(
            "650x420"
        )
        janela_acompanhamento.transient(
            janela_lista
        )
        janela_acompanhamento.grab_set()

        container_acompanhamento = (
            ttk.Frame(
                janela_acompanhamento,
                padding=20
            )
        )
        container_acompanhamento.pack(
            expand=True,
            fill="both"
        )

        ttk.Label(
            container_acompanhamento,
            text="Novo acompanhamento",
            font=(
                "Arial",
                18,
                "bold"
            )
        ).pack(
            pady=(0, 5)
        )

        ttk.Label(
            container_acompanhamento,
            text=(
                "Lead: "
                f"{lead_selecionado.get('nome', '')}"
            )
        ).pack(
            pady=(0, 15)
        )

        texto_novo = tk.Text(
            container_acompanhamento,
            height=12,
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

        def salvar_acompanhamento():
            nova_observacao = (
                texto_novo.get(
                    "1.0",
                    tk.END
                ).strip()
            )

            if not nova_observacao:
                messagebox.showwarning(
                    "Observação vazia",
                    (
                        "Digite o "
                        "acompanhamento."
                    ),
                    parent=(
                        janela_acompanhamento
                    )
                )
                texto_novo.focus_set()
                return

            lead_atualizado = (
                lead_selecionado.copy()
            )

            observacao_anterior = str(
                lead_atualizado.get(
                    "observacao",
                    ""
                )
            ).strip()

            data_hora = (
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

            novo_registro = (
                f"[{data_hora}]\n"
                f"{nova_observacao}"
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
                "observacao"
            ] = observacao_completa

            lead_atualizado[
                "ultima_interacao"
            ] = data_hora

            try:
                atualizar_lead(
                    lead_atualizado
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao atualizar",
                    (
                        "Não foi possível salvar "
                        "o acompanhamento."
                        f"\n\n{erro}"
                    ),
                    parent=(
                        janela_acompanhamento
                    )
                )
                return

            janela_acompanhamento.destroy()

            carregar_tabela()
            aplicar_filtros()

            messagebox.showinfo(
                "Acompanhamento salvo",
                (
                    "O acompanhamento foi "
                    "adicionado com sucesso."
                ),
                parent=janela_lista
            )

        frame_acoes = ttk.Frame(
            container_acompanhamento
        )
        frame_acoes.pack(
            pady=(15, 0)
        )

        ttk.Button(
            frame_acoes,
            text=(
                "Salvar "
                "Acompanhamento"
            ),
            command=(
                salvar_acompanhamento
            )
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_acoes,
            text="Cancelar",
            command=(
                janela_acompanhamento
                .destroy
            )
        ).pack(
            side="left",
            padx=5
        )

        texto_novo.bind(
            "<Control-Return>",
            lambda evento: (
                salvar_acompanhamento(),
                "break"
            )[1]
        )

        texto_novo.focus_set()

    # =========================================================
    # EDIÇÃO COMPLETA
    # =========================================================

    def editar():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        janela_editar = tk.Toplevel(
            janela_lista
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
            janela_lista
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

        for numero_linha, (
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
                row=numero_linha,
                column=0,
                sticky="w",
                padx=5,
                pady=5
            )

            valor_atual = (
                lead_selecionado.get(
                    chave,
                    ""
                )
            )

            if chave == "unidade":
                campo = ttk.Combobox(
                    container_edicao,
                    values=UNIDADES,
                    state="readonly",
                    width=36
                )

                campo.set(
                    valor_atual
                )

            elif chave == "status":
                campo = ttk.Combobox(
                    container_edicao,
                    values=STATUS,
                    state="readonly",
                    width=36
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
                    width=36
                )

                campo.set(
                    valor_atual
                    or (
                        OPCAO_EMAIL_NAO_INFORMADO
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
                    valor_atual
                    or APLICACOES[0]
                )

            elif chave == "observacao":
                campo = tk.Text(
                    container_edicao,
                    width=39,
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
                    width=39
                )

                campo.insert(
                    0,
                    valor_atual
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

            campos_edicao[
                chave
            ] = campo

        def verificar_status_edicao(
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

        def selecionar_email_edicao(
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
                == (
                    OPCAO_EMAIL_NAO_INFORMADO
                )
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
            verificar_status_edicao
        )

        campos_edicao[
            "email"
        ].bind(
            "<<ComboboxSelected>>",
            selecionar_email_edicao
        )

        container_edicao.columnconfigure(
            1,
            weight=1
        )

        def salvar_alteracoes():
            nonlocal lead_selecionado

            lead_atualizado = (
                lead_selecionado.copy()
            )

            for chave, campo in (
                campos_edicao.items()
            ):
                if isinstance(
                    campo,
                    tk.Text
                ):
                    valor = campo.get(
                        "1.0",
                        tk.END
                    ).strip()

                else:
                    valor = (
                        campo.get().strip()
                    )

                lead_atualizado[
                    chave
                ] = valor

            if (
                lead_atualizado
                .get(
                    "status",
                    ""
                )
                .strip()
                .upper()
                == "DECLINADO"
            ):
                lead_atualizado[
                    "proximo_contato"
                ] = ""

            if not lead_atualizado[
                "nome"
            ]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    (
                        "Informe o nome "
                        "do lead."
                    ),
                    parent=janela_editar
                )

                campos_edicao[
                    "nome"
                ].focus_set()
                return

            if not lead_atualizado[
                "telefone"
            ]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    (
                        "Informe o telefone "
                        "do lead."
                    ),
                    parent=janela_editar
                )

                campos_edicao[
                    "telefone"
                ].focus_set()
                return

            if not lead_atualizado[
                "produto"
            ]:
                messagebox.showwarning(
                    "Campo obrigatório",
                    (
                        "Informe o produto."
                    ),
                    parent=janela_editar
                )

                campos_edicao[
                    "produto"
                ].focus_set()
                return

            try:
                atualizar_lead(
                    lead_atualizado
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro ao atualizar",
                    (
                        "Não foi possível "
                        "atualizar o lead."
                        f"\n\n{erro}"
                    ),
                    parent=janela_editar
                )
                return

            janela_editar.destroy()

            carregar_tabela()
            aplicar_filtros()

            messagebox.showinfo(
                "Sucesso",
                (
                    "Lead atualizado "
                    "com sucesso!"
                ),
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

    # =========================================================
    # EXCLUSÃO
    # =========================================================

    def excluir():
        nonlocal lead_selecionado

        if lead_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                (
                    "Selecione um lead "
                    "primeiro."
                ),
                parent=janela_lista
            )
            return

        confirmacao = (
            messagebox.askyesno(
                "Excluir Lead",
                (
                    "Deseja realmente "
                    "excluir este lead?"
                    "\n\n"
                    "Nome: "
                    f"{lead_selecionado.get('nome', '')}\n"
                    "Telefone: "
                    f"{lead_selecionado.get('telefone', '')}"
                ),
                parent=janela_lista
            )
        )

        if not confirmacao:
            return

        try:
            criar_backup()

            excluir_lead(
                lead_selecionado
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                (
                    "Não foi possível criar "
                    "o backup ou excluir "
                    "o lead."
                    f"\n\n{erro}"
                ),
                parent=janela_lista
            )
            return

        carregar_tabela()
        aplicar_filtros()

        messagebox.showinfo(
            "Sucesso",
            (
                "Lead excluído "
                "com sucesso!"
            ),
            parent=janela_lista
        )

    # =========================================================
    # BOTÕES DOS FILTROS
    # =========================================================

    ttk.Button(
        frame_filtros,
        text="Filtrar",
        command=aplicar_filtros
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        frame_filtros,
        text="Limpar",
        command=limpar_filtros
    ).pack(
        side="left",
        padx=5
    )

    # =========================================================
    # BOTÕES PRINCIPAIS
    # =========================================================

    ttk.Button(
        frame_botoes,
        text="Atualizar Lista",
        command=carregar_tabela
    ).pack(
        side="left",
        padx=3
    )

    ttk.Button(
        frame_botoes,
        text="Exportar Relatório",
        command=exportar_relatorio
    ).pack(
        side="left",
        padx=3
    )

    botao_editar = ttk.Button(
        frame_botoes,
        text="Editar Lead",
        command=editar,
        state="disabled"
    )
    botao_editar.pack(
        side="left",
        padx=3
    )

    botao_acompanhamento = (
        ttk.Button(
            frame_botoes,
            text=(
                "Adicionar "
                "Acompanhamento"
            ),
            command=(
                adicionar_acompanhamento
            ),
            state="disabled"
        )
    )
    botao_acompanhamento.pack(
        side="left",
        padx=3
    )

    botao_excluir = ttk.Button(
        frame_botoes,
        text="Excluir Lead",
        command=excluir,
        state="disabled"
    )
    botao_excluir.pack(
        side="left",
        padx=3
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
        padx=3
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
        padx=3
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
        padx=3
    )

    ttk.Button(
        frame_botoes,
        text="Fechar",
        command=(
            janela_lista.destroy
        )
    ).pack(
        side="left",
        padx=3
    )

    # =========================================================
    # CONTROLES DO STATUS RÁPIDO
    # =========================================================

    ttk.Label(
        frame_status_rapido,
        text="Novo status:"
    ).pack(
        side="left",
        padx=(0, 5)
    )

    campo_status_rapido = (
        ttk.Combobox(
            frame_status_rapido,
            values=STATUS,
            state="disabled",
            width=28
        )
    )
    campo_status_rapido.pack(
        side="left",
        padx=5
    )

    botao_status_rapido = (
        ttk.Button(
            frame_status_rapido,
            text="Atualizar Status",
            command=(
                atualizar_status_rapido
            ),
            state="disabled"
        )
    )
    botao_status_rapido.pack(
        side="left",
        padx=5
    )

    # =========================================================
    # EVENTOS
    # =========================================================

    tabela.bind(
        "<Double-1>",
        lambda evento: (
            editar()
            if tabela.selection()
            else None
        )
    )

    campo_pesquisa.bind(
        "<KeyRelease>",
        aplicar_filtros
    )

    filtro_status.bind(
        "<<ComboboxSelected>>",
        aplicar_filtros
    )

    campo_status_rapido.bind(
        "<Return>",
        lambda evento: (
            atualizar_status_rapido()
        )
    )

    carregar_tabela()
