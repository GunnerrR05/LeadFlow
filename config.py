import os
import sys
from pathlib import Path
from shutil import copy2


NOME_APLICACAO = "LeadFlow"


def obter_pasta_aplicacao():
    """
    Retorna a pasta onde está o programa.

    Durante o desenvolvimento:
        pasta do projeto.

    Quando convertido em executável:
        pasta onde está o LeadFlow.exe.
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
    C:\\Users\\USUARIO\\AppData\\Local\\LeadFlow
    """

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
        / f".{NOME_APLICACAO.lower()}"
    )


PASTA_APLICACAO = obter_pasta_aplicacao()
PASTA_DADOS = obter_pasta_dados()

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
    / "leadflow.log"
)

ARQUIVO_BLOQUEIO = (
    PASTA_DADOS
    / "leadflow.lock"
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


def preparar_ambiente():
    """
    Prepara as pastas e migra uma planilha já existente.
    """

    criar_pastas()
    migrar_planilha_antiga()


preparar_ambiente()