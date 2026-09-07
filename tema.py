from tkinter import ttk


AZUL = "#4F6F8E"
AZUL_ESCURO = "#3D5871"
PRETO = "#151719"
BRANCO = "#F7F6F3"
CINZA_CLARO = "#E1E0DC"
CINZA_TEXTO = "#55585C"


def aplicar_tema(estilo: ttk.Style) -> None:
    """Aplica a identidade visual usada na carteira de leads."""

    if "clam" in estilo.theme_names():
        estilo.theme_use("clam")

    estilo.configure(
        ".",
        font=("Segoe UI", 10),
        background=CINZA_CLARO,
        foreground=PRETO,
    )

    estilo.configure("TFrame", background=CINZA_CLARO)
    estilo.configure(
        "TLabel",
        background=CINZA_CLARO,
        foreground=PRETO,
    )
    estilo.configure(
        "Titulo.TLabel",
        font=("Segoe UI", 24, "bold"),
        foreground=PRETO,
    )
    estilo.configure(
        "Subtitulo.TLabel",
        font=("Segoe UI", 11),
        foreground=AZUL,
    )

    for nome_estilo, fonte, preenchimento in (
        ("TButton", ("Segoe UI", 10), (10, 7)),
        ("Menu.TButton", ("Segoe UI", 11), 10),
    ):
        estilo.configure(
            nome_estilo,
            font=fonte,
            padding=preenchimento,
            background=CINZA_CLARO,
            foreground=PRETO,
            bordercolor="#A6A49E",
            lightcolor="#A6A49E",
            darkcolor="#A6A49E",
            borderwidth=1,
            relief="solid",
            focusthickness=1,
            focuscolor="#888680",
        )
        estilo.map(
            nome_estilo,
            background=[
                ("disabled", "#DCDAD5"),
                ("pressed", "#CAC8C2"),
                ("active", "#D5D3CE"),
            ],
            foreground=[
                ("disabled", "#8A8985"),
                ("pressed", PRETO),
                ("active", PRETO),
            ],
            bordercolor=[
                ("disabled", "#BBB9B3"),
                ("pressed", "#888680"),
                ("active", "#94928C"),
            ],
            lightcolor=[
                ("disabled", "#BBB9B3"),
                ("pressed", "#888680"),
                ("active", "#94928C"),
            ],
            darkcolor=[
                ("disabled", "#BBB9B3"),
                ("pressed", "#888680"),
                ("active", "#94928C"),
            ],
        )

    estilo.configure(
        "TEntry",
        fieldbackground=BRANCO,
        foreground=PRETO,
        bordercolor="#AAA8A2",
        lightcolor="#AAA8A2",
        darkcolor="#AAA8A2",
    )
    estilo.configure(
        "TCombobox",
        fieldbackground=BRANCO,
        foreground=PRETO,
        arrowcolor=CINZA_TEXTO,
    )
    estilo.configure(
        "Treeview",
        background="#FBFAF8",
        fieldbackground="#FBFAF8",
        foreground=PRETO,
        rowheight=28,
    )
    estilo.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#292B2E",
        foreground=BRANCO,
        relief="flat",
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#71869A")],
        foreground=[("selected", BRANCO)],
    )
    estilo.map(
        "Treeview.Heading",
        background=[("active", "#4F5860")],
        foreground=[("active", BRANCO)],
    )


def aplicar_tema_carteira(estilo: ttk.Style) -> None:
    """Aplica o visual do Zarken somente aos estilos da carteira."""

    estilo.configure(
        "Carteira.TFrame",
        background=CINZA_CLARO,
    )
    estilo.configure(
        "Carteira.TLabel",
        font=("Segoe UI", 10),
        background=CINZA_CLARO,
        foreground=PRETO,
    )
    estilo.configure(
        "Carteira.TLabelframe",
        background=CINZA_CLARO,
        foreground=PRETO,
    )
    estilo.configure(
        "Carteira.TLabelframe.Label",
        font=("Segoe UI", 10),
        background=CINZA_CLARO,
        foreground=PRETO,
    )
    estilo.configure(
        "Carteira.TButton",
        font=("Segoe UI", 10),
        padding=(10, 7),
        background=CINZA_CLARO,
        foreground=PRETO,
        bordercolor="#A6A49E",
        lightcolor="#A6A49E",
        darkcolor="#A6A49E",
        borderwidth=1,
        relief="solid",
        focusthickness=1,
        focuscolor="#888680",
    )
    estilo.map(
        "Carteira.TButton",
        background=[
            ("disabled", "#DCDAD5"),
            ("pressed", "#CAC8C2"),
            ("active", "#D5D3CE"),
        ],
        foreground=[
            ("disabled", "#8A8985"),
            ("pressed", PRETO),
            ("active", PRETO),
        ],
        bordercolor=[
            ("disabled", "#BBB9B3"),
            ("pressed", "#888680"),
            ("active", "#94928C"),
        ],
        lightcolor=[
            ("disabled", "#BBB9B3"),
            ("pressed", "#888680"),
            ("active", "#94928C"),
        ],
        darkcolor=[
            ("disabled", "#BBB9B3"),
            ("pressed", "#888680"),
            ("active", "#94928C"),
        ],
    )
    estilo.configure(
        "Carteira.TEntry",
        font=("Segoe UI", 10),
        fieldbackground=BRANCO,
        foreground=PRETO,
        bordercolor="#AAA8A2",
        lightcolor="#AAA8A2",
        darkcolor="#AAA8A2",
    )
    estilo.configure(
        "Carteira.TCombobox",
        font=("Segoe UI", 10),
        fieldbackground=BRANCO,
        foreground=PRETO,
        arrowcolor=CINZA_TEXTO,
    )
    estilo.configure(
        "Carteira.Treeview",
        font=("Segoe UI", 10),
        background="#FBFAF8",
        fieldbackground="#FBFAF8",
        foreground=PRETO,
        rowheight=28,
    )
    estilo.configure(
        "Carteira.Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#292B2E",
        foreground=BRANCO,
        relief="flat",
    )
    estilo.map(
        "Carteira.Treeview",
        background=[("selected", "#71869A")],
        foreground=[("selected", BRANCO)],
    )
    estilo.map(
        "Carteira.Treeview.Heading",
        background=[("active", "#4F5860")],
        foreground=[("active", BRANCO)],
    )
