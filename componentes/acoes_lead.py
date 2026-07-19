import re
import webbrowser
from urllib.parse import quote


def normalizar_telefone_whatsapp(telefone):
    numeros = re.sub(
        r"\D",
        "",
        str(telefone)
    )

    if numeros.startswith("55") and len(numeros) in (12, 13):
        return numeros

    if len(numeros) in (10, 11):
        return f"55{numeros}"

    raise ValueError(
        "O telefone precisa ter DDD e 10 ou 11 números."
    )


def copiar_resumo(janela, lead):
    resumo = str(
        lead.get("resumo", "")
    ).strip()

    if not resumo:
        raise ValueError(
            "Este lead não possui resumo."
        )

    janela.clipboard_clear()
    janela.clipboard_append(resumo)
    janela.update()


def abrir_whatsapp(lead):
    telefone = normalizar_telefone_whatsapp(
        lead.get("telefone", "")
    )

    mensagem = str(
        lead.get("resumo", "")
    ).strip()

    url = f"https://wa.me/{telefone}"

    if mensagem:
        url += f"?text={quote(mensagem)}"

    aberto = webbrowser.open(url)

    if not aberto:
        raise RuntimeError(
            "Não foi possível abrir o navegador."
        )