import logging
import tkinter as tk
from tkinter import messagebox

from excel import criar_planilha
from interface import iniciar_interface

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
        "LeadFlow já está aberto",
        (
            "O LeadFlow já está sendo executado.\n\n"
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
            "Erro fatal ao iniciar o LeadFlow.",
            erro
        )

        janela_erro = tk.Tk()
        janela_erro.withdraw()

        messagebox.showerror(
            "Erro ao iniciar",
            (
                "Não foi possível iniciar o LeadFlow.\n\n"
                "O problema foi registrado no arquivo de log.\n\n"
                f"Detalhes: {erro}"
            ),
            parent=janela_erro
        )

        janela_erro.destroy()

    finally:
        liberar_bloqueio_instancia()

        logging.info(
            "LeadFlow encerrado."
        )


if __name__ == "__main__":
    main()