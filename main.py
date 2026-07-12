from excel import salvar_lead, listar_leads, atualizar_status

def cadastrar_lead():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    interesse = input("Interesse: ")
    origem = input("Origem: ")
    consultor = input("Consultor: ")
    observacoes = input("Observações: ")

    return {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "interesse": interesse,
        "origem": origem,
        "consultor": consultor,
        "observacao": observacoes,
        "status": "Novo"
    }


while True:
    print("\n===== MENU =====")
    print("1 - Cadastrar lead")
    print("2 - Listar leads")
    print("3 - Atualizar status")
    print("4 - Sair")

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
        print("Encerrando o sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")