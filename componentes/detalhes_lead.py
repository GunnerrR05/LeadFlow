import tkinter as tk
from tkinter import ttk


FUNDO_CONTEUDO = "#FBFAF8"
TEXTO_PRINCIPAL = "#151719"
TEXTO_SECUNDARIO = "#55585C"
AZUL = "#4F6F8E"


SECOES = (
    (
        "Contato",
        (
            ("nome", "Nome"),
            ("telefone", "Telefone"),
            ("email", "E-mail"),
            ("cidade_uf", "Cidade / UF"),
        ),
    ),
    (
        "Negociação",
        (
            ("status", "Status"),
            ("produto", "Produto"),
            ("aplicacao", "Aplicação"),
            ("origem", "Origem"),
        ),
    ),
    (
        "Responsabilidade e datas",
        (
            ("unidade", "Unidade"),
            ("consultor", "Consultor"),
            ("data_cadastro", "Cadastro"),
            ("proximo_contato", "Próximo contato"),
            ("ultima_interacao", "Última interação"),
        ),
    ),
)


class PainelDetalhesLead(ttk.Frame):
    """Ficha visual reutilizável para exibir os dados de um lead."""

    def __init__(self, pai, **opcoes):
        super().__init__(pai, **opcoes)

        self._variaveis = {}
        self._nome = tk.StringVar(
            master=self,
            value="Nenhum lead selecionado",
        )
        self._status = tk.StringVar(
            master=self,
            value="",
        )
        self._resumo = tk.StringVar(
            master=self,
            value="—",
        )
        self._whatsapp = tk.StringVar(
            master=self,
            value="—",
        )

        self._criar_interface()

    def _criar_interface(self):
        cabecalho = ttk.Frame(
            self,
            padding=(12, 8),
        )
        cabecalho.pack(
            fill="x",
            pady=(0, 8),
        )

        ttk.Label(
            cabecalho,
            textvariable=self._nome,
            font=("Segoe UI", 16, "bold"),
        ).pack(
            side="left",
        )

        ttk.Label(
            cabecalho,
            textvariable=self._status,
            font=("Segoe UI", 10, "bold"),
            foreground=AZUL,
        ).pack(
            side="right",
        )

        frame_secoes = ttk.Frame(self)
        frame_secoes.pack(
            fill="x",
            pady=(0, 8),
        )

        for coluna, (titulo, campos) in enumerate(SECOES):
            frame_secoes.columnconfigure(
                coluna,
                weight=1,
                uniform="detalhes",
            )

            cartao = ttk.LabelFrame(
                frame_secoes,
                text=titulo,
                padding=10,
            )
            cartao.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=(0 if coluna == 0 else 4, 0 if coluna == 2 else 4),
            )
            cartao.columnconfigure(1, weight=1)

            for linha, (chave, rotulo) in enumerate(campos):
                variavel = tk.StringVar(
                    master=self,
                    value="—",
                )
                self._variaveis[chave] = variavel

                ttk.Label(
                    cartao,
                    text=f"{rotulo}:",
                    font=("Segoe UI", 9, "bold"),
                ).grid(
                    row=linha,
                    column=0,
                    sticky="nw",
                    padx=(0, 8),
                    pady=3,
                )

                ttk.Label(
                    cartao,
                    textvariable=variavel,
                    font=("Segoe UI", 9),
                    foreground=TEXTO_SECUNDARIO,
                    wraplength=250,
                ).grid(
                    row=linha,
                    column=1,
                    sticky="nw",
                    pady=3,
                )

        area_inferior = ttk.Frame(self)
        area_inferior.pack(
            expand=True,
            fill="both",
        )
        area_inferior.columnconfigure(0, weight=3)
        area_inferior.columnconfigure(1, weight=2)
        area_inferior.rowconfigure(0, weight=1)

        frame_observacao = ttk.LabelFrame(
            area_inferior,
            text="Observações e histórico",
            padding=8,
        )
        frame_observacao.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 4),
        )

        barra_observacao = ttk.Scrollbar(
            frame_observacao,
            orient="vertical",
        )
        barra_observacao.pack(
            side="right",
            fill="y",
        )

        self._observacao = tk.Text(
            frame_observacao,
            wrap="word",
            font=("Segoe UI", 10),
            background=FUNDO_CONTEUDO,
            foreground=TEXTO_PRINCIPAL,
            selectbackground="#71869A",
            selectforeground="#F7F6F3",
            relief="flat",
            padx=10,
            pady=8,
            yscrollcommand=barra_observacao.set,
        )
        self._observacao.pack(
            side="left",
            expand=True,
            fill="both",
        )
        barra_observacao.configure(
            command=self._observacao.yview,
        )

        frame_complementos = ttk.Frame(area_inferior)
        frame_complementos.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(4, 0),
        )
        frame_complementos.rowconfigure(0, weight=1)
        frame_complementos.rowconfigure(1, weight=1)
        frame_complementos.columnconfigure(0, weight=1)

        frame_resumo = ttk.LabelFrame(
            frame_complementos,
            text="Resumo comercial",
            padding=10,
        )
        frame_resumo.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 4),
        )

        ttk.Label(
            frame_resumo,
            textvariable=self._resumo,
            font=("Segoe UI", 10),
            foreground=TEXTO_SECUNDARIO,
            wraplength=360,
            justify="left",
        ).pack(
            anchor="nw",
        )

        frame_whatsapp = ttk.LabelFrame(
            frame_complementos,
            text="Identificação no WhatsApp",
            padding=10,
        )
        frame_whatsapp.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(4, 0),
        )

        ttk.Label(
            frame_whatsapp,
            textvariable=self._whatsapp,
            font=("Segoe UI", 10),
            foreground=TEXTO_SECUNDARIO,
            wraplength=360,
            justify="left",
        ).pack(
            anchor="nw",
        )

        self.limpar()

    def limpar(self):
        self._nome.set(
            "Nenhum lead selecionado"
        )
        self._status.set("")

        for variavel in self._variaveis.values():
            variavel.set("—")

        self._resumo.set("—")
        self._whatsapp.set("—")
        self._definir_observacao("")

    def exibir(self, lead):
        lead = lead or {}
        nome = str(
            lead.get("nome", "")
            or "Lead sem nome"
        ).strip()
        status = str(
            lead.get("status", "")
            or "SEM STATUS"
        ).strip()

        self._nome.set(nome)
        self._status.set(status)

        for chave, variavel in self._variaveis.items():
            valor = str(
                lead.get(chave, "")
                or "—"
            ).strip()
            variavel.set(valor)

        self._resumo.set(
            str(lead.get("resumo", "") or "—").strip()
        )
        self._whatsapp.set(
            str(lead.get("whatsapp", "") or "—").strip()
        )
        self._definir_observacao(
            str(lead.get("observacao", "") or "").strip()
        )

    def _definir_observacao(self, texto):
        self._observacao.configure(state="normal")
        self._observacao.delete("1.0", tk.END)
        self._observacao.insert(
            "1.0",
            texto or "Nenhuma observação registrada.",
        )
        self._observacao.configure(state="disabled")
        self._observacao.yview_moveto(0)
