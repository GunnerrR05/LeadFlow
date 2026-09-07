import logging
import tkinter as tk
from tkinter import messagebox

from excel import criar_planilha
from interface import iniciar_interface
from config import NOME_APLICACAO

from sistema import (
    adquirir_bloqueio_instancia,
    configurar_logs,
    liberar_bloqueio_instancia,
    registrar_erro,
)


def mostrar_programa_aberto():
    janela_aviso = tk.Tk()
    janela_aviso.withdraw()

    messagebox.showwarning(
        f"{NOME_APLICACAO} já está aberto",
        (
            f"O {NOME_APLICACAO} já está sendo executado.\n\n"
            "Feche a janela que já está aberta "
            "antes de iniciar novamente."
        ),
        parent=janela_aviso
    )

    janela_aviso.destroy()


def main():
    configurar_logs()

    if not adquirir_bloqueio_instancia():
        mostrar_programa_aberto()
        return

    try:
        criar_planilha()
        iniciar_interface()

    except Exception as erro:
        registrar_erro(
            f"Erro fatal ao iniciar o {NOME_APLICACAO}.",
            erro
        )

        janela_erro = tk.Tk()
        janela_erro.withdraw()

        messagebox.showerror(
            "Erro ao iniciar",
            (
                f"Não foi possível iniciar o {NOME_APLICACAO}.\n\n"
                "O problema foi registrado no arquivo de log.\n\n"
                f"Detalhes: {erro}"
            ),
            parent=janela_erro
        )

        janela_erro.destroy()

    finally:
        liberar_bloqueio_instancia()

        logging.info(
            f"{NOME_APLICACAO} encerrado."
        )


if __name__ == "__main__":
    main()
