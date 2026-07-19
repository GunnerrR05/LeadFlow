from datetime import datetime
from pathlib import Path
from shutil import copy2

from openpyxl import load_workbook


PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_LEADS = PASTA_PROJETO / "leads.xlsx"
PASTA_BACKUPS = PASTA_PROJETO / "backups"

LIMITE_BACKUPS = 30

def limpar_backups_antigos(limite=LIMITE_BACKUPS):
    """
    Mantém somente os backups mais recentes.
    """

    if limite < 1:
        raise ValueError(
            "O limite de backups precisa ser maior que zero."
        )

    if not PASTA_BACKUPS.exists():
        return []

    arquivos = sorted(
        PASTA_BACKUPS.glob(
            "leads_backup_*.xlsx"
        ),
        key=lambda arquivo: arquivo.name,
        reverse=True
    )

    arquivos_removidos = []

    for arquivo in arquivos[limite:]:
        try:
            arquivo.unlink()
            arquivos_removidos.append(arquivo)

        except OSError:
            continue

    return arquivos_removidos

def criar_backup():
    """
    Cria uma cópia da planilha na pasta backups.
    """

    if not ARQUIVO_LEADS.exists():
        raise FileNotFoundError(
            "A planilha leads.xlsx não foi encontrada."
        )

    PASTA_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nome_backup = (
        f"leads_backup_{data_hora}.xlsx"
    )

    destino = PASTA_BACKUPS / nome_backup

    copy2(
        ARQUIVO_LEADS,
        destino
    )

    limpar_backups_antigos()

    return destino

def restaurar_backup(caminho_backup):
    """
    Restaura um arquivo de backup como a planilha principal.

    Antes da restauração, cria uma cópia de segurança
    da planilha atual.
    """

    origem = Path(caminho_backup)

    if not origem.exists():
        raise FileNotFoundError(
            "O arquivo de backup não foi encontrado."
        )

    if origem.suffix.lower() != ".xlsx":
        raise ValueError(
            "Selecione um arquivo de backup no formato .xlsx."
        )

    if origem.resolve() == ARQUIVO_LEADS.resolve():
        raise ValueError(
            "O arquivo selecionado já é a planilha principal."
        )

    try:
        planilha_teste = load_workbook(
            origem,
            read_only=True
        )
        planilha_teste.close()

    except Exception as erro:
        raise ValueError(
            "O arquivo selecionado não é uma planilha válida."
        ) from erro

    backup_seguranca = None

    if ARQUIVO_LEADS.exists():
        backup_seguranca = criar_backup()

    copy2(
        origem,
        ARQUIVO_LEADS
    )

    return backup_seguranca

def criar_backup_diario():
    """
    Cria somente um backup automático por dia.

    Retorna:
        caminho do backup
        True se um novo backup foi criado
        False se já existia backup do dia
    """

    if not ARQUIVO_LEADS.exists():
        raise FileNotFoundError(
            "A planilha leads.xlsx não foi encontrada."
        )

    PASTA_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )

    data_atual = datetime.now().strftime(
        "%Y-%m-%d"
    )

    padrao = (
        f"leads_backup_{data_atual}_*.xlsx"
    )

    backups_do_dia = sorted(
        PASTA_BACKUPS.glob(padrao),
        key=lambda arquivo: arquivo.stat().st_mtime,
        reverse=True
    )

    if backups_do_dia:
        return backups_do_dia[0], False

    novo_backup = criar_backup()

    return novo_backup, True