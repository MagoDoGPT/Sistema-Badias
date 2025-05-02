import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração da página
st.set_page_config(
    page_title="Controle de Serviços - Móveis Planejados",
    page_icon="🏭",
    layout="wide"
)

# Função para carregar dados do CSV
def carregar_dados():
    if os.path.exists('servicos.csv'):
        return pd.read_csv('servicos.csv', parse_dates=['data_inicio', 'prazo_entrega'])
    return pd.DataFrame(columns=[
        'marceneiro', 'cliente', 'data_inicio', 'prazo_entrega',
        'status', 'tempo_corte', 'observacoes'
    ])

# Função para salvar dados no CSV
def salvar_dados(df):
    df.to_csv('servicos.csv', index=False)

# Função para verificar status do prazo
def verificar_prazo(prazo):
    hoje = datetime.now().date()
    prazo = pd.to_datetime(prazo).date()
    dias_ate_prazo = (prazo - hoje).days
    
    if dias_ate_prazo < 0:
        return "atrasado", "🔴"
    elif dias_ate_prazo <= 3:
        return "proximo", "🟡"
    else:
        return "normal", "🟢"

# Inicialização do estado da sessão
if 'servicos' not in st.session_state:
    st.session_state.servicos = carregar_dados()

# Função para calcular o tempo de corte
def calcular_tempo_corte(detalhes_projeto):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em marcenaria que calcula tempos de corte para projetos."},
                {"role": "user", "content": f"""
                Calcule o tempo estimado de corte para o seguinte projeto de móveis planejados.
                Considere:
                - Complexidade do projeto
                - Quantidade de peças
                - Tipo de material
                - Acabamentos necessários
                
                Detalhes do projeto:
                {detalhes_projeto}
                
                Forneça o tempo estimado em horas.
                """}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao calcular tempo de corte: {str(e)}")
        return "Erro no cálculo"

# Sidebar para adicionar novo serviço
with st.sidebar:
    st.title("Novo Serviço")
    
    marceneiro = st.text_input("Nome do Marceneiro")
    cliente = st.text_input("Nome do Cliente")
    data_inicio = st.date_input("Data de Início")
    prazo_entrega = st.date_input("Prazo de Entrega")
    detalhes_projeto = st.text_area("Detalhes do Projeto")
    
    if st.button("Adicionar Serviço"):
        if marceneiro and cliente and data_inicio and prazo_entrega:
            # Calcular tempo de corte
            tempo_corte = calcular_tempo_corte(detalhes_projeto)
            
            # Adicionar novo serviço
            novo_servico = pd.DataFrame([{
                'marceneiro': marceneiro,
                'cliente': cliente,
                'data_inicio': data_inicio,
                'prazo_entrega': prazo_entrega,
                'status': 'Em andamento',
                'tempo_corte': tempo_corte,
                'observacoes': detalhes_projeto
            }])
            
            st.session_state.servicos = pd.concat([st.session_state.servicos, novo_servico], ignore_index=True)
            salvar_dados(st.session_state.servicos)
            st.success("Serviço adicionado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

# Título principal
st.title("🏭 Controle de Serviços - Móveis Planejados")

# Tabs para diferentes visualizações
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Serviços em Andamento", "Relatórios"])

with tab1:
    st.header("Visão Geral dos Serviços")
    
    # Verificar prazos próximos e atrasados
    if not st.session_state.servicos.empty:
        servicos_atrasados = []
        servicos_proximos = []
        
        for _, servico in st.session_state.servicos.iterrows():
            status_prazo, _ = verificar_prazo(servico['prazo_entrega'])
            if status_prazo == "atrasado":
                servicos_atrasados.append(servico)
            elif status_prazo == "proximo":
                servicos_proximos.append(servico)
        
        if servicos_atrasados:
            st.error("⚠️ Serviços Atrasados:")
            for servico in servicos_atrasados:
                st.write(f"- {servico['cliente']} (Prazo: {servico['prazo_entrega'].strftime('%d/%m/%Y')})")
        
        if servicos_proximos:
            st.warning("⚠️ Serviços com Prazo Próximo:")
            for servico in servicos_proximos:
                st.write(f"- {servico['cliente']} (Prazo: {servico['prazo_entrega'].strftime('%d/%m/%Y')})")
    
    # Gráfico de serviços por status
    if not st.session_state.servicos.empty:
        fig = px.pie(
            st.session_state.servicos,
            names='status',
            title='Distribuição de Serviços por Status'
        )
        st.plotly_chart(fig)

with tab2:
    st.header("Serviços em Andamento")
    
    if not st.session_state.servicos.empty:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_marceneiro = st.selectbox(
                "Filtrar por Marceneiro",
                ['Todos'] + list(st.session_state.servicos['marceneiro'].unique())
            )
        with col2:
            filtro_status = st.selectbox(
                "Filtrar por Status",
                ['Todos'] + list(st.session_state.servicos['status'].unique())
            )
        
        # Aplicar filtros
        df_filtrado = st.session_state.servicos
        if filtro_marceneiro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['marceneiro'] == filtro_marceneiro]
        if filtro_status != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]
        
        # Exibir tabela responsiva
        st.dataframe(
            df_filtrado.style.applymap(
                lambda x: 'color: red' if isinstance(x, pd.Timestamp) and x.date() < datetime.now().date() else '',
                subset=['prazo_entrega']
            ),
            column_config={
                'marceneiro': st.column_config.TextColumn('Marceneiro'),
                'cliente': st.column_config.TextColumn('Cliente'),
                'data_inicio': st.column_config.DateColumn('Data de Início'),
                'prazo_entrega': st.column_config.DateColumn('Prazo de Entrega'),
                'status': st.column_config.TextColumn('Status'),
                'tempo_corte': st.column_config.TextColumn('Tempo de Corte'),
                'observacoes': st.column_config.TextColumn('Observações'),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Botões de ação para cada serviço
        for idx, servico in df_filtrado.iterrows():
            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
            with col1:
                status_prazo, emoji = verificar_prazo(servico['prazo_entrega'])
                st.write(f"{emoji} **Status do Prazo:** {status_prazo.upper()}")
            with col2:
                if st.button("✅ Concluir", key=f"concluir_{idx}"):
                    st.session_state.servicos.loc[idx, 'status'] = 'Concluído'
                    salvar_dados(st.session_state.servicos)
                    st.rerun()
            with col3:
                if st.button("❌ Excluir", key=f"excluir_{idx}"):
                    st.session_state.servicos = st.session_state.servicos.drop(idx)
                    salvar_dados(st.session_state.servicos)
                    st.rerun()
            st.write("---")
    else:
        st.info("Nenhum serviço cadastrado.")

with tab3:
    st.header("Relatórios")
    
    if not st.session_state.servicos.empty:
        # Estatísticas gerais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Serviços", len(st.session_state.servicos))
        with col2:
            st.metric(
                "Serviços em Andamento",
                len(st.session_state.servicos[st.session_state.servicos['status'] == 'Em andamento'])
            )
        with col3:
            st.metric(
                "Serviços Concluídos",
                len(st.session_state.servicos[st.session_state.servicos['status'] == 'Concluído'])
            )
        
        # Gráfico de tempo de corte por marceneiro
        fig = px.bar(
            st.session_state.servicos,
            x='marceneiro',
            y='tempo_corte',
            title='Tempo de Corte por Marceneiro',
            labels={'tempo_corte': 'Tempo de Corte (horas)'}
        )
        st.plotly_chart(fig)
    else:
        st.info("Nenhum dado disponível para relatórios.") 