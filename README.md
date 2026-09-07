# Zarken Leads

Aplicação desktop para organizar e acompanhar leads comerciais. O projeto centraliza cadastros, históricos, follow-ups e informações de contato em uma interface simples, desenvolvida para uso local.

## Funcionalidades

- Cadastro, consulta, edição e exclusão de leads
- Busca por telefone
- Histórico de status e prioridades
- Follow-ups comerciais
- Dashboard para acompanhar os leads
- Exportação de dados
- Backups locais
- Interface gráfica com Tkinter

## Tecnologias

- Python
- Tkinter
- OpenPyXL
- PyInstaller

## Como executar

```bash
git clone https://github.com/GunnerrR05/LeadFlow.git
cd LeadFlow
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## Privacidade e dados

Este repositório contém somente código e recursos visuais. Planilhas de leads, backups, logs e executáveis ficam fora do controle de versão para proteger dados comerciais.

## Estrutura do projeto

```text
componentes/  # Elementos reutilizáveis da interface
servicos/     # Regras de negócio, backup e exportação
telas/        # Telas da aplicação
assets/       # Ícones e imagens
main.py       # Ponto de entrada
```

## Autor

Desenvolvido por [Alan Richard Vieira Silva](https://github.com/GunnerrR05).
