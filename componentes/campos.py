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


UNIDADES = [
    "AMERICANA",
    "GOIÂNIA",
    "SANTA CATARINA",
    "SANTO ANDRÉ",
    "TAUBATÉ",
]


OPCAO_EMAIL_MANUAL = (
    "ESCREVER E-MAIL MANUALMENTE"
)

OPCAO_EMAIL_NAO_INFORMADO = (
    "NÃO INFORMADO"
)


OPCOES_EMAIL = [
    OPCAO_EMAIL_MANUAL,
    OPCAO_EMAIL_NAO_INFORMADO,
]


CAMPOS_CADASTRO = [
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


def _mascara_data(evento):
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


def _mascara_data_hora(evento):
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


def mascara_telefone(evento):
    campo = evento.widget

    numeros = "".join(
        caractere
        for caractere in campo.get()
        if caractere.isdigit()
    )[:11]

    if len(numeros) <= 2:
        texto = (
            f"({numeros}"
        )

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

    campo.delete(
        0,
        tk.END
    )

    campo.insert(
        0,
        texto
    )


def inserir_quebra_linha(evento):
    evento.widget.insert(
        tk.INSERT,
        "\n"
    )

    return "break"


def criar_campos(janela):
    """
    Cria e retorna os campos utilizados
    na tela de cadastro.
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

    for numero_linha, (
        texto,
        chave
    ) in enumerate(
        CAMPOS_CADASTRO,
        start=1
    ):
        ttk.Label(
            container,
            text=f"{texto}:"
        ).grid(
            row=numero_linha,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=6
        )

        if chave == "unidade":
            campo = ttk.Combobox(
                container,
                values=UNIDADES,
                state="readonly",
                width=32
            )

            campo.set("")

        elif chave == "status":
            campo = ttk.Combobox(
                container,
                values=STATUS,
                state="readonly",
                width=32
            )

            campo.set(
                "EM ANDAMENTO"
            )

        elif chave == "email":
            campo = ttk.Combobox(
                container,
                values=OPCOES_EMAIL,
                state="normal",
                width=32
            )

            campo.set(
                OPCAO_EMAIL_NAO_INFORMADO
            )

        elif chave == "aplicacao":
            campo = ttk.Combobox(
                container,
                values=APLICACOES,
                state="readonly",
                width=32
            )

            campo.set(
                APLICACOES[0]
            )

        elif chave == "observacao":
            campo = tk.Text(
                container,
                width=40,
                height=4,
                wrap="word"
            )

            campo.bind(
                "<Shift-Return>",
                inserir_quebra_linha
            )

        else:
            campo = ttk.Entry(
                container,
                width=40
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

    def verificar_status(evento=None):
        """
        Limpa o próximo contato quando
        o status for DECLINADO.
        """

        status = (
            campos["status"]
            .get()
            .strip()
            .upper()
        )

        if status == "DECLINADO":
            campos[
                "proximo_contato"
            ].delete(
                0,
                tk.END
            )

    def selecionar_opcao_email(
        evento=None
    ):
        """
        Ao escolher a opção de escrever
        manualmente, limpa o combobox e
        posiciona o cursor para digitação.
        """

        opcao = (
            campos["email"]
            .get()
            .strip()
        )

        if (
            opcao
            == OPCAO_EMAIL_MANUAL
        ):
            campos[
                "email"
            ].set("")

            campos[
                "email"
            ].focus_set()

            campos[
                "email"
            ].icursor(
                tk.END
            )

        elif (
            opcao
            == OPCAO_EMAIL_NAO_INFORMADO
        ):
            campos[
                "email"
            ].set(
                OPCAO_EMAIL_NAO_INFORMADO
            )

    campos["status"].bind(
        "<<ComboboxSelected>>",
        verificar_status
    )

    campos["email"].bind(
        "<<ComboboxSelected>>",
        selecionar_opcao_email
    )

    container.columnconfigure(
        1,
        weight=1
    )

    return campos