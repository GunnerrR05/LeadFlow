from excel import salvar_lead, listar_leads, atualizar_status, dashboard, listar_followups

def cadastrar_lead():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    interesse = input("Interesse: ")
    origem = input("Origem: ")
    consultor = input("Consultor: ")
    observacoes = input("Observações: ")
    proximo_contato = input("Próximo contato (DD/MM/AAAA): ")
    ultima_interacao = input("Última interação: ")
    print("""
    Prioridade:
    1 - Quente
    2 - Morno
    3 - Frio
    """)
    opcao_prioridade = input("Escolha: ")
    prioridades = {
        "1": "Quente",
        "2": "Morno",
        "3": "Frio"
    }
    prioridade = prioridades.get(opcao_prioridade, "Morno")



    return{
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "interesse": interesse,
        "origem": origem,
        "consultor": consultor,
        "observacao": observacoes,
        "status": "Novo",
        "prioridade": prioridade,
        "proximo_contato": proximo_contato,
        "ultima_interacao": ultima_interacao
    }


while True:
    print("\n===== MENU =====")
    print("1 - Cadastrar lead")
    print("2 - Listar leads")
    print("3 - Atualizar status")
    print("4 - Dashboard")
    print("5 - Follow-ups")
    print("6 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        lead = cadastrar_lead()
        salvar_lead(lead)
        print("Lead cadastrado com sucesso!")

    elif opcao == "2":
        listar_leads()

    elif opcao == "3":

        telefone = input("Telefone do lead: ")

        print("""
    1 - Novo
    2 - Contato realizado
    3 - Proposta enviada
    4 - Fechado
    5 - Perdido
    """)

        escolha = input("Novo status: ")

        status = {
            "1": "Novo",
            "2": "Contato realizado",
            "3": "Proposta enviada",
            "4": "Fechado",
            "5": "Perdido"
        }

        atualizar_status(telefone, status[escolha])

        print("Status atualizado!")

    elif opcao == "4":

        dashboard()

    elif opcao == "5":
        listar_followups()

    elif opcao == "6":
        print("Encerrando o sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")