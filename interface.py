import tkinter as tk
from tkinter import ttk, messagebox

from telas.cadastro import abrir_cadastro
from telas.buscar import abrir_busca
from telas.listar import abrir_lista
from telas.dashboard import abrir_dashboard
from telas.followups import abrir_followups


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
    janela = tk.Tk()

    janela.title("LeadFlow - Gerenciador de Leads")
    centralizar_janela(janela, 500, 680)

    janela.resizable(False, False)

    estilo = ttk.Style(janela)

    if "clam" in estilo.theme_names():
        estilo.theme_use("clam")

    estilo.configure(
        "Titulo.TLabel",
        font=("Arial", 24, "bold")
    )

    estilo.configure(
        "Subtitulo.TLabel",
        font=("Arial", 11)
    )

    estilo.configure(
        "Menu.TButton",
        font=("Arial", 11),
        padding=10
    )

    container = ttk.Frame(
        janela,
        padding=30
    )

    container.pack(
        expand=True,
        fill="both"
    )

    titulo = ttk.Label(
        container,
        text="Sistema de Leads",
        style="Titulo.TLabel"
    )

    titulo.pack(pady=(20, 5))

    subtitulo = ttk.Label(
        container,
        text="Gerenciamento de contatos comerciais",
        style="Subtitulo.TLabel"
    )

    subtitulo.pack(pady=(0, 30))

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

    def fechar_programa():
        confirmacao = messagebox.askyesno(
            "Fechar programa",
            "Deseja realmente fechar o LeadFlow?",
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
        text="LeadFlow",
        font=("Arial", 9)
    )

    rodape.pack(
        side="bottom",
        pady=10
    )

    janela.protocol(
        "WM_DELETE_WINDOW",
        fechar_programa
    )

    janela.mainloop()


if __name__ == "__main__":
    iniciar_interface()