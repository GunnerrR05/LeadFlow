import os
from datetime import date, datetime

from openpyxl import Workbook, load_workbook


ARQUIVO_LEADS = "leads.xlsx"

CABECALHOS = [
    "DATA DE CADASTRO",
    "PRÓXIMO CONTATO",
    "ÚLTIMA INTERAÇÃO",
    "STATUS",
    "TELEFONE",
    "NOME",
    "PRODUTO",
    "CIDADE / UF",
    "E-MAIL",
    "APLICAÇÃO",
    "ORIGEM",
    "CONSULTOR",
    "OBSERVAÇÃO",
    "RESUMO",
    "NOME NO WHATSAPP",
]

STATUS_VALIDOS = [
    "EM ANDAMENTO",
    "NEGOCIAÇÃO",
    "DECLINADO",
    "CONQUISTADO - SUPRIM",
    "CONQUISTADO - EQUIP",
    "FUTURA",
    "CLIENTE ATIVO",
]


def _valor(campo):
    """
    Aceita tanto texto comum quanto objetos Entry e Combobox do Tkinter.
    """

    if hasattr(campo, "get") and callable(campo.get):
        campo = campo.get()

    if campo is None:
        return ""

    return str(campo).strip()


def _abrir_planilha():
    """
    Abre a planilha. Caso não exista, cria automaticamente.
    """

    if not os.path.exists(ARQUIVO_LEADS):
        criar_planilha()

    arquivo = load_workbook(ARQUIVO_LEADS)
    planilha = arquivo.active

    return arquivo, planilha


def _gerar_resumo(dados):
    """
    Formato:
    NOME - TELEFONE - ORIGEM - PRODUTO
    """

    return (
        f"{dados['nome']} - "
        f"{dados['telefone']} - "
        f"{dados['origem']} - "
        f"{dados['produto']}"
    )


def _gerar_nome_whatsapp(dados):
    """
    Formato:
    LEAD - NOME - PRODUTO - CIDADE / UF - ORIGEM
    """

    return (
        f"LEAD - "
        f"{dados['nome']} - "
        f"{dados['produto']} - "
        f"{dados['cidade_uf']} - "
        f"{dados['origem']}"
    )


def _lead_da_linha(planilha, linha):
    """
    Transforma uma linha do Excel em um dicionário de lead.
    """

    return {
        "linha": linha,
        "data_cadastro": planilha[f"A{linha}"].value or "",
        "proximo_contato": planilha[f"B{linha}"].value or "",
        "ultima_interacao": planilha[f"C{linha}"].value or "",
        "status": planilha[f"D{linha}"].value or "EM ANDAMENTO",
        "telefone": planilha[f"E{linha}"].value or "",
        "nome": planilha[f"F{linha}"].value or "",
        "produto": planilha[f"G{linha}"].value or "",
        "cidade_uf": planilha[f"H{linha}"].value or "",
        "email": planilha[f"I{linha}"].value or "",
        "aplicacao": planilha[f"J{linha}"].value or "",
        "origem": planilha[f"K{linha}"].value or "",
        "consultor": planilha[f"L{linha}"].value or "",
        "observacao": planilha[f"M{linha}"].value or "",
        "resumo": planilha[f"N{linha}"].value or "",
        "whatsapp": planilha[f"O{linha}"].value or "",
    }


def criar_planilha():
    """
    Cria leads.xlsx somente quando o arquivo ainda não existe.
    Não sobrescreve uma planilha existente.
    """

    if os.path.exists(ARQUIVO_LEADS):
        return False

    workbook = Workbook()
    planilha = workbook.active
    planilha.title = "Leads"

    for coluna, cabecalho in enumerate(CABECALHOS, start=1):
        planilha.cell(
            row=1,
            column=coluna,
            value=cabecalho
        )

    larguras = {
        "A": 20,
        "B": 18,
        "C": 20,
        "D": 24,
        "E": 16,
        "F": 24,
        "G": 24,
        "H": 18,
        "I": 28,
        "J": 24,
        "K": 18,
        "L": 18,
        "M": 35,
        "N": 55,
        "O": 65,
    }

    for coluna, largura in larguras.items():
        planilha.column_dimensions[coluna].width = largura

    planilha.freeze_panes = "A2"
    planilha.auto_filter.ref = "A1:O1"

    workbook.save(ARQUIVO_LEADS)

    return True


def salvar_lead(lead):
    """
    Salva um novo lead na próxima linha vazia da planilha.
    """

    arquivo, planilha = _abrir_planilha()

    linha_vazia = planilha.max_row + 1

    dados = {
        "proximo_contato": _valor(
            lead.get("proximo_contato", "")
        ),
        "ultima_interacao": _valor(
            lead.get("ultima_interacao", "")
        ),
        "status": (
            _valor(lead.get("status", ""))
            or "EM ANDAMENTO"
        ),
        "telefone": _valor(
            lead.get("telefone", "")
        ),
        "nome": _valor(
            lead.get("nome", "")
        ),
        "produto": _valor(
            lead.get(
                "produto",
                lead.get("interesse", "")
            )
        ),
        "cidade_uf": _valor(
            lead.get("cidade_uf", "")
        ),
        "email": _valor(
            lead.get("email", "")
        ),
        "aplicacao": _valor(
            lead.get("aplicacao", "")
        ),
        "origem": _valor(
            lead.get("origem", "")
        ),
        "consultor": _valor(
            lead.get("consultor", "")
        ),
        "observacao": _valor(
            lead.get("observacao", "")
        ),
    }

    data_cadastro = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    resumo = _gerar_resumo(dados)
    nome_whatsapp = _gerar_nome_whatsapp(dados)

    valores = [
        data_cadastro,
        dados["proximo_contato"],
        dados["ultima_interacao"],
        dados["status"],
        dados["telefone"],
        dados["nome"],
        dados["produto"],
        dados["cidade_uf"],
        dados["email"],
        dados["aplicacao"],
        dados["origem"],
        dados["consultor"],
        dados["observacao"],
        resumo,
        nome_whatsapp,
    ]

    for coluna, valor in enumerate(valores, start=1):
        planilha.cell(
            row=linha_vazia,
            column=coluna,
            value=valor
        )

    arquivo.save(ARQUIVO_LEADS)

    return linha_vazia


def pegar_leads():
    """
    Retorna todos os leads da planilha em uma lista.
    """

    arquivo, planilha = _abrir_planilha()

    leads = []

    for linha in range(2, planilha.max_row + 1):

        telefone = planilha[f"E{linha}"].value
        nome = planilha[f"F{linha}"].value

        if telefone is None and nome is None:
            continue

        lead = _lead_da_linha(
            planilha,
            linha
        )

        leads.append(lead)

    return leads


def listar_leads():
    """
    Mantida para compatibilidade com o main.py antigo.
    A interface gráfica utiliza pegar_leads().
    """

    leads = pegar_leads()

    for numero, lead in enumerate(leads, start=1):

        print(f"\nLEAD {numero}")

        print(
            f"Data de cadastro: "
            f"{lead['data_cadastro']}"
        )

        print(
            f"Próximo contato: "
            f"{lead['proximo_contato']}"
        )

        print(
            f"Última interação: "
            f"{lead['ultima_interacao']}"
        )

        print(f"Status: {lead['status']}")
        print(f"Telefone: {lead['telefone']}")
        print(f"Nome: {lead['nome']}")
        print(f"Produto: {lead['produto']}")
        print(f"Cidade / UF: {lead['cidade_uf']}")
        print(f"E-mail: {lead['email']}")
        print(f"Aplicação: {lead['aplicacao']}")
        print(f"Origem: {lead['origem']}")
        print(f"Consultor: {lead['consultor']}")
        print(f"Observação: {lead['observacao']}")
        print(f"Resumo: {lead['resumo']}")

        print(
            f"Nome no WhatsApp: "
            f"{lead['whatsapp']}"
        )

    return leads


def buscar_lead_por_nome(nome_busca):
    """
    Busca pelo nome e retorna o número da linha do Excel.
    """

    arquivo, planilha = _abrir_planilha()

    nome_procurado = _valor(
        nome_busca
    ).casefold()

    for linha in range(2, planilha.max_row + 1):

        nome = _valor(
            planilha[f"F{linha}"].value
        )

        if nome.casefold() == nome_procurado:
            return linha

    return None


def buscar_lead_por_telefone(telefone_busca):
    """
    Busca um lead pelo telefone e retorna o dicionário completo.
    """

    arquivo, planilha = _abrir_planilha()

    telefone_procurado = _valor(
        telefone_busca
    )

    for linha in range(2, planilha.max_row + 1):

        telefone = _valor(
            planilha[f"E{linha}"].value
        )

        if telefone == telefone_procurado:

            return _lead_da_linha(
                planilha,
                linha
            )

    return None


def atualizar_lead(lead):
    """
    Atualiza um lead existente pela chave 'linha'.
    O resumo e o nome do WhatsApp são recriados automaticamente.
    """

    arquivo, planilha = _abrir_planilha()

    if "linha" not in lead:
        raise KeyError(
            "O lead precisa possuir a chave 'linha'."
        )

    linha = int(lead["linha"])

    if linha < 2 or linha > planilha.max_row:
        raise ValueError(
            "Linha do lead inválida."
        )

    atual = _lead_da_linha(
        planilha,
        linha
    )

    dados = {
        "data_cadastro": (
            _valor(
                lead.get(
                    "data_cadastro",
                    lead.get(
                        "data",
                        atual["data_cadastro"]
                    )
                )
            )
            or _valor(atual["data_cadastro"])
        ),

        "proximo_contato": _valor(
            lead.get(
                "proximo_contato",
                atual["proximo_contato"]
            )
        ),

        "ultima_interacao": _valor(
            lead.get(
                "ultima_interacao",
                atual["ultima_interacao"]
            )
        ),

        "status": (
            _valor(
                lead.get(
                    "status",
                    atual["status"]
                )
            )
            or "EM ANDAMENTO"
        ),

        "telefone": _valor(
            lead.get(
                "telefone",
                atual["telefone"]
            )
        ),

        "nome": _valor(
            lead.get(
                "nome",
                atual["nome"]
            )
        ),

        "produto": _valor(
            lead.get(
                "produto",
                lead.get(
                    "interesse",
                    atual["produto"]
                )
            )
        ),

        "cidade_uf": _valor(
            lead.get(
                "cidade_uf",
                atual["cidade_uf"]
            )
        ),

        "email": _valor(
            lead.get(
                "email",
                atual["email"]
            )
        ),

        "aplicacao": _valor(
            lead.get(
                "aplicacao",
                atual["aplicacao"]
            )
        ),

        "origem": _valor(
            lead.get(
                "origem",
                atual["origem"]
            )
        ),

        "consultor": _valor(
            lead.get(
                "consultor",
                atual["consultor"]
            )
        ),

        "observacao": _valor(
            lead.get(
                "observacao",
                atual["observacao"]
            )
        ),
    }

    resumo = _gerar_resumo(dados)
    nome_whatsapp = _gerar_nome_whatsapp(dados)

    valores = [
        dados["data_cadastro"],
        dados["proximo_contato"],
        dados["ultima_interacao"],
        dados["status"],
        dados["telefone"],
        dados["nome"],
        dados["produto"],
        dados["cidade_uf"],
        dados["email"],
        dados["aplicacao"],
        dados["origem"],
        dados["consultor"],
        dados["observacao"],
        resumo,
        nome_whatsapp,
    ]

    for coluna, valor in enumerate(valores, start=1):

        planilha.cell(
            row=linha,
            column=coluna,
            value=valor
        )

    arquivo.save(ARQUIVO_LEADS)

    dados["linha"] = linha
    dados["resumo"] = resumo
    dados["whatsapp"] = nome_whatsapp

    return dados


def excluir_lead(linha):
    """
    Exclui uma linha do Excel.
    """

    arquivo, planilha = _abrir_planilha()

    linha = int(linha)

    if linha < 2 or linha > planilha.max_row:
        raise ValueError(
            "Linha do lead inválida."
        )

    planilha.delete_rows(linha)

    arquivo.save(ARQUIVO_LEADS)

    return True


def atualizar_status(telefone, novo_status):
    """
    Atualiza o status pelo telefone.
    Também registra o momento na coluna Última Interação.
    """

    arquivo, planilha = _abrir_planilha()

    telefone_procurado = _valor(telefone)
    status_novo = _valor(novo_status)

    for linha in range(2, planilha.max_row + 1):

        telefone_planilha = _valor(
            planilha[f"E{linha}"].value
        )

        if telefone_planilha == telefone_procurado:

            planilha[f"D{linha}"] = status_novo

            planilha[f"C{linha}"] = (
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

            arquivo.save(ARQUIVO_LEADS)

            return True

    return False


def dashboard():
    """
    Mostra a quantidade de leads por status.
    """

    leads = pegar_leads()

    contagem = {
        status: 0
        for status in STATUS_VALIDOS
    }

    for lead in leads:

        status = (
            _valor(lead.get("status"))
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

    print("\n===== DASHBOARD =====")
    print(f"Total de leads: {total}")

    for status, quantidade in contagem.items():
        print(f"{status}: {quantidade}")

    print(
        f"Taxa de conversão: "
        f"{taxa_conversao:.1f}%"
    )

    return {
        "total": total,
        "status": contagem,
        "taxa_conversao": taxa_conversao,
    }


def _converter_data_contato(valor):
    """
    Converte o próximo contato para uma data Python.
    """

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    texto = _valor(valor)

    formatos = [
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
    ]

    for formato in formatos:

        try:
            return datetime.strptime(
                texto,
                formato
            ).date()

        except ValueError:
            continue

    return None


def listar_followups():
    """
    Separa os próximos contatos em atrasados, hoje e futuros.
    """

    hoje = datetime.now().date()

    atrasados = []
    hoje_lista = []
    proximos = []

    for lead in pegar_leads():

        data_contato = _converter_data_contato(
            lead["proximo_contato"]
        )

        if data_contato is None:
            continue

        item = lead.copy()

        item["_data_contato"] = data_contato

        if data_contato < hoje:
            atrasados.append(item)

        elif data_contato == hoje:
            hoje_lista.append(item)

        else:
            proximos.append(item)

    def chave_ordenacao(item):

        return (
            item["_data_contato"],
            _valor(item["nome"]).casefold()
        )

    atrasados.sort(
        key=chave_ordenacao
    )

    hoje_lista.sort(
        key=chave_ordenacao
    )

    proximos.sort(
        key=chave_ordenacao
    )

    def mostrar_grupo(titulo, grupo):

        print(f"\n{titulo}")

        for lead in grupo:

            print("-" * 25)
            print(f"Nome: {lead['nome']}")
            print(f"Telefone: {lead['telefone']}")
            print(f"Status: {lead['status']}")

            print(
                f"Próximo contato: "
                f"{lead['proximo_contato']}"
            )

    print("\n===== FOLLOW-UPS =====")

    mostrar_grupo(
        "ATRASADOS",
        atrasados
    )

    mostrar_grupo(
        "HOJE",
        hoje_lista
    )

    mostrar_grupo(
        "PRÓXIMOS",
        proximos
    )

    for grupo in (
        atrasados,
        hoje_lista,
        proximos
    ):

        for item in grupo:
            item.pop(
                "_data_contato",
                None
            )

    return {
        "atrasados": atrasados,
        "hoje": hoje_lista,
        "proximos": proximos,
    }


if __name__ == "__main__":

    criado = criar_planilha()

    if criado:

        print(
            "Planilha leads.xlsx "
            "criada com sucesso."
        )

    else:

        print(
            "A planilha leads.xlsx já existe "
            "e não foi sobrescrita."
        )