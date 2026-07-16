from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import datetime

def criar_planilha():
    workbook = Workbook()
    planilha = workbook.active
    
    
    planilha['A1'] = 'NOME'
    planilha['B1'] = 'TELEFONE'
    planilha['C1'] = 'E-MAIL'
    planilha['D1'] = 'INTERESSE'
    planilha['E1'] = 'ORIGEM'
    planilha['F1'] = 'CONSULTOR'
    planilha['G1'] = 'DATA DE CADASTRO'
    planilha['H1'] = 'OBSERVAÇÕES'
    planilha["I1"] = "STATUS"
    planilha['J1'] = 'HISTÓRICO'
    planilha['K1'] = 'PROXIMO CONTATO'
    planilha['L1'] = 'ULTIMA INTERACAO'
    planilha['M1'] = 'PRIORIDADE'

    
    
    workbook.save('leads.xlsx')

def salvar_lead(lead):
    arquivo = load_workbook('leads.xlsx')
    planilha = arquivo.active

    linha_vazia = planilha.max_row + 1
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M")

    planilha[f"A{linha_vazia}"] = lead["nome"]
    planilha[f"B{linha_vazia}"] = lead["telefone"]
    planilha[f"C{linha_vazia}"] = lead["email"]
    planilha[f"D{linha_vazia}"] = lead["interesse"]
    planilha[f"E{linha_vazia}"] = lead["origem"]
    planilha[f"F{linha_vazia}"] = lead["consultor"]
    planilha[f"G{linha_vazia}"] = data_formatada
    planilha[f"H{linha_vazia}"] = lead["observacao"]
    planilha[f"I{linha_vazia}"] = lead["status"]
    planilha[f"J{linha_vazia}"] = (
        f"[{data_formatada}] Criado - {lead['status']}"
    )
    planilha[f'K{linha_vazia}'] = lead["proximo_contato"]
    planilha[f'L{linha_vazia}'] = lead["ultima_interacao"]
    planilha[f'M{linha_vazia}'] = lead["prioridade"]
    

    arquivo.save('leads.xlsx')


def listar_leads():
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    print("\n===== LEADS CADASTRADOS =====")

    for linha in range(2, planilha.max_row + 1):
        nome = planilha[f"A{linha}"].value
        telefone = planilha[f"B{linha}"].value
        email = planilha[f"C{linha}"].value
        interesse = planilha[f"D{linha}"].value
        origem = planilha[f"E{linha}"].value
        consultor = planilha[f"F{linha}"].value
        data = planilha[f"G{linha}"].value
        observacao = planilha[f"H{linha}"].value
        status = planilha[f"I{linha}"].value
        historico = planilha[f"J{linha}"].value
        prioridade = planilha[f"M{linha}"].value
        proximo_contato = planilha[f"K{linha}"].value
        ultima_interacao = planilha[f"L{linha}"].value

        if status is None:
            status = "Novo"

        print(f"\nLead {linha - 1}")
        print(f"Nome: {nome}")
        print(f"Telefone: {telefone}")
        print(f"E-mail: {email}")
        print(f"Interesse: {interesse}")
        print(f"Origem: {origem}")
        print(f"Consultor: {consultor}")
        print(f"Data: {data}")
        print(f"Observações: {observacao}")
        print(f"Status: {status}")
        print(f"Histórico: {historico}")
        print(f"Prioridade: {prioridade}")
        print(f"Próximo contato: {proximo_contato}")
        print(f"Última interação: {ultima_interacao}")
        
        
        print("-" * 30)


def buscar_lead_por_nome(nome_busca):
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    for linha in range(2, planilha.max_row + 1):
        nome = planilha[f"A{linha}"].value
        if nome == nome_busca:
            return linha
        
    return None
        

def pegar_leads():
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    leads = []

    for linha in range(2, planilha.max_row + 1):

        nome = planilha[f"A{linha}"].value

        if nome is not None:
            lead = {
                "nome": planilha[f"A{linha}"].value,
                "telefone": planilha[f"B{linha}"].value,
                "email": planilha[f"C{linha}"].value,
                "interesse": planilha[f"D{linha}"].value,
                "origem": planilha[f"E{linha}"].value,
                "consultor": planilha[f"F{linha}"].value,
                "data": planilha[f"G{linha}"].value,
                "observacao": planilha[f"H{linha}"].value,
                "status": planilha[f"I{linha}"].value,
                "historico": planilha[f"J{linha}"].value,
                "proximo_contato": planilha[f"K{linha}"].value,
                "ultima_interacao": planilha[f"L{linha}"].value,
                "prioridade": planilha[f"M{linha}"].value
            }

        leads.append(lead)

    return leads


def buscar_lead_por_telefone(telefone_busca):
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    for linha in range(2, planilha.max_row + 1):

        telefone = planilha[f"B{linha}"].value

        if telefone == telefone_busca:
            lead = {
                "linha": linha,
                "nome": planilha[f"A{linha}"].value,
                "telefone": telefone,
                "email": planilha[f"C{linha}"].value,
                "interesse": planilha[f"D{linha}"].value,
                "origem": planilha[f"E{linha}"].value,
                "consultor": planilha[f"F{linha}"].value,
                "data": planilha[f"G{linha}"].value,
                "observacao": planilha[f"H{linha}"].value,
                "status": planilha[f"I{linha}"].value or "Novo",
                "prioridade": planilha[f"M{linha}"].value or "Morno",
                "proximo_contato": planilha[f"K{linha}"].value or ""
            }

            return lead

    return None


def atualizar_lead(lead):

    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    linha = lead["linha"]

    planilha[f"A{linha}"] = lead.get("nome", "")
    planilha[f"B{linha}"] = lead.get("telefone", "")
    planilha[f"C{linha}"] = lead.get("email", "")
    planilha[f"D{linha}"] = lead.get("interesse", "")
    planilha[f"E{linha}"] = lead.get("origem", "")
    planilha[f"F{linha}"] = lead.get("consultor", "")
    planilha[f"H{linha}"] = lead.get("observacao", "")
    planilha[f"I{linha}"] = lead.get("status", "")
    planilha[f"J{linha}"] = lead.get("historico", "")
    planilha[f"K{linha}"] = lead.get("proximo_contato", "")
    planilha[f"L{linha}"] = lead.get("ultima_interacao", "")
    planilha[f"M{linha}"] = lead.get("prioridade", "")

    arquivo.save("leads.xlsx")


def excluir_lead(linha):
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    planilha.delete_rows(linha)

    arquivo.save("leads.xlsx")



def atualizar_status(telefone, novo_status):

    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    for linha in range(2, planilha.max_row + 1):

        if planilha[f"B{linha}"].value == telefone:

            status_antigo = planilha[f"I{linha}"].value

            planilha[f"I{linha}"] = novo_status

            historico_atual = planilha[f"J{linha}"].value

            novo_historico = (
                f"{historico_atual}\n"
                f"[{agora}] {status_antigo} -> {novo_status}"
            )

            planilha[f"J{linha}"] = novo_historico

            arquivo.save("leads.xlsx")

            return True

    return False



def dashboard():

    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    total = 0

    status_contagem = {
        "Novo": 0,
        "Contato realizado": 0,
        "Proposta enviada": 0,
        "Fechado": 0,
        "Perdido": 0
    }


    for linha in range(2, planilha.max_row + 1):

        nome = planilha[f"A{linha}"].value
        status = planilha[f"I{linha}"].value

        if status is None:
            status = "Novo"

        if nome:

            total += 1

            if status in status_contagem:
                status_contagem[status] += 1


    print("\n===== DASHBOARD =====")

    print(f"\nTotal de leads: {total}\n")


    for status, quantidade in status_contagem.items():

        print(f"{status}: {quantidade}")


    if total > 0:

        conversao = (
            status_contagem["Fechado"]
            / total
        ) * 100

        print(
            f"\nTaxa de conversão: {conversao:.1f}%"
        )


    print("====================\n")    

    print("\n===== FUNIL DE VENDAS =====")

    etapas = {
        "Novo": status_contagem["Novo"],
        "Contato realizado": status_contagem["Contato realizado"],
        "Proposta enviada": status_contagem["Proposta enviada"],
        "Fechado": status_contagem["Fechado"],
        "Perdido": status_contagem["Perdido"]
    }

    for nome, quantidade in etapas.items():
        barra = "█" * quantidade
        print(f"{nome:<18} {barra} {quantidade}")



def listar_followups():

    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    hoje = datetime.now().date()

    atrasados = []
    hoje_lista = []
    proximos = []

    def peso_prioridade(lead):
        ordem = {
            "Quente": 1,
            "Morno": 2,
            "Frio": 3
        }

        return ordem.get(
            lead["prioridade"],
            4
        )

    for linha in range(2, planilha.max_row + 1):

        nome = planilha[f"A{linha}"].value
        telefone = planilha[f"B{linha}"].value
        status = planilha[f"I{linha}"].value
        prioridade = planilha[f"M{linha}"].value
        contato = planilha[f"K{linha}"].value

        if contato:

            try:
                data_contato = datetime.strptime(
                    contato,
                    "%d/%m/%Y"
                ).date()

                lead = {
                    "nome": nome,
                    "telefone": telefone,
                    "status": status,
                    "prioridade": prioridade,
                    "data": contato
                }

                if data_contato < hoje:
                    atrasados.append(lead)

                elif data_contato == hoje:
                    hoje_lista.append(lead)

                else:
                    proximos.append(lead)

            except:
                pass


    atrasados.sort(key=peso_prioridade)
    hoje_lista.sort(key=peso_prioridade)
    proximos.sort(key=peso_prioridade)


    print("\n===== FOLLOW-UPS =====")


    print("\n🔴 ATRASADOS")
    for lead in atrasados:
        print("----------------")
        print(f"Nome: {lead['nome']}")
        print(f"Telefone: {lead['telefone']}")
        print(f"Status: {lead['status']}")
        print(f"Prioridade: {lead['prioridade']}")
        print(f"Contato: {lead['data']}")


    print("\n🟡 HOJE")
    for lead in hoje_lista:
        print("----------------")
        print(f"Nome: {lead['nome']}")
        print(f"Telefone: {lead['telefone']}")
        print(f"Status: {lead['status']}")
        print(f"Prioridade: {lead['prioridade']}")
        print(f"Contato: {lead['data']}")


    print("\n🟢 PRÓXIMOS")
    for lead in proximos:
        print("----------------")
        print(f"Nome: {lead['nome']}")
        print(f"Telefone: {lead['telefone']}")
        print(f"Status: {lead['status']}")
        print(f"Prioridade: {lead['prioridade']}")
        print(f"Contato: {lead['data']}")