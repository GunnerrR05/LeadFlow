import tkinter as tk
from tkinter import ttk


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


CAMPOS_CADASTRO = [
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


def criar_campos(janela):
    """
    Cria os campos usados na tela de cadastro.

    Retorna um dicionário no formato:
    {
        "nome": Entry,
        "telefone": Entry,
        "status": Combobox,
        ...
    }
    """

    campos = {}

    container = ttk.Frame(
        janela,
        padding=20
    )

    container.pack(
        expand=True,
        fill="both"
    )

    ttk.Label(
        container,
        text="Novo Lead",
        font=("Arial", 18, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(0, 15)
    )

    for numero_linha, (texto, chave) in enumerate(
        CAMPOS_CADASTRO,
        start=1
    ):
        label = ttk.Label(
            container,
            text=f"{texto}:"
        )

        label.grid(
            row=numero_linha,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=6
        )

        if chave == "status":
            campo = ttk.Combobox(
                container,
                values=STATUS,
                state="readonly",
                width=32
            )

            campo.set("EM ANDAMENTO")

        elif chave == "aplicacao":
            campo = ttk.Combobox(
                container,
                values=APLICACOES,
                state="readonly",
                width=32
            )

            campo.set(APLICACOES[0])

        else:
            campo = ttk.Entry(
                container,
                width=35
            )

        campo.grid(
            row=numero_linha,
            column=1,
            sticky="ew",
            pady=6
        )

        campos[chave] = campo

    container.columnconfigure(
        1,
        weight=1
    )

    return campos