import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from servicos.leads import listar_leads


STATUS = [
    "EM ANDAMENTO",
    "NEGOCIAÇÃO",
    "DECLINADO",
    "CONQUISTADO - SUPRIM",
    "CONQUISTADO - EQUIP",
    "FUTURA",
    "CLIENTE ATIVO",
]


def converter_data_cadastro(valor):
    texto = str(valor or "").strip()

    for formato in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
    ):
        try:
            return datetime.strptime(
                texto,
                formato
            ).date()
        except ValueError:
            continue

    return None


def mascara_data(evento):
    campo = evento.widget
    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:8]

    texto = numeros

    if len(numeros) > 2:
        texto = f"{numeros[:2]}/{numeros[2:]}"

    if len(numeros) > 4:
        texto = (
            f"{numeros[:2]}/"
            f"{numeros[2:4]}/"
            f"{numeros[4:]}"
        )

    campo.delete(0, tk.END)
    campo.insert(0, texto)


def filtrar_leads_dashboard(
    leads,
    data_inicial=None,
    data_final=None,
    consultor="TODOS",
):
    consultor = str(consultor or "TODOS").strip()
    resultado = []

    for lead in leads:
        consultor_lead = str(
            lead.get("consultor", "")
            or "NÃO INFORMADO"
        ).strip()

        if (
            consultor != "TODOS"
            and consultor_lead != consultor
        ):
            continue

        if data_inicial is not None or data_final is not None:
            data_cadastro = converter_data_cadastro(
                lead.get("data_cadastro", "")
            )

            if data_cadastro is None:
                continue

            if (
                data_inicial is not None
                and data_cadastro < data_inicial
            ):
                continue

            if (
                data_final is not None
                and data_cadastro > data_final
            ):
                continue

        resultado.append(lead)

    return resultado


def abrir_dashboard():
    janela_dashboard = tk.Toplevel()
    janela_dashboard.title("Dashboard de Leads")
    janela_dashboard.geometry("760x720")
    janela_dashboard.minsize(700, 650)

    container = ttk.Frame(
        janela_dashboard,
        padding=15
    )
    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Dashboard",
        font=("Arial", 18, "bold")
    ).pack(pady=(0, 10))

    estilo = ttk.Style(janela_dashboard)
    estilo.configure(
        "Dashboard.TButton",
        font=("Segoe UI", 10),
        padding=(8, 5)
    )

    frame_filtros = ttk.LabelFrame(
        container,
        text="Filtros do dashboard",
        padding=10
    )
    frame_filtros.pack(
        fill="x",
        pady=(0, 12)
    )

    ttk.Label(
        frame_filtros,
        text="De:"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 5)
    )

    campo_data_inicial = ttk.Entry(
        frame_filtros,
        width=12
    )
    campo_data_inicial.grid(
        row=0,
        column=1,
        sticky="w",
        padx=(0, 12)
    )
    campo_data_inicial.bind(
        "<KeyRelease>",
        mascara_data
    )

    ttk.Label(
        frame_filtros,
        text="Até:"
    ).grid(
        row=0,
        column=2,
        sticky="w",
        padx=(0, 5)
    )

    campo_data_final = ttk.Entry(
        frame_filtros,
        width=12
    )
    campo_data_final.grid(
        row=0,
        column=3,
        sticky="w",
        padx=(0, 12)
    )
    campo_data_final.bind(
        "<KeyRelease>",
        mascara_data
    )

    ttk.Label(
        frame_filtros,
        text="Consultor:"
    ).grid(
        row=0,
        column=4,
        sticky="w",
        padx=(0, 5)
    )

    filtro_consultor = ttk.Combobox(
        frame_filtros,
        values=["TODOS"],
        state="readonly",
        width=20
    )
    filtro_consultor.set("TODOS")
    filtro_consultor.grid(
        row=0,
        column=5,
        sticky="w",
        padx=(0, 12)
    )

    frame_acoes_filtros = ttk.Frame(
        frame_filtros
    )
    frame_acoes_filtros.grid(
        row=0,
        column=6,
        sticky="w"
    )

    ttk.Label(
        frame_filtros,
        text=(
            "Formato: DD/MM/AAAA. "
            "Deixe as duas datas vazias para considerar todos os meses."
        ),
        foreground="#55585C",
        font=("Segoe UI", 9)
    ).grid(
        row=1,
        column=0,
        columnspan=7,
        sticky="w",
        pady=(8, 0)
    )

    frame_resumo = ttk.LabelFrame(
        container,
        text="Resumo do recorte",
        padding=15
    )
    frame_resumo.pack(
        fill="x",
        pady=(0, 15)
    )

    label_total = ttk.Label(
        frame_resumo,
        text="Total de leads: 0",
        font=("Arial", 14, "bold")
    )
    label_total.pack(anchor="w")

    label_conquistados = ttk.Label(
        frame_resumo,
        text="Leads conquistados: 0",
        font=("Arial", 11)
    )
    label_conquistados.pack(
        anchor="w",
        pady=(8, 0)
    )

    label_conversao = ttk.Label(
        frame_resumo,
        text="Taxa de conversão: 0,0%",
        font=("Arial", 11)
    )
    label_conversao.pack(
        anchor="w",
        pady=(5, 0)
    )

    label_filtro_ativo = ttk.Label(
        frame_resumo,
        text="",
        foreground="#4F6F8E",
        font=("Segoe UI", 9, "bold")
    )
    label_filtro_ativo.pack(
        anchor="w",
        pady=(7, 0)
    )

    frame_botoes = ttk.Frame(container)
    frame_botoes.pack(
        side="bottom",
        fill="x",
        pady=(12, 0)
    )

    frame_botoes_central = ttk.Frame(
        frame_botoes
    )
    frame_botoes_central.pack()

    frame_status = ttk.LabelFrame(
        container,
        text="Leads por Status",
        padding=15
    )
    frame_status.pack(
        expand=True,
        fill="both"
    )

    tabela = ttk.Treeview(
        frame_status,
        columns=(
            "status",
            "quantidade"
        ),
        show="headings",
        height=9
    )

    tabela.heading(
        "status",
        text="Status"
    )

    tabela.heading(
        "quantidade",
        text="Quantidade"
    )

    tabela.column(
        "status",
        width=350,
        anchor="w"
    )

    tabela.column(
        "quantidade",
        width=130,
        anchor="center"
    )

    tabela.pack(
        expand=True,
        fill="both"
    )

    def carregar_dashboard():
        texto_data_inicial = campo_data_inicial.get().strip()
        texto_data_final = campo_data_final.get().strip()
        data_inicial = (
            converter_data_cadastro(texto_data_inicial)
            if texto_data_inicial
            else None
        )
        data_final = (
            converter_data_cadastro(texto_data_final)
            if texto_data_final
            else None
        )

        if texto_data_inicial and data_inicial is None:
            messagebox.showwarning(
                "Data inicial inválida",
                "Informe a data inicial no formato DD/MM/AAAA.",
                parent=janela_dashboard
            )
            campo_data_inicial.focus_set()
            return

        if texto_data_final and data_final is None:
            messagebox.showwarning(
                "Data final inválida",
                "Informe a data final no formato DD/MM/AAAA.",
                parent=janela_dashboard
            )
            campo_data_final.focus_set()
            return

        if (
            data_inicial is not None
            and data_final is not None
            and data_inicial > data_final
        ):
            messagebox.showwarning(
                "Período inválido",
                "A data inicial não pode ser posterior à data final.",
                parent=janela_dashboard
            )
            campo_data_inicial.focus_set()
            return

        for item in tabela.get_children():
            tabela.delete(item)

        try:
            todos_leads = listar_leads()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar o dashboard."
                    f"\n\n{erro}"
                ),
                parent=janela_dashboard
            )
            return

        consultores = sorted({
            str(
                lead.get("consultor", "")
                or "NÃO INFORMADO"
            ).strip()
            for lead in todos_leads
        })

        consultor_atual = filtro_consultor.get()
        opcoes_consultores = [
            "TODOS"
        ] + consultores
        filtro_consultor.configure(
            values=opcoes_consultores
        )

        if consultor_atual not in opcoes_consultores:
            consultor_atual = "TODOS"
            filtro_consultor.set(
                consultor_atual
            )

        leads = filtrar_leads_dashboard(
            todos_leads,
            data_inicial=data_inicial,
            data_final=data_final,
            consultor=consultor_atual,
        )

        contagem = {
            status: 0
            for status in STATUS
        }

        for lead in leads:
            status = (
                lead.get("status", "").strip()
                or "EM ANDAMENTO"
            )

            if status not in contagem:
                contagem[status] = 0

            contagem[status] += 1

        total = len(leads)

        conquistados = (
            contagem.get(
                "CONQUISTADO - SUPRIM",
                0
            )
            +
            contagem.get(
                "CONQUISTADO - EQUIP",
                0
            )
        )

        if total > 0:
            taxa_conversao = (
                conquistados / total
            ) * 100

        else:
            taxa_conversao = 0

        label_total.configure(
            text=f"Total de leads: {total}"
        )

        label_conquistados.configure(
            text=(
                "Leads conquistados: "
                f"{conquistados}"
            )
        )

        label_conversao.configure(
            text=(
                "Taxa de conversão: "
                f"{taxa_conversao:.1f}%"
            )
        )

        if data_inicial is None and data_final is None:
            periodo_exibido = "Todos os meses"
        elif data_inicial is None:
            periodo_exibido = (
                "Até "
                f"{data_final.strftime('%d/%m/%Y')}"
            )
        elif data_final is None:
            periodo_exibido = (
                "A partir de "
                f"{data_inicial.strftime('%d/%m/%Y')}"
            )
        else:
            periodo_exibido = (
                f"{data_inicial.strftime('%d/%m/%Y')}"
                " a "
                f"{data_final.strftime('%d/%m/%Y')}"
            )

        label_filtro_ativo.configure(
            text=(
                f"Período: {periodo_exibido}  •  "
                f"Consultor: {consultor_atual}"
            )
        )

        for status, quantidade in contagem.items():
            tabela.insert(
                "",
                tk.END,
                values=(
                    status,
                    quantidade
                )
            )

    def limpar_filtros():
        campo_data_inicial.delete(0, tk.END)
        campo_data_final.delete(0, tk.END)
        filtro_consultor.set(
            "TODOS"
        )
        carregar_dashboard()

    ttk.Button(
        frame_acoes_filtros,
        text="Aplicar",
        command=carregar_dashboard,
        style="Dashboard.TButton",
        width=9
    ).pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_acoes_filtros,
        text="Limpar",
        command=limpar_filtros,
        style="Dashboard.TButton",
        width=9
    ).pack(
        side="left",
        padx=4
    )

    ttk.Button(
        frame_botoes_central,
        text="Atualizar Dados",
        command=carregar_dashboard,
        style="Dashboard.TButton",
        width=14
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        frame_botoes_central,
        text="Fechar",
        command=janela_dashboard.destroy,
        style="Dashboard.TButton",
        width=10
    ).pack(
        side="left",
        padx=5
    )

    carregar_dashboard()
