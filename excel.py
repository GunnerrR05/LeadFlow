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

        print(f"\nLead {linha - 1}")
        print(f"Nome: {nome}")
        print(f"Telefone: {telefone}")
        print(f"E-mail: {email}")
        print(f"Interesse: {interesse}")
        print(f"Origem: {origem}")
        print(f"Consultor: {consultor}")
        print(f"Data: {data}")
        print(f"Observações: {observacao}")
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
                "nome": nome,
                "telefone": planilha[f"B{linha}"].value,
                "email": planilha[f"C{linha}"].value,
                "interesse": planilha[f"D{linha}"].value,
                "origem": planilha[f"E{linha}"].value,
                "consultor": planilha[f"F{linha}"].value,
                "data": planilha[f"G{linha}"].value,
                "observacao": planilha[f"H{linha}"].value
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
                "observacao": planilha[f"H{linha}"].value
            }

            return lead

    return None


def atualizar_lead(lead):
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    linha = lead["linha"]

    planilha[f"A{linha}"] = lead["nome"]
    planilha[f"B{linha}"] = lead["telefone"]
    planilha[f"C{linha}"] = lead["email"]
    planilha[f"D{linha}"] = lead["interesse"]
    planilha[f"E{linha}"] = lead["origem"]
    planilha[f"F{linha}"] = lead["consultor"]
    planilha[f"H{linha}"] = lead["observacao"]

    arquivo.save("leads.xlsx")


def excluir_lead(linha):
    arquivo = load_workbook("leads.xlsx")
    planilha = arquivo.active

    planilha.delete_rows(linha)

    arquivo.save("leads.xlsx")
    

