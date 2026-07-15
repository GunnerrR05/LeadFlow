import tkinter as tk


def criar_botoes(
    janela,
    cadastrar,
    limpar,
    abrir_lista,
    abrir_busca,
    campos
):

    botoes = {}


    botoes["cadastrar"] = tk.Button(
        janela,
        text="Cadastrar Lead",
        command=cadastrar
    )

    botoes["cadastrar"].pack()



    botoes["limpar"] = tk.Button(
        janela,
        text="Limpar",
        command=limpar
    )

    botoes["limpar"].pack()


    botoes["listar"] = tk.Button(
        janela,
        text="Listar Leads",
        command=abrir_lista
    )

    botoes["listar"].pack()


    botoes["buscar"] = tk.Button(
        janela,
        text="Buscar Lead",
        command=abrir_busca
    )

    botoes["buscar"].pack()


    return botoes