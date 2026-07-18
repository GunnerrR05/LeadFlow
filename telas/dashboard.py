import tkinter as tk
from tkinter import ttk, messagebox

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


def abrir_dashboard():
    janela_dashboard = tk.Toplevel()
    janela_dashboard.title("Dashboard de Leads")
    janela_dashboard.geometry("650x600")
    janela_dashboard.resizable(False, False)

    container = ttk.Frame(
        janela_dashboard,
        padding=25
    )
    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Dashboard",
        font=("Arial", 22, "bold")
    ).pack(pady=(0, 20))

    frame_resumo = ttk.LabelFrame(
        container,
        text="Resumo Geral",
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
        for item in tabela.get_children():
            tabela.delete(item)

        try:
            leads = listar_leads()

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

        for status, quantidade in contagem.items():
            tabela.insert(
                "",
                tk.END,
                values=(
                    status,
                    quantidade
                )
            )

    frame_botoes = ttk.Frame(container)
    frame_botoes.pack(pady=(15, 0))

    ttk.Button(
        frame_botoes,
        text="Atualizar",
        command=carregar_dashboard
    ).pack(
        side="left",
        padx=5
    )

    ttk.Button(
        frame_botoes,
        text="Fechar",
        command=janela_dashboard.destroy
    ).pack(
        side="left",
        padx=5
    )

    carregar_dashboard()