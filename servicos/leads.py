from datetime import datetime
from excel import (
    salvar_lead,
    pegar_leads,
    buscar_lead_por_telefone,
    atualizar_lead as atualizar_lead_excel,
    excluir_lead as excluir_lead_excel
)


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



def atualizar_lead(lead, campos):

    lead["nome"] = campos["nome"].get()
    lead["telefone"] = campos["telefone"].get()
    lead["email"] = campos["email"].get()
    lead["interesse"] = campos["interesse"].get()
    lead["origem"] = campos["origem"].get()
    lead["consultor"] = campos["consultor"].get()
    lead["observacao"] = campos["observacao"].get()

    atualizar_lead_excel(lead)

    return lead



def buscar_lead(telefone):

    return buscar_lead_por_telefone(telefone)



def excluir_lead(lead):

    excluir_lead_excel(lead["linha"])


def listar_leads():

    return pegar_leads()