from datetime import date, datetime
import re
import unicodedata

from excel import (
    salvar_lead,
    pegar_leads,
    atualizar_lead as atualizar_lead_excel,
    excluir_lead as excluir_lead_excel,
)


CAMPOS_LEAD = (
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
)


UNIDADES = [
    "AMERICANA",
    "GOIÂNIA",
    "SANTA CATARINA",
    "SANTO ANDRÉ",
    "TAUBATÉ",
]


def _converter_para_texto(valor):
    """
    Converte o valor recebido para texto.

    Também aceita Entry e Combobox
    do Tkinter.
    """

    if (
        hasattr(valor, "get")
        and callable(valor.get)
    ):
        valor = valor.get()

    if valor is None:
        return ""

    return str(valor).strip()


def _normalizar_texto(valor):
    """
    Remove acentos e converte para maiúsculas.

    Exemplo:
    NÃO INFORMADO -> NAO INFORMADO
    """

    texto = _converter_para_texto(
        valor
    ).upper()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(
            caractere
        ) != "Mn"
    )


UNIDADES_NORMALIZADAS = {
    _normalizar_texto(
        unidade
    ): unidade
    for unidade in UNIDADES
}


def _normalizar_telefone(valor):
    """
    Mantém apenas os números
    do telefone.
    """

    texto = _converter_para_texto(
        valor
    )

    return "".join(
        caractere
        for caractere in texto
        if caractere.isdigit()
    )


def _validar_telefone(valor):
    numeros = _normalizar_telefone(
        valor
    )

    if len(numeros) in (
        10,
        11,
    ):
        return

    if (
        len(numeros) in (
            12,
            13,
        )
        and numeros.startswith(
            "55"
        )
    ):
        return

    raise ValueError(
        "Telefone inválido. Informe o DDD e "
        "um telefone com 10 ou 11 números."
    )


def _validar_email(valor):
    email = _converter_para_texto(
        valor
    )

    # Mantém compatibilidade com leads antigos
    # que não possuem e-mail preenchido.
    if not email:
        return

    email_normalizado = (
        _normalizar_texto(
            email
        )
    )

    if email_normalizado == "NAO INFORMADO":
        return

    if (
        email_normalizado
        == "ESCREVER E-MAIL MANUALMENTE"
    ):
        raise ValueError(
            "Digite o endereço de e-mail ou "
            "selecione NÃO INFORMADO."
        )

    padrao = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    if not re.fullmatch(
        padrao,
        email
    ):
        raise ValueError(
            "E-mail inválido. Digite um endereço "
            "válido ou selecione NÃO INFORMADO."
        )


def _validar_unidade(valor):
    unidade = _converter_para_texto(
        valor
    )

    # Os leads antigos ficarão inicialmente
    # sem unidade após a migração.
    if not unidade:
        return

    unidade_normalizada = (
        _normalizar_texto(
            unidade
        )
    )

    if (
        unidade_normalizada
        not in UNIDADES_NORMALIZADAS
    ):
        raise ValueError(
            "Unidade inválida. Selecione uma "
            "das unidades disponíveis."
        )


def _validar_data(
    valor,
    nome_campo,
    formatos
):
    """
    Valida uma data usando os formatos
    permitidos.

    Campo vazio continua permitido.
    """

    if not valor:
        return

    for formato in formatos:
        try:
            datetime.strptime(
                valor,
                formato
            )
            return

        except ValueError:
            continue

    formatos_legiveis = " ou ".join(
        formato
        .replace(
            "%d",
            "DD"
        )
        .replace(
            "%m",
            "MM"
        )
        .replace(
            "%Y",
            "AAAA"
        )
        .replace(
            "%H",
            "HH"
        )
        .replace(
            "%M",
            "MM"
        )
        for formato in formatos
    )

    raise ValueError(
        f"{nome_campo} inválido. "
        f"Use o formato {formatos_legiveis}."
    )


def _preparar_lead(campos):
    """
    Cria um dicionário limpo com os
    campos utilizados pelo sistema.
    """

    if not isinstance(
        campos,
        dict
    ):
        raise TypeError(
            "Os dados do lead precisam ser "
            "enviados em um dicionário."
        )

    lead = {}

    for campo in CAMPOS_LEAD:
        lead[campo] = (
            _converter_para_texto(
                campos.get(
                    campo,
                    ""
                )
            )
        )

    if not lead["status"]:
        lead["status"] = (
            "EM ANDAMENTO"
        )

    lead["status"] = (
        lead["status"].upper()
    )

    # Corrige a ortografia da unidade,
    # inclusive quando vier sem acento.
    unidade_normalizada = (
        _normalizar_texto(
            lead["unidade"]
        )
    )

    if (
        unidade_normalizada
        in UNIDADES_NORMALIZADAS
    ):
        lead["unidade"] = (
            UNIDADES_NORMALIZADAS[
                unidade_normalizada
            ]
        )

    # Padroniza a opção sem e-mail.
    if (
        _normalizar_texto(
            lead["email"]
        )
        == "NAO INFORMADO"
    ):
        lead["email"] = (
            "NÃO INFORMADO"
        )

    # Regra central:
    # lead declinado não terá
    # próximo contato.
    if (
        lead["status"]
        == "DECLINADO"
    ):
        lead[
            "proximo_contato"
        ] = ""

    return lead


def _validar_lead(lead):
    """
    Valida os campos obrigatórios,
    telefone, e-mail, unidade e datas.
    """

    if not lead["nome"]:
        raise ValueError(
            "O nome do lead é obrigatório."
        )

    if not lead["telefone"]:
        raise ValueError(
            "O telefone do lead é obrigatório."
        )

    if not lead["produto"]:
        raise ValueError(
            "O produto é obrigatório."
        )

    _validar_telefone(
        lead["telefone"]
    )

    _validar_email(
        lead["email"]
    )

    _validar_unidade(
        lead["unidade"]
    )

    _validar_data(
        lead[
            "proximo_contato"
        ],
        "Próximo contato",
        (
            "%d/%m/%Y",
        )
    )

    _validar_data(
        lead[
            "ultima_interacao"
        ],
        "Última interação",
        (
            "%d/%m/%Y",
            "%d/%m/%Y %H:%M",
        )
    )


def cadastrar_lead(campos):
    """
    Prepara, valida e salva um novo lead.

    Impede telefones duplicados.
    """

    lead = _preparar_lead(
        campos
    )

    _validar_lead(
        lead
    )

    telefone_novo = (
        _normalizar_telefone(
            lead["telefone"]
        )
    )

    for lead_existente in (
        pegar_leads()
    ):
        telefone_existente = (
            _normalizar_telefone(
                lead_existente.get(
                    "telefone",
                    ""
                )
            )
        )

        if (
            telefone_existente
            == telefone_novo
        ):
            raise ValueError(
                "Já existe um lead cadastrado "
                "com esse telefone."
            )

    linha = salvar_lead(
        lead
    )

    lead["linha"] = linha

    return lead


def listar_leads():
    """
    Retorna todos os leads cadastrados.
    """

    return pegar_leads()


def buscar_lead(telefone):
    """
    Busca um lead pelo telefone,
    ignorando a formatação.
    """

    telefone_procurado = (
        _normalizar_telefone(
            telefone
        )
    )

    if not telefone_procurado:
        return None

    for lead in pegar_leads():
        telefone_lead = (
            _normalizar_telefone(
                lead.get(
                    "telefone",
                    ""
                )
            )
        )

        if (
            telefone_lead
            == telefone_procurado
        ):
            return lead

    return None


def atualizar_lead(lead):
    """
    Atualiza um lead existente e
    impede telefone duplicado.
    """

    if not isinstance(
        lead,
        dict
    ):
        raise TypeError(
            "Os dados do lead precisam ser "
            "enviados em um dicionário."
        )

    if "linha" not in lead:
        raise KeyError(
            "O lead precisa possuir "
            "a informação da linha."
        )

    linha_atual = int(
        lead["linha"]
    )

    lead_atualizado = (
        _preparar_lead(
            lead
        )
    )

    lead_atualizado[
        "linha"
    ] = linha_atual

    if "data_cadastro" in lead:
        lead_atualizado[
            "data_cadastro"
        ] = (
            _converter_para_texto(
                lead[
                    "data_cadastro"
                ]
            )
        )

    _validar_lead(
        lead_atualizado
    )

    telefone_novo = (
        _normalizar_telefone(
            lead_atualizado[
                "telefone"
            ]
        )
    )

    for lead_existente in (
        pegar_leads()
    ):
        linha_existente = int(
            lead_existente[
                "linha"
            ]
        )

        telefone_existente = (
            _normalizar_telefone(
                lead_existente.get(
                    "telefone",
                    ""
                )
            )
        )

        if (
            linha_existente
            != linha_atual
            and telefone_existente
            == telefone_novo
        ):
            raise ValueError(
                "Já existe outro lead cadastrado "
                "com esse telefone."
            )

    return atualizar_lead_excel(
        lead_atualizado
    )


def excluir_lead(lead):
    """
    Exclui um lead usando a linha
    armazenada no dicionário.

    Também aceita diretamente
    o número da linha.
    """

    if isinstance(
        lead,
        dict
    ):
        if "linha" not in lead:
            raise KeyError(
                "O lead precisa possuir "
                "a informação da linha."
            )

        linha = lead["linha"]

    else:
        linha = lead

    return excluir_lead_excel(
        int(linha)
    )


def _converter_data_proximo_contato(
    valor
):
    """
    Converte o próximo contato
    para uma data Python.
    """

    if isinstance(
        valor,
        datetime
    ):
        return valor.date()

    if isinstance(
        valor,
        date
    ):
        return valor

    texto = _converter_para_texto(
        valor
    )

    if not texto:
        return None

    for formato in (
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
    ):
        try:
            return datetime.strptime(
                texto,
                formato
            ).date()

        except ValueError:
            continue

    return None


def obter_followups():
    """
    Separa os leads por data
    do próximo contato.

    Leads declinados ficam em Finalizado.

    Leads ativos sem data não aparecem
    no Follow-up.
    """

    hoje = datetime.now().date()

    grupos = {
        "atrasados": [],
        "hoje": [],
        "proximos": [],
        "finalizados": [],
        "invalidos": [],
    }

    for lead in listar_leads():
        item = lead.copy()

        status = (
            _converter_para_texto(
                lead.get(
                    "status",
                    ""
                )
            ).upper()
        )

        # Declinado sempre aparece
        # na aba Finalizado.
        if status == "DECLINADO":
            grupos[
                "finalizados"
            ].append(
                item
            )
            continue

        valor_proximo_contato = (
            _converter_para_texto(
                lead.get(
                    "proximo_contato",
                    ""
                )
            )
        )

        # A aba Sem Data foi removida.
        # Leads ativos sem data ficam fora
        # da tela de Follow-up.
        if not valor_proximo_contato:
            continue

        data_contato = (
            _converter_data_proximo_contato(
                valor_proximo_contato
            )
        )

        if data_contato is None:
            grupos[
                "invalidos"
            ].append(
                item
            )
            continue

        item[
            "_data_ordenacao"
        ] = data_contato

        if data_contato < hoje:
            grupos[
                "atrasados"
            ].append(
                item
            )

        elif data_contato == hoje:
            grupos[
                "hoje"
            ].append(
                item
            )

        else:
            grupos[
                "proximos"
            ].append(
                item
            )

    def ordenar_por_data(item):
        return (
            item[
                "_data_ordenacao"
            ],
            _converter_para_texto(
                item.get(
                    "nome",
                    ""
                )
            ).casefold()
        )

    for nome_grupo in (
        "atrasados",
        "hoje",
        "proximos",
    ):
        grupos[
            nome_grupo
        ].sort(
            key=ordenar_por_data
        )

        for item in grupos[
            nome_grupo
        ]:
            item.pop(
                "_data_ordenacao",
                None
            )

    grupos[
        "finalizados"
    ].sort(
        key=lambda item: (
            _converter_para_texto(
                item.get(
                    "nome",
                    ""
                )
            ).casefold()
        )
    )

    grupos[
        "invalidos"
    ].sort(
        key=lambda item: (
            _converter_para_texto(
                item.get(
                    "nome",
                    ""
                )
            ).casefold()
        )
    )

    return grupos