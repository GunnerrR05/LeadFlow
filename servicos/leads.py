from excel import (
    salvar_lead,
    pegar_leads,
    buscar_lead_por_telefone,
    atualizar_lead as atualizar_lead_excel,
    excluir_lead as excluir_lead_excel,
)
from datetime import date, datetime


CAMPOS_LEAD = (
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
)


def _converter_para_texto(valor):
    """
    Converte o valor recebido para texto.

    Também aceita Entry e Combobox do Tkinter,
    caso algum campo seja enviado diretamente.
    """

    if hasattr(valor, "get") and callable(valor.get):
        valor = valor.get()

    if valor is None:
        return ""

    return str(valor).strip()


def _preparar_lead(campos):
    """
    Cria um dicionário limpo com os campos utilizados pelo sistema.
    """

    if not isinstance(campos, dict):
        raise TypeError(
            "Os dados do lead precisam ser enviados em um dicionário."
        )

    lead = {}

    for campo in CAMPOS_LEAD:
        lead[campo] = _converter_para_texto(
            campos.get(campo, "")
        )

    if not lead["status"]:
        lead["status"] = "EM ANDAMENTO"

    return lead


def _validar_lead(lead):
    """
    Valida os campos obrigatórios.
    """

    if not lead["nome"]:
        raise ValueError("O nome do lead é obrigatório.")

    if not lead["telefone"]:
        raise ValueError("O telefone do lead é obrigatório.")

    if not lead["produto"]:
        raise ValueError("O produto é obrigatório.")


def cadastrar_lead(campos):
    """
    Prepara, valida e salva um novo lead.
    """

    lead = _preparar_lead(campos)

    _validar_lead(lead)

    linha = salvar_lead(lead)

    lead["linha"] = linha

    return lead


def listar_leads():
    """
    Retorna todos os leads cadastrados.
    """

    return pegar_leads()


def buscar_lead(telefone):
    """
    Busca um lead pelo telefone.
    """

    telefone = _converter_para_texto(telefone)

    if not telefone:
        return None

    return buscar_lead_por_telefone(telefone)


def atualizar_lead(lead):
    """
    Atualiza um lead já existente.
    """

    if not isinstance(lead, dict):
        raise TypeError(
            "Os dados do lead precisam ser enviados em um dicionário."
        )

    if "linha" not in lead:
        raise KeyError(
            "O lead precisa possuir a informação da linha."
        )

    lead_atualizado = _preparar_lead(lead)

    lead_atualizado["linha"] = int(lead["linha"])

    if "data_cadastro" in lead:
        lead_atualizado["data_cadastro"] = _converter_para_texto(
            lead["data_cadastro"]
        )

    _validar_lead(lead_atualizado)

    return atualizar_lead_excel(lead_atualizado)


def excluir_lead(lead):
    """
    Exclui um lead usando a linha armazenada no dicionário.

    Também aceita diretamente o número da linha.
    """

    if isinstance(lead, dict):

        if "linha" not in lead:
            raise KeyError(
                "O lead precisa possuir a informação da linha."
            )

        linha = lead["linha"]

    else:
        linha = lead

    return excluir_lead_excel(int(linha))


def _converter_data_proximo_contato(valor):
    """
    Converte o próximo contato para uma data Python.
    Aceita DD/MM/AAAA e DD/MM/AAAA HH:MM.
    """

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    texto = _converter_para_texto(valor)

    if not texto:
        return None

    formatos = (
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
    )

    for formato in formatos:
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
    Separa os leads por data do próximo contato.
    """

    hoje = datetime.now().date()

    grupos = {
        "atrasados": [],
        "hoje": [],
        "proximos": [],
        "invalidos": [],
    }

    for lead in listar_leads():
        data_contato = _converter_data_proximo_contato(
            lead.get("proximo_contato")
        )

        item = lead.copy()

        if data_contato is None:
            grupos["invalidos"].append(item)
            continue

        item["_data_ordenacao"] = data_contato

        if data_contato < hoje:
            grupos["atrasados"].append(item)

        elif data_contato == hoje:
            grupos["hoje"].append(item)

        else:
            grupos["proximos"].append(item)

    def ordenar(item):
        return (
            item["_data_ordenacao"],
            item.get("nome", "").casefold()
        )

    grupos["atrasados"].sort(key=ordenar)
    grupos["hoje"].sort(key=ordenar)
    grupos["proximos"].sort(key=ordenar)

    for nome_grupo in (
        "atrasados",
        "hoje",
        "proximos"
    ):
        for item in grupos[nome_grupo]:
            item.pop("_data_ordenacao", None)

    return grupos