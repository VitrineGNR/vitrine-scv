import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="VitrineSCV - Sistema de Controle de Vendas", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f1f3f4;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🎯 VitrineSCV - Sistema Completo de Controle de Vendas</h1>', unsafe_allow_html=True)

# Sidebar com navegação
st.sidebar.title("📋 Menu de Navegação")
st.sidebar.markdown("---")

pagina = st.sidebar.selectbox(
    "Selecione uma seção:",
    ["📊 Dashboard", "👥 Clientes", "📦 Produtos", "🛒 Pedidos", "📈 Relatórios", "⚙️ Configurações"]
)

# Função para dados de exemplo
@st.cache_data
def gerar_dados_vendas():
    datas = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    vendas = [45000 + (i * 1000) + (i % 7 * 2000) for i in range(30)]
    return pd.DataFrame({'Data': datas, 'Vendas': vendas})

# Página Dashboard
if pagina == "📊 Dashboard":
    st.subheader("Dashboard de Vendas - Tempo Real")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Vendas do Mês",
            value="R$ 125.430,00",
            delta="12,5%",
            help="Vendas acumuladas no mês atual"
        )

    with col2:
        st.metric(
            label="📋 Pedidos",
            value="347",
            delta="8,2%",
            help="Total de pedidos no período"
        )

    with col3:
        st.metric(
            label="👥 Clientes Ativos", 
            value="89",
            delta="15,3%",
            help="Clientes com pedidos nos últimos 30 dias"
        )

    with col4:
        st.metric(
            label="📦 Produtos",
            value="1.234",
            delta="-2,1%",
            help="Produtos em estoque"
        )

    st.markdown("---")

    # Gráficos
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📈 Evolução das Vendas (Últimos 30 dias)")
        df_vendas = gerar_dados_vendas()
        fig_vendas = px.line(
            df_vendas, 
            x='Data', 
            y='Vendas',
            title="Vendas Diárias",
            color_discrete_sequence=['#1f77b4']
        )
        fig_vendas.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor (R$)",
            showlegend=False
        )
        st.plotly_chart(fig_vendas, use_container_width=True)

    with col_right:
        st.subheader("📊 Status dos Pedidos")
        status_dados = {
            'Status': ['Processando', 'Enviado', 'Entregue', 'Cancelado'],
            'Quantidade': [25, 45, 60, 5]
        }
        df_status = pd.DataFrame(status_dados)
        fig_status = px.pie(
            df_status,
            values='Quantidade',
            names='Status',
            title="Distribuição de Pedidos"
        )
        st.plotly_chart(fig_status, use_container_width=True)

# Outras páginas
elif pagina == "👥 Clientes":
    st.subheader("👥 Gestão de Clientes")
    st.info("📋 Módulo de gestão de clientes - Em desenvolvimento")

    # Preview da funcionalidade
    with st.expander("🔍 Preview das Funcionalidades"):
        st.write("**Recursos planejados:**")
        st.write("• Cadastro completo de clientes")
        st.write("• Histórico de compras")
        st.write("• Análise de comportamento")
        st.write("• Segmentação de clientes")

elif pagina == "📦 Produtos":
    st.subheader("📦 Catálogo de Produtos") 
    st.info("🛍️ Módulo de produtos - Em desenvolvimento")

    with st.expander("🔍 Preview das Funcionalidades"):
        st.write("**Recursos planejados:**")
        st.write("• Catálogo com imagens")
        st.write("• Controle de estoque")
        st.write("• Preços por representada")
        st.write("• Alertas de estoque baixo")

elif pagina == "🛒 Pedidos":
    st.subheader("🛒 Controle de Pedidos")
    st.info("📋 Módulo de pedidos - Em desenvolvimento")

    with st.expander("🔍 Preview das Funcionalidades"):
        st.write("**Recursos planejados:**")
        st.write("• Criação de propostas")
        st.write("• Conversão proposta → pedido")
        st.write("• Acompanhamento de status")
        st.write("• Geração de PDF")

elif pagina == "📈 Relatórios":
    st.subheader("📈 Relatórios e Análises")
    st.info("📊 Módulo de relatórios - Em desenvolvimento")

    with st.expander("🔍 Preview das Funcionalidades"):
        st.write("**Recursos planejados:**")
        st.write("• Relatórios de vendas")
        st.write("• Análise de comissões")
        st.write("• Performance por representada")
        st.write("• Exportação para Excel/PDF")

elif pagina == "⚙️ Configurações":
    st.subheader("⚙️ Configurações do Sistema")
    st.info("🔧 Módulo de configurações - Em desenvolvimento")

    with st.expander("🔍 Preview das Funcionalidades"):
        st.write("**Recursos planejados:**")
        st.write("• Configuração de representadas")
        st.write("• Upload de logomarcas")
        st.write("• Configuração de impostos")
        st.write("• Backup de dados")

# Sidebar - Informações do sistema
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Acesso Mobile")
st.sidebar.success("✅ Otimizado para iPad")
st.sidebar.info("📍 Perfeito para visitas a clientes")

st.sidebar.markdown("### 🔗 Links Úteis")
st.sidebar.markdown("[📚 Documentação](https://vitrinescv.streamlit.app)")
st.sidebar.markdown("[💬 Suporte](mailto:suporte@vitrinescv.com)")

# Footer
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**📧 Contato:** suporte@vitrinescv.com")

with col_footer2:  
    st.markdown("**🌐 Status:** Sistema Online ✅")

with col_footer3:
    st.markdown("**📱 Versão:** 1.0.0 Beta")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "<strong>VitrineSCV</strong> - Sistema completo para controle de vendas | "
    "Desenvolvido para acesso via iPad durante visitas a clientes"
    "</div>", 
    unsafe_allow_html=True
)