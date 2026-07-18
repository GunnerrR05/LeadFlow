import tkinter as tk
from tkinter import ttk, messagebox

from servicos.leads import obter_followups


COLUNAS = (
    "proximo_contato",
    "nome",
    "telefone",
    "status",
    "produto",
    "cidade_uf",
    "consultor",
)


TITULOS = {
    "proximo_contato": "Próximo Contato",
    "nome": "Nome",
    "telefone": "Telefone",
    "status": "Status",
    "produto": "Produto",
    "cidade_uf": "Cidade / UF",
    "consultor": "Consultor",
}


LARGURAS = {
    "proximo_contato": 140,
    "nome": 190,
    "telefone": 140,
    "status": 210,
    "produto": 190,
    "cidade_uf": 150,
    "consultor": 150,
}


def abrir_followups():
    janela = tk.Toplevel()
    janela.title("Follow-ups")
    janela.geometry("1250x650")

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
        font=("Arial", 22, "bold")
    ).pack(pady=(0, 5))

    label_resumo = ttk.Label(
        container,
        text="",
        font=("Arial", 11)
    )
    label_resumo.pack(pady=(0, 15))

    abas = ttk.Notebook(container)
    abas.pack(
        expand=True,
        fill="both"
    )

    configuracoes = {
        "atrasados": "Atrasados",
        "hoje": "Hoje",
        "proximos": "Próximos",
        "invalidos": "Data Inválida",
    }

    tabelas = {}
    frames = {}

    for chave, titulo in configuracoes.items():
        frame = ttk.Frame(
            abas,
            padding=8
        )

        abas.add(
            frame,
            text=titulo
        )

        frame_tabela = ttk.Frame(frame)
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
            xscrollcommand=barra_horizontal.set
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
                minwidth=90,
                anchor="w",
                stretch=False
            )

        tabelas[chave] = tabela
        frames[chave] = frame

    def carregar():
        try:
            grupos = obter_followups()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar os follow-ups."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        for chave, tabela in tabelas.items():
            for item in tabela.get_children():
                tabela.delete(item)

            for lead in grupos[chave]:
                tabela.insert(
                    "",
                    tk.END,
                    values=(
                        lead.get("proximo_contato", ""),
                        lead.get("nome", ""),
                        lead.get("telefone", ""),
                        lead.get("status", ""),
                        lead.get("produto", ""),
                        lead.get("cidade_uf", ""),
                        lead.get("consultor", ""),
                    )
                )

            abas.tab(
                frames[chave],
                text=(
                    f"{configuracoes[chave]} "
                    f"({len(grupos[chave])})"
                )
            )

        label_resumo.configure(
            text=(
                f"Atrasados: {len(grupos['atrasados'])}    |    "
                f"Hoje: {len(grupos['hoje'])}    |    "
                f"Próximos: {len(grupos['proximos'])}    |    "
                f"Datas inválidas: {len(grupos['invalidos'])}"
            )
        )

    frame_botoes = ttk.Frame(container)
    frame_botoes.pack(pady=(12, 0))

    ttk.Button(
        frame_botoes,
        text="Atualizar",
        command=carregar
    ).pack(
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