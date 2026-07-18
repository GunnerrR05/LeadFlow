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

def _mascara_data(evento):
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


def _mascara_data_hora(evento):
    campo = evento.widget

    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:12]

    texto = numeros

    if len(numeros) > 2:
        texto = f"{numeros[:2]}/{numeros[2:]}"

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

    campo.delete(0, tk.END)
    campo.insert(0, texto)


def mascara_telefone(evento):
    campo = evento.widget

    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:11]

    if len(numeros) <= 2:
        texto = f"({numeros}"

    elif len(numeros) <= 6:
        texto = (
            f"({numeros[:2]}) "
            f"{numeros[2:]}"
        )

    elif len(numeros) <= 10:
        texto = (
            f"({numeros[:2]}) "
            f"{numeros[2:6]}-"
            f"{numeros[6:]}"
        )

    else:
        texto = (
            f"({numeros[:2]}) "
            f"{numeros[2:7]}-"
            f"{numeros[7:]}"
        )

    campo.delete(0, tk.END)
    campo.insert(0, texto)


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

        if chave == "telefone":
            campo.bind(
                "<KeyRelease>",
                mascara_telefone
            )

        elif chave == "proximo_contato":
            campo.bind(
                "<KeyRelease>",
                _mascara_data
            )

        elif chave == "ultima_interacao":
            campo.bind(
                "<KeyRelease>",
                _mascara_data_hora
            )

        campos[chave] = campo

    container.columnconfigure(
        1,
        weight=1
    )

    return campos