import os
from datetime import datetime
from pathlib import Path
from shutil import copy2

from openpyxl import load_workbook

from config import (
    ARQUIVO_LEADS,
    PASTA_BACKUPS,
    preparar_ambiente,
)


LIMITE_BACKUPS = 30


preparar_ambiente()


def limpar_backups_antigos(
    limite=LIMITE_BACKUPS
):
    """
    Mantém somente os backups mais recentes.
    """

    if limite < 1:
        raise ValueError(
            "O limite de backups precisa "
            "ser maior que zero."
        )

    if not PASTA_BACKUPS.exists():
        return []

    arquivos = sorted(
        PASTA_BACKUPS.glob(
            "leads_backup_*.xlsx"
        ),
        key=lambda arquivo: (
            arquivo.stat().st_mtime
        ),
        reverse=True
    )

    arquivos_removidos = []

    for arquivo in arquivos[limite:]:
        try:
            arquivo.unlink()
            arquivos_removidos.append(
                arquivo
            )

        except OSError:
            continue

    return arquivos_removidos


def criar_backup():
    """
    Cria uma cópia da planilha na pasta de backups.
    """

    preparar_ambiente()

    if not ARQUIVO_LEADS.exists():
        raise FileNotFoundError(
            "A planilha leads.xlsx "
            "não foi encontrada."
        )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S-%f"
    )

    nome_backup = (
        f"leads_backup_{data_hora}.xlsx"
    )

    destino = (
        PASTA_BACKUPS
        / nome_backup
    )

    try:
        copy2(
            ARQUIVO_LEADS,
            destino
        )

    except PermissionError as erro:
        raise PermissionError(
            "Não foi possível criar o backup. "
            "Feche o arquivo leads.xlsx no Excel "
            "e tente novamente."
        ) from erro

    limpar_backups_antigos()

    return destino


def validar_backup(caminho_backup):
    """
    Confere se o arquivo selecionado é uma
    planilha válida do Excel.
    """

    origem = Path(
        caminho_backup
    )

    if not origem.exists():
        raise FileNotFoundError(
            "O arquivo de backup "
            "não foi encontrado."
        )

    if origem.suffix.lower() != ".xlsx":
        raise ValueError(
            "Selecione um arquivo de backup "
            "no formato .xlsx."
        )

    if (
        origem.resolve()
        == ARQUIVO_LEADS.resolve()
    ):
        raise ValueError(
            "O arquivo selecionado já é "
            "a planilha principal."
        )

    try:
        planilha_teste = load_workbook(
            origem,
            read_only=True,
            data_only=False
        )

        planilha_teste.close()

    except Exception as erro:
        raise ValueError(
            "O arquivo selecionado não é "
            "uma planilha válida."
        ) from erro

    return origem


def restaurar_backup(caminho_backup):
    """
    Restaura um backup como planilha principal.

    Antes da restauração, cria uma cópia de
    segurança da planilha atual.
    """

    preparar_ambiente()

    origem = validar_backup(
        caminho_backup
    )

    backup_seguranca = None

    if ARQUIVO_LEADS.exists():
        backup_seguranca = criar_backup()

    arquivo_temporario = (
        ARQUIVO_LEADS.with_name(
            "leads_restauracao.tmp.xlsx"
        )
    )

    try:
        copy2(
            origem,
            arquivo_temporario
        )

        os.replace(
            arquivo_temporario,
            ARQUIVO_LEADS
        )

    except PermissionError as erro:
        if arquivo_temporario.exists():
            try:
                arquivo_temporario.unlink()
            except OSError:
                pass

        raise PermissionError(
            "Não foi possível restaurar o backup. "
            "Feche o arquivo leads.xlsx no Excel "
            "e tente novamente."
        ) from erro

    except Exception:
        if arquivo_temporario.exists():
            try:
                arquivo_temporario.unlink()
            except OSError:
                pass

        raise

    return backup_seguranca


def criar_backup_diario():
    """
    Cria somente um backup automático por dia.

    Retorna:
        caminho do backup;
        True quando um novo backup foi criado;
        False quando já existia um backup no dia.
    """

    preparar_ambiente()

    if not ARQUIVO_LEADS.exists():
        raise FileNotFoundError(
            "A planilha leads.xlsx "
            "não foi encontrada."
        )

    data_atual = datetime.now().strftime(
        "%Y-%m-%d"
    )

    padrao = (
        f"leads_backup_{data_atual}_*.xlsx"
    )

    backups_do_dia = sorted(
        PASTA_BACKUPS.glob(
            padrao
        ),
        key=lambda arquivo: (
            arquivo.stat().st_mtime
        ),
        reverse=True
    )

    if backups_do_dia:
        return (
            backups_do_dia[0],
            False
        )

    novo_backup = criar_backup()

    return (
        novo_backup,
        True
    )