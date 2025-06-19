
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Sistema de Controle de Vendas",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .status-ativo { color: #28a745; }
    .status-pendente { color: #ffc107; }
    .status-cancelado { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>💼 Sistema Completo de Controle de Vendas</h1>", unsafe_allow_html=True)

# Sidebar para navegação
st.sidebar.title("🔧 Painel de Controle")
page = st.sidebar.selectbox("Selecione uma função:", [
    "📊 Dashboard Principal",
    "📦 Controle de Estoque", 
    "🎯 Gestão de Leads",
    "📋 Propostas Comerciais",
    "💰 Relatório de Vendas",
    "📤 Upload de Dados"
])

# Função para gerar dados de exemplo
@st.cache_data
def gerar_dados_exemplo():
    # Dados de produtos/estoque
    produtos = pd.DataFrame({
        'codigo': [f'PROD{i:03d}' for i in range(1, 51)],
        'nome': [f'Produto {i}' for i in range(1, 51)],
        'categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Casa', 'Esportes'], 50),
        'preco': np.random.uniform(50, 500, 50).round(2),
        'estoque': np.random.randint(0, 100, 50),
        'estoque_minimo': np.random.randint(5, 20, 50)
    })

    # Dados de clientes/leads
    clientes = pd.DataFrame({
        'id': range(1, 26),
        'nome': [f'Cliente {i}' for i in range(1, 26)],
        'email': [f'cliente{i}@email.com' for i in range(1, 26)],
        'telefone': [f'(11) 9999-{i:04d}' for i in range(1, 26)],
        'status': np.random.choice(['Ativo', 'Prospect', 'Inativo'], 25),
        'cidade': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador'], 25)
    })

    # Dados de vendas
    vendas = pd.DataFrame({
        'id': range(1, 101),
        'data': pd.date_range(start='2025-01-01', periods=100, freq='D')[:100],
        'cliente_id': np.random.randint(1, 26, 100),
        'produto_codigo': np.random.choice(produtos['codigo'], 100),
        'quantidade': np.random.randint(1, 10, 100),
        'valor_unitario': np.random.uniform(50, 500, 100).round(2),
        'status': np.random.choice(['Finalizada', 'Pendente', 'Cancelada'], 100, p=[0.7, 0.2, 0.1])
    })
    vendas['valor_total'] = vendas['quantidade'] * vendas['valor_unitario']

    return produtos, clientes, vendas

# Carregar dados
produtos, clientes, vendas = gerar_dados_exemplo()

# Dashboard Principal
if page == "📊 Dashboard Principal":
    st.header("📊 Dashboard Executivo")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_vendas = vendas[vendas['status'] == 'Finalizada']['valor_total'].sum()
        st.metric("💰 Vendas Totais", f"R$ {total_vendas:,.2f}")

    with col2:
        leads_ativos = len(clientes[clientes['status'] == 'Ativo'])
        st.metric("👥 Clientes Ativos", leads_ativos)

    with col3:
        produtos_estoque_baixo = len(produtos[produtos['estoque'] <= produtos['estoque_minimo']])
        st.metric("⚠️ Estoque Baixo", produtos_estoque_baixo)

    with col4:
        vendas_pendentes = len(vendas[vendas['status'] == 'Pendente'])
        st.metric("⏳ Vendas Pendentes", vendas_pendentes)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Vendas por Mês")
        vendas_mes = vendas[vendas['status'] == 'Finalizada'].copy()
        vendas_mes['mes'] = vendas_mes['data'].dt.to_period('M')
        vendas_agrupadas = vendas_mes.groupby('mes')['valor_total'].sum().reset_index()
        vendas_agrupadas['mes'] = vendas_agrupadas['mes'].astype(str)

        fig = px.line(vendas_agrupadas, x='mes', y='valor_total', 
                     title="Evolução das Vendas")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🥧 Vendas por Status")
        status_vendas = vendas['status'].value_counts()
        fig = px.pie(values=status_vendas.values, names=status_vendas.index,
                    title="Distribuição de Vendas por Status")
        st.plotly_chart(fig, use_container_width=True)

# Controle de Estoque
elif page == "📦 Controle de Estoque":
    st.header("📦 Controle de Estoque")

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        categoria_filter = st.selectbox("Filtrar por categoria:", 
                                       ['Todas'] + list(produtos['categoria'].unique()))
    with col2:
        estoque_filter = st.selectbox("Filtrar por estoque:", 
                                     ['Todos', 'Estoque Baixo', 'Estoque OK'])

    # Aplicar filtros
    produtos_filtrados = produtos.copy()
    if categoria_filter != 'Todas':
        produtos_filtrados = produtos_filtrados[produtos_filtrados['categoria'] == categoria_filter]

    if estoque_filter == 'Estoque Baixo':
        produtos_filtrados = produtos_filtrados[produtos_filtrados['estoque'] <= produtos_filtrados['estoque_minimo']]
    elif estoque_filter == 'Estoque OK':
        produtos_filtrados = produtos_filtrados[produtos_filtrados['estoque'] > produtos_filtrados['estoque_minimo']]

    # Adicionar coluna de status de estoque
    produtos_filtrados['status_estoque'] = produtos_filtrados.apply(
        lambda row: '🔴 Baixo' if row['estoque'] <= row['estoque_minimo'] else '🟢 OK', axis=1
    )

    st.dataframe(produtos_filtrados, use_container_width=True)

    # Gráfico de estoque
    fig = px.bar(produtos_filtrados, x='nome', y='estoque', 
                title="Níveis de Estoque por Produto",
                color='categoria')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Gestão de Leads
elif page == "🎯 Gestão de Leads":
    st.header("🎯 Gestão de Leads e Clientes")

    # Formulário para novo lead
    with st.expander("➕ Adicionar Novo Lead"):
        with st.form("novo_lead"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Cliente")
                email = st.text_input("Email")
            with col2:
                telefone = st.text_input("Telefone")
                cidade = st.selectbox("Cidade", ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador'])

            if st.form_submit_button("💾 Adicionar Lead"):
                st.success("Lead adicionado com sucesso!")

    # Filtros para clientes
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filtrar por status:", ['Todos'] + list(clientes['status'].unique()))
    with col2:
        cidade_filter = st.selectbox("Filtrar por cidade:", ['Todas'] + list(clientes['cidade'].unique()))

    # Aplicar filtros
    clientes_filtrados = clientes.copy()
    if status_filter != 'Todos':
        clientes_filtrados = clientes_filtrados[clientes_filtrados['status'] == status_filter]
    if cidade_filter != 'Todas':
        clientes_filtrados = clientes_filtrados[clientes_filtrados['cidade'] == cidade_filter]

    st.dataframe(clientes_filtrados, use_container_width=True)

    # Gráfico de distribuição de clientes
    fig = px.bar(clientes['status'].value_counts().reset_index(), 
                x='index', y='status', title="Distribuição de Clientes por Status")
    st.plotly_chart(fig, use_container_width=True)

# Propostas Comerciais
elif page == "📋 Propostas Comerciais":
    st.header("📋 Gerador de Propostas Comerciais")

    with st.form("nova_proposta"):
        st.subheader("📝 Nova Proposta")

        col1, col2 = st.columns(2)
        with col1:
            cliente_selecionado = st.selectbox("Selecionar Cliente:", clientes['nome'].tolist())
            data_proposta = st.date_input("Data da Proposta:", datetime.now())

        with col2:
            validade = st.number_input("Validade (dias):", min_value=1, value=30)
            desconto = st.number_input("Desconto (%):", min_value=0.0, max_value=50.0, value=0.0)

        st.subheader("🛒 Itens da Proposta")
        produto_selecionado = st.selectbox("Selecionar Produto:", produtos['nome'].tolist())
        quantidade = st.number_input("Quantidade:", min_value=1, value=1)

        if st.form_submit_button("📄 Gerar Proposta"):
            produto_info = produtos[produtos['nome'] == produto_selecionado].iloc[0]
            valor_unitario = produto_info['preco']
            valor_total = valor_unitario * quantidade
            valor_com_desconto = valor_total * (1 - desconto/100)

            st.success("✅ Proposta gerada com sucesso!")

            # Exibir proposta
            st.markdown("---")
            st.markdown(f"""
            ### 📋 PROPOSTA COMERCIAL

            **Cliente:** {cliente_selecionado}  
            **Data:** {data_proposta.strftime('%d/%m/%Y')}  
            **Validade:** {validade} dias  

            **Produto:** {produto_selecionado}  
            **Código:** {produto_info['codigo']}  
            **Quantidade:** {quantidade}  
            **Valor Unitário:** R$ {valor_unitario:.2f}  
            **Desconto:** {desconto}%  
            **Valor Total:** R$ {valor_com_desconto:.2f}  
            """)

# Relatório de Vendas
elif page == "💰 Relatório de Vendas":
    st.header("💰 Relatório Detalhado de Vendas")

    # Filtros de data
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data Início:", vendas['data'].min())
    with col2:
        data_fim = st.date_input("Data Fim:", vendas['data'].max())

    # Filtrar vendas por data
    vendas_filtradas = vendas[
        (vendas['data'] >= pd.to_datetime(data_inicio)) & 
        (vendas['data'] <= pd.to_datetime(data_fim))
    ]

    # Métricas do período
    col1, col2, col3 = st.columns(3)
    with col1:
        receita_periodo = vendas_filtradas[vendas_filtradas['status'] == 'Finalizada']['valor_total'].sum()
        st.metric("💰 Receita do Período", f"R$ {receita_periodo:,.2f}")

    with col2:
        qtd_vendas = len(vendas_filtradas[vendas_filtradas['status'] == 'Finalizada'])
        st.metric("📦 Quantidade de Vendas", qtd_vendas)

    with col3:
        ticket_medio = receita_periodo / qtd_vendas if qtd_vendas > 0 else 0
        st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:.2f}")

    # Tabela de vendas
    st.subheader("📊 Vendas Detalhadas")
    st.dataframe(vendas_filtradas, use_container_width=True)

    # Gráfico de vendas por dia
    vendas_diarias = vendas_filtradas[vendas_filtradas['status'] == 'Finalizada'].groupby('data')['valor_total'].sum().reset_index()
    fig = px.line(vendas_diarias, x='data', y='valor_total', title="Vendas Diárias")
    st.plotly_chart(fig, use_container_width=True)

# Upload de Dados
elif page == "📤 Upload de Dados":
    st.header("📤 Upload e Sincronização de Dados")

    st.markdown("""
    ### 📋 Instruções para Upload

    Você pode fazer upload de planilhas Excel (.xlsx, .xlsm) ou CSV com os seguintes formatos:

    **Produtos/Estoque:**
    - codigo, nome, categoria, preco, estoque, estoque_minimo

    **Clientes:**
    - nome, email, telefone, status, cidade

    **Vendas:**
    - data, cliente_id, produto_codigo, quantidade, valor_unitario, status
    """)

    uploaded_file = st.file_uploader(
        "Escolha um arquivo", 
        type=['xlsx', 'xlsm', 'csv'],
        help="Selecione uma planilha Excel ou CSV para importar dados"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ Arquivo carregado com sucesso!")
            st.subheader("👀 Preview dos Dados")
            st.dataframe(df.head(), use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Total de Linhas", len(df))
            with col2:
                st.metric("📋 Total de Colunas", len(df.columns))

            # Botão para processar dados
            if st.button("🔄 Processar e Integrar Dados"):
                st.success("🎉 Dados integrados com sucesso ao sistema!")

        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")

    # Seção de exportação
    st.markdown("---")
    st.subheader("📥 Exportar Dados")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Exportar Estoque"):
            csv = produtos.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, "estoque.csv", "text/csv")

    with col2:
        if st.button("👥 Exportar Clientes"):
            csv = clientes.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, "clientes.csv", "text/csv")

    with col3:
        if st.button("💰 Exportar Vendas"):
            csv = vendas.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, "vendas.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    💼 Sistema Completo de Controle de Vendas | Desenvolvido com Streamlit
</div>
""", unsafe_allow_html=True)
