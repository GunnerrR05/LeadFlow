import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import NOME_APLICACAO
from telas.cadastro import abrir_cadastro
from telas.buscar import abrir_busca
from telas.listar import abrir_lista
from telas.dashboard import abrir_dashboard
from telas.followups import abrir_followups
from servicos.backup import (
    criar_backup,
    criar_backup_diario,
    restaurar_backup,
    PASTA_BACKUPS,
)
from servicos.leads import obter_followups

from sistema import tratar_erro_tkinter
from tema import CINZA_CLARO, aplicar_tema

import sys
from pathlib import Path


ID_APLICATIVO_WINDOWS = "ZarkenLeads.GestaoDeLeads"


def configurar_identidade_windows():
    if sys.platform != "win32":
        return

    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            ID_APLICATIVO_WINDOWS
        )
    except (AttributeError, OSError):
        pass

def caminho_recurso(nome_arquivo):
    """
    Encontra arquivos tanto durante o desenvolvimento
    quanto dentro do executável criado pelo PyInstaller.
    """

    if hasattr(sys, "_MEIPASS"):
        pasta_base = Path(sys._MEIPASS)
    else:
        pasta_base = Path(__file__).resolve().parent

    return pasta_base / nome_arquivo

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    posicao_x = (largura_tela - largura) // 2
    posicao_y = (altura_tela - altura) // 2

    janela.geometry(
        f"{largura}x{altura}+{posicao_x}+{posicao_y}"
    )


def iniciar_interface():
    configurar_identidade_windows()

    janela = tk.Tk()
    janela.configure(
        background=CINZA_CLARO
    )

    logo_zarken = None
    caminho_icone = caminho_recurso(
        "zarken-leads.ico"
    )

    try:
        janela.iconbitmap(
            str(caminho_icone)
        )
        janela.iconbitmap(
            default=str(caminho_icone)
        )
    except tk.TclError:
        pass

    try:
        logo_zarken = tk.PhotoImage(
            file=str(
                caminho_recurso(
                    "assets/brand/zarken-symbol-64.png"
                )
            )
        )
        janela.iconphoto(
            True,
            logo_zarken
        )
        janela.logo_zarken = logo_zarken
    except tk.TclError:
        logo_zarken = None

    janela.report_callback_exception = (
        tratar_erro_tkinter
    )

    janela.title(
        f"{NOME_APLICACAO} - Gestão de Leads"
    )
    centralizar_janela(
        janela,
        500,
        850
    )


    janela.resizable(False, False)

    estilo = ttk.Style(janela)
    aplicar_tema(estilo)

    estilo.configure(
        "Titulo.TLabel",
        font=("Segoe UI", 22, "bold")
    )

    estilo.configure(
        "Subtitulo.TLabel",
        font=("Segoe UI", 10)
    )

    estilo.configure(
        "Menu.TButton",
        font=("Segoe UI", 10),
        padding=7
    )

    container = ttk.Frame(
        janela,
        padding=30
    )

    container.pack(
        expand=True,
        fill="both"
    )

    cabecalho = ttk.Frame(
        container
    )

    cabecalho.pack(
        pady=(4, 18)
    )

    if logo_zarken is not None:
        ttk.Label(
            cabecalho,
            image=logo_zarken
        ).pack(
            side="left",
            padx=(0, 14)
        )

    textos_cabecalho = ttk.Frame(
        cabecalho
    )
    textos_cabecalho.pack(
        side="left"
    )

    ttk.Label(
        textos_cabecalho,
        text=NOME_APLICACAO,
        style="Titulo.TLabel"
    ).pack(
        anchor="w"
    )

    ttk.Label(
        textos_cabecalho,
        text="Cada lead, uma nova oportunidade.",
        style="Subtitulo.TLabel"
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    def fazer_backup():
        try:
            arquivo_backup = criar_backup()

        except Exception as erro:
            messagebox.showerror(
                "Erro no backup",
                (
                    "Não foi possível criar o backup."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        messagebox.showinfo(
            "Backup concluído",
            (
                "Backup criado com sucesso!"
                f"\n\nArquivo: {arquivo_backup.name}"
                "\nPasta: backups"
            ),
            parent=janela
        )

    def restaurar_planilha():
        arquivo_selecionado = filedialog.askopenfilename(
            title="Selecionar Backup",
            initialdir=PASTA_BACKUPS,
            filetypes=[
                (
                    "Planilhas do Excel",
                    "*.xlsx"
                )
            ],
            parent=janela
        )

        if not arquivo_selecionado:
            return

        confirmacao = messagebox.askyesno(
            "Restaurar Backup",
            (
                "A planilha atual será substituída "
                "pelo backup selecionado.\n\n"
                "Antes disso, o sistema criará uma "
                "cópia de segurança da planilha atual.\n\n"
                "Deseja continuar?"
            ),
            parent=janela
        )

        if not confirmacao:
            return

        try:
            backup_seguranca = restaurar_backup(
                arquivo_selecionado
            )

        except PermissionError:
            messagebox.showerror(
                "Planilha em uso",
                (
                    "Não foi possível restaurar o backup.\n\n"
                    "Feche o arquivo leads.xlsx no Excel "
                    "e tente novamente."
                ),
                parent=janela
            )
            return

        except Exception as erro:
            messagebox.showerror(
                "Erro na restauração",
                (
                    "Não foi possível restaurar o backup."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        mensagem = (
            "Backup restaurado com sucesso!"
        )

        if backup_seguranca is not None:
            mensagem += (
                "\n\nUma cópia da planilha anterior foi criada:"
                f"\n{backup_seguranca.name}"
            )

        messagebox.showinfo(
            "Restauração concluída",
            mensagem,
            parent=janela
        )

    def verificar_backup_diario():
        try:
            criar_backup_diario()

        except Exception as erro:
            messagebox.showerror(
                "Erro no backup automático",
                (
                    "Não foi possível criar o "
                    "backup automático diário."
                    f"\n\n{erro}"
                ),
                parent=janela
            )

    def verificar_followups_iniciais():
        try:
            grupos = obter_followups()

        except Exception as erro:
            messagebox.showerror(
                "Erro nos follow-ups",
                (
                    "Não foi possível verificar "
                    "os follow-ups."
                    f"\n\n{erro}"
                ),
                parent=janela
            )
            return

        quantidade_atrasados = len(
            grupos["atrasados"]
        )

        quantidade_hoje = len(
            grupos["hoje"]
        )

        if (
            quantidade_atrasados == 0
            and quantidade_hoje == 0
        ):
            return

        mensagem = (
            "Você possui follow-ups pendentes:\n\n"
            f"Atrasados: {quantidade_atrasados}\n"
            f"Para hoje: {quantidade_hoje}"
        )

        messagebox.showwarning(
            "Follow-ups pendentes",
            mensagem,
            parent=janela
        )

    botao_cadastrar = ttk.Button(
        container,
        text="Cadastrar Lead",
        command=abrir_cadastro,
        style="Menu.TButton",
        width=30
    )

    botao_cadastrar.pack(pady=8)

    botao_buscar = ttk.Button(
        container,
        text="Buscar Lead",
        command=abrir_busca,
        style="Menu.TButton",
        width=30
    )

    botao_buscar.pack(pady=8)

    botao_listar = ttk.Button(
        container,
        text="Listar Leads",
        command=abrir_lista,
        style="Menu.TButton",
        width=30
    )

    botao_listar.pack(pady=8)

    botao_dashboard = ttk.Button(
        container,
        text="Dashboard",
        command=abrir_dashboard,
        style="Menu.TButton",
        width=30
    )

    botao_dashboard.pack(pady=8)

    botao_followups = ttk.Button(
        container,
        text="Follow-ups",
        command=abrir_followups,
        style="Menu.TButton",
        width=30
    )

    botao_followups.pack(pady=8)

    ttk.Separator(
        container,
        orient="horizontal"
    ).pack(
        fill="x",
        pady=25
    )

    botao_backup = ttk.Button(
        container,
        text="Fazer Backup",
        command=fazer_backup,
        style="Menu.TButton",
        width=30
    )

    botao_backup.pack(pady=8)

    botao_restaurar = ttk.Button(
        container,
        text="Restaurar Backup",
        command=restaurar_planilha,
        style="Menu.TButton",
        width=30
    )

    botao_restaurar.pack(pady=8)

    def fechar_programa():
        confirmacao = messagebox.askyesno(
            "Fechar programa",
            f"Deseja realmente fechar o {NOME_APLICACAO}?",
            parent=janela
        )

        if confirmacao:
            janela.destroy()

    botao_sair = ttk.Button(
        container,
        text="Sair",
        command=fechar_programa,
        style="Menu.TButton",
        width=30
    )

    botao_sair.pack(pady=8)

    rodape = ttk.Label(
        container,
        text=NOME_APLICACAO,
        font=("Segoe UI", 9)
    )

    rodape.pack(
        side="bottom",
        pady=10
    )

    janela.protocol(
        "WM_DELETE_WINDOW",
        fechar_programa
    )

    janela.after(
        300,
        verificar_backup_diario
    )

    janela.after(
        700,
        verificar_followups_iniciais
    )

    janela.mainloop()


if __name__ == "__main__":
    iniciar_interface()
