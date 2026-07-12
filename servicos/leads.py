from datetime import datetime
from excel import salvar_lead


def cadastrar_lead(campos):

    lead = {
        "nome": campos["nome"].get(),
        "telefone": campos["telefone"].get(),
        "email": campos["email"].get(),
        "interesse": campos["interesse"].get(),
        "origem": campos["origem"].get(),
        "consultor": campos["consultor"].get(),
        "observacao": campos["observacao"].get(),

        "status": "Novo",
        "prioridade": "Morno",
        "proximo_contato": "",
        "ultima_interacao": "",
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    salvar_lead(lead)

    return lead