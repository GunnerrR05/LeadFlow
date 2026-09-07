import os
import sys
from pathlib import Path
from shutil import copy2


NOME_APLICACAO = "Zarken Leads"
SLUG_APLICACAO = "zarken-leads"
NOME_APLICACAO_ANTIGO = "LeadFlow"


def obter_pasta_aplicacao():
    """
    Retorna a pasta onde está o programa.

    Durante o desenvolvimento:
        pasta do projeto.

    Quando convertido em executável:
        pasta onde está o executável do Zarken Leads.
    """

    if getattr(sys, "frozen", False):
        return Path(
            sys.executable
        ).resolve().parent

    return Path(
        __file__
    ).resolve().parent


def obter_pasta_dados():
    """
    Retorna a pasta permanente dos dados do usuário.

    No Windows:
    C:\\Users\\USUARIO\\AppData\\Local\\Zarken Leads
    """

    pasta_personalizada = os.getenv(
        "ZARKEN_LEADS_DATA_DIR"
    )

    if not pasta_personalizada:
        pasta_personalizada = os.getenv(
            "LEADFLOW_DATA_DIR"
        )

    if pasta_personalizada:
        return Path(
            pasta_personalizada
        )

    pasta_local = os.getenv(
        "LOCALAPPDATA"
    )

    if pasta_local:
        return (
            Path(pasta_local)
            / NOME_APLICACAO
        )

    return (
        Path.home()
        / f".{SLUG_APLICACAO}"
    )


def obter_pasta_dados_anterior():
    """Localiza a pasta de dados usada pelo LeadFlow."""

    pasta_personalizada = os.getenv(
        "LEADFLOW_DATA_DIR"
    )

    if pasta_personalizada:
        return Path(
            pasta_personalizada
        )

    pasta_local = os.getenv(
        "LOCALAPPDATA"
    )

    if pasta_local:
        return (
            Path(pasta_local)
            / NOME_APLICACAO_ANTIGO
        )

    return (
        Path.home()
        / f".{NOME_APLICACAO_ANTIGO.lower()}"
    )


PASTA_APLICACAO = obter_pasta_aplicacao()
PASTA_DADOS = obter_pasta_dados()
PASTA_DADOS_ANTERIOR = obter_pasta_dados_anterior()

ARQUIVO_LEADS = (
    PASTA_DADOS
    / "leads.xlsx"
)

PASTA_BACKUPS = (
    PASTA_DADOS
    / "backups"
)

PASTA_LOGS = (
    PASTA_DADOS
    / "logs"
)

ARQUIVO_LOG = (
    PASTA_LOGS
    / "zarken-leads.log"
)

ARQUIVO_BLOQUEIO = (
    PASTA_DADOS
    / "zarken-leads.lock"
)

ARQUIVO_LEADS_ANTIGO = (
    PASTA_APLICACAO
    / "leads.xlsx"
)


def criar_pastas():
    """
    Cria as pastas necessárias para o programa.
    """

    PASTA_DADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    PASTA_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )

    PASTA_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )


def migrar_planilha_antiga():
    """
    Copia o leads.xlsx antigo da pasta do projeto para
    a nova pasta de dados.

    A planilha antiga não é apagada.
    """

    if ARQUIVO_LEADS.exists():
        return False

    if not ARQUIVO_LEADS_ANTIGO.exists():
        return False

    if (
        ARQUIVO_LEADS_ANTIGO.resolve()
        == ARQUIVO_LEADS.resolve()
    ):
        return False

    copy2(
        ARQUIVO_LEADS_ANTIGO,
        ARQUIVO_LEADS
    )

    return True


def migrar_dados_marca_anterior():
    """
    Copia leads e backups do LeadFlow para o Zarken Leads.

    Arquivos existentes no novo destino nunca são
    sobrescritos e a pasta antiga permanece intacta.
    """

    try:
        mesma_pasta = (
            PASTA_DADOS_ANTERIOR.resolve()
            == PASTA_DADOS.resolve()
        )
    except OSError:
        mesma_pasta = False

    if mesma_pasta or not PASTA_DADOS_ANTERIOR.exists():
        return False

    copiou_arquivo = False
    origem_leads = (
        PASTA_DADOS_ANTERIOR
        / "leads.xlsx"
    )

    if origem_leads.exists() and not ARQUIVO_LEADS.exists():
        copy2(
            origem_leads,
            ARQUIVO_LEADS
        )
        copiou_arquivo = True

    pasta_backups_anterior = (
        PASTA_DADOS_ANTERIOR
        / "backups"
    )

    if pasta_backups_anterior.exists():
        for origem_backup in pasta_backups_anterior.glob(
            "*.xlsx"
        ):
            destino_backup = (
                PASTA_BACKUPS
                / origem_backup.name
            )

            if not destino_backup.exists():
                copy2(
                    origem_backup,
                    destino_backup
                )
                copiou_arquivo = True

    return copiou_arquivo


def preparar_ambiente():
    """
    Prepara as pastas e migra uma planilha já existente.
    """

    criar_pastas()
    migrar_dados_marca_anterior()
    migrar_planilha_antiga()


preparar_ambiente()
