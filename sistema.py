import logging
import socket
import traceback
from logging.handlers import RotatingFileHandler
from tkinter import messagebox

from config import (
    ARQUIVO_LOG,
    NOME_APLICACAO,
    preparar_ambiente,
)


PORTA_INSTANCIA = 47653
_socket_instancia = None


def configurar_logs():
    """
    Configura o arquivo de registro de erros.

    O arquivo ficará em:
    AppData/Local/Zarken Leads/logs/zarken-leads.log
    """

    preparar_ambiente()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return

    manipulador = RotatingFileHandler(
        ARQUIVO_LOG,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )

    manipulador.setFormatter(
        formato
    )

    logger.addHandler(
        manipulador
    )

    logging.info(
        f"{NOME_APLICACAO} iniciado."
    )


def registrar_erro(
    mensagem,
    erro=None
):
    """
    Registra um erro no arquivo de log.
    """

    if erro is None:
        logging.error(
            mensagem
        )
        return

    logging.error(
        "%s\n%s",
        mensagem,
        "".join(
            traceback.format_exception(
                type(erro),
                erro,
                erro.__traceback__
            )
        )
    )


def tratar_erro_tkinter(
    tipo_erro,
    erro,
    rastreamento
):
    """
    Trata erros inesperados ocorridos
    dentro de botões e eventos do Tkinter.
    """

    texto_rastreamento = "".join(
        traceback.format_exception(
            tipo_erro,
            erro,
            rastreamento
        )
    )

    logging.error(
        "Erro inesperado no Tkinter:\n%s",
        texto_rastreamento
    )

    messagebox.showerror(
        "Erro inesperado",
        (
            f"O {NOME_APLICACAO} encontrou um erro inesperado.\n\n"
            "O problema foi registrado no arquivo de log.\n\n"
            f"Detalhes: {erro}"
        )
    )


def adquirir_bloqueio_instancia():
    """
    Impede que duas instâncias do Zarken Leads
    sejam abertas simultaneamente.
    """

    global _socket_instancia

    socket_instancia = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        if hasattr(
            socket,
            "SO_EXCLUSIVEADDRUSE"
        ):
            socket_instancia.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_EXCLUSIVEADDRUSE,
                1
            )

        socket_instancia.bind(
            (
                "127.0.0.1",
                PORTA_INSTANCIA
            )
        )

        socket_instancia.listen(
            1
        )

    except OSError:
        socket_instancia.close()
        return False

    _socket_instancia = (
        socket_instancia
    )

    return True


def liberar_bloqueio_instancia():
    """
    Libera o bloqueio quando o programa é fechado.
    """

    global _socket_instancia

    if _socket_instancia is None:
        return

    try:
        _socket_instancia.close()

    except OSError:
        pass

    _socket_instancia = None
