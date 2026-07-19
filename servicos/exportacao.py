from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill


COLUNAS_EXPORTACAO = [
    ("data_cadastro", "DATA DE CADASTRO"),
    ("proximo_contato", "PRÓXIMO CONTATO"),
    ("ultima_interacao", "ÚLTIMA INTERAÇÃO"),
    ("status", "STATUS"),
    ("telefone", "TELEFONE"),
    ("nome", "NOME"),
    ("produto", "PRODUTO"),
    ("cidade_uf", "CIDADE / UF"),
    ("email", "E-MAIL"),
    ("aplicacao", "APLICAÇÃO"),
    ("origem", "ORIGEM"),
    ("consultor", "CONSULTOR"),
    ("observacao", "OBSERVAÇÃO"),
    ("resumo", "RESUMO"),
    ("whatsapp", "NOME NO WHATSAPP"),
]


def exportar_leads(lista_leads, caminho):
    if not lista_leads:
        raise ValueError(
            "Não existem leads para exportar."
        )

    destino = Path(caminho)

    if destino.suffix.lower() != ".xlsx":
        destino = destino.with_suffix(".xlsx")

    workbook = Workbook()
    planilha = workbook.active
    planilha.title = "Relatório de Leads"

    cabecalhos = [
        titulo
        for _, titulo in COLUNAS_EXPORTACAO
    ]

    planilha.append(cabecalhos)

    preenchimento = PatternFill(
        fill_type="solid",
        fgColor="D9EAF7"
    )

    for celula in planilha[1]:
        celula.font = Font(bold=True)
        celula.fill = preenchimento
        celula.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    for lead in lista_leads:
        planilha.append([
            lead.get(chave, "")
            for chave, _ in COLUNAS_EXPORTACAO
        ])

    planilha.freeze_panes = "A2"
    planilha.auto_filter.ref = planilha.dimensions

    larguras = {
        "A": 20,
        "B": 20,
        "C": 20,
        "D": 25,
        "E": 18,
        "F": 25,
        "G": 25,
        "H": 20,
        "I": 30,
        "J": 25,
        "K": 20,
        "L": 20,
        "M": 55,
        "N": 45,
        "O": 55,
    }

    for coluna, largura in larguras.items():
        planilha.column_dimensions[
            coluna
        ].width = largura

    for linha in planilha.iter_rows(
        min_row=2
    ):
        for celula in linha:
            celula.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

    workbook.save(destino)

    return destino