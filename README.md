# Controle de Serviços - Móveis Planejados 🏭

Sistema de controle de serviços para fábrica de móveis planejados, desenvolvido com Streamlit e LangChain.

## Funcionalidades

- 📝 Cadastro de serviços com marceneiro e cliente
- ⏰ Controle de prazos com alertas
- ⚡ Cálculo automático de tempo de corte
- 📊 Relatórios e visualizações
- 🔍 Filtros e busca de serviços
- 📈 Métricas de desempenho

## Requisitos

- Python 3.8+
- Chave da API OpenAI

## Instalação

1. Clone o repositório:
```bash
git clone [seu-repositorio]
cd [seu-diretorio]
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto
- Adicione sua chave da API OpenAI:
```
OPENAI_API_KEY=sua_chave_aqui
```

## Uso

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. Acesse a interface web no navegador (geralmente http://localhost:8501)

## Funcionalidades Detalhadas

### Cadastro de Serviços
- Nome do marceneiro
- Nome do cliente
- Data de início
- Prazo de entrega
- Detalhes do projeto

### Controle de Prazos
- Alertas para serviços próximos do prazo
- Visualização de status dos serviços
- Histórico de serviços

### Cálculo de Tempo de Corte
- Análise automática do projeto
- Consideração de complexidade
- Estimativa de tempo em horas

### Relatórios
- Total de serviços
- Serviços em andamento
- Serviços concluídos
- Gráficos de desempenho

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License. 