import re
import webbrowser
from urllib.parse import quote


def normalizar_telefone_whatsapp(telefone):
    numeros = re.sub(
        r"\D",
        "",
        str(telefone)
    )

    if (
        numeros.startswith("55")
        and len(numeros) in (12, 13)
    ):
        return numeros

    if len(numeros) in (10, 11):
        return f"55{numeros}"

    raise ValueError(
        "O telefone precisa ter DDD "
        "e 10 ou 11 números."
    )


def _copiar_texto(
    janela,
    texto,
    mensagem_erro
):
    texto = str(
        texto
    ).strip()

    if not texto:
        raise ValueError(
            mensagem_erro
        )

    janela.clipboard_clear()
    janela.clipboard_append(
        texto
    )
    janela.update()


def copiar_resumo(
    janela,
    lead
):
    _copiar_texto(
        janela,
        lead.get(
            "resumo",
            ""
        ),
        "Este lead não possui resumo."
    )


def copiar_whatsapp(
    janela,
    lead
):
    """
    Copia o nome utilizado ao salvar
    o contato no WhatsApp.

    Formato:
    LEAD - NOME - PRODUTO - CIDADE / UF - ORIGEM
    """

    _copiar_texto(
        janela,
        lead.get(
            "whatsapp",
            ""
        ),
        (
            "Este lead não possui um nome "
            "para o WhatsApp."
        )
    )


def abrir_whatsapp(lead):
    telefone = (
        normalizar_telefone_whatsapp(
            lead.get(
                "telefone",
                ""
            )
        )
    )

    # Usa o nome correto do WhatsApp,
    # não mais o resumo do lead.
    mensagem = str(
        lead.get(
            "whatsapp",
            ""
        )
    ).strip()

    url = (
        f"https://wa.me/{telefone}"
    )

    if mensagem:
        url += (
            f"?text={quote(mensagem)}"
        )

    aberto = webbrowser.open(
        url
    )

    if not aberto:
        raise RuntimeError(
            "Não foi possível abrir "
            "o navegador."
        )