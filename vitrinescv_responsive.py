
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_js_eval import streamlit_js_eval

class VitrineSCVResponsive:
    """Classe principal para o sistema VitrineSCV com interface responsiva"""

    def __init__(self):
        self.device_info = self.detect_device()
        self.setup_page_config()
        self.apply_mobile_css()

    def detect_device(self):
        """Detecta o tipo de dispositivo e suas características"""
        try:
            # Detectar largura da tela
            width = streamlit_js_eval(js_expressions="window.innerWidth", key="width", want_output=True)
            height = streamlit_js_eval(js_expressions="window.innerHeight", key="height", want_output=True)

            # Detectar user agent para identificar dispositivo
            user_agent = streamlit_js_eval(js_expressions="navigator.userAgent", key="ua", want_output=True)

            # Detectar se é touch device
            is_touch = streamlit_js_eval(js_expressions="'ontouchstart' in window", key="touch", want_output=True)

            # Detectar orientação
            orientation = streamlit_js_eval(js_expressions="screen.orientation ? screen.orientation.angle : 0", key="orient", want_output=True)

            device_type = self.classify_device(width, height, user_agent)

            return {
                "width": width or 1200,
                "height": height or 800,
                "user_agent": user_agent or "",
                "is_touch": is_touch or False,
                "orientation": orientation or 0,
                "device_type": device_type
            }
        except Exception as e:
            # Fallback para dispositivos que não suportam JS
            return {
                "width": 1200,
                "height": 800,
                "user_agent": "",
                "is_touch": False,
                "orientation": 0,
                "device_type": "desktop"
            }

    def classify_device(self, width, height, user_agent):
        """Classifica o tipo de dispositivo baseado nas características"""
        if width is None:
            return "desktop"

        # Detectar por user agent primeiro
        user_agent = (user_agent or "").lower()
        if any(device in user_agent for device in ["iphone", "android", "mobile"]):
            return "smartphone"
        elif any(device in user_agent for device in ["ipad", "tablet"]):
            return "tablet"

        # Detectar por largura da tela
        if width <= 480:
            return "smartphone"
        elif width <= 768:
            return "small_tablet"
        elif width <= 1024:
            return "tablet"
        else:
            return "desktop"

    def setup_page_config(self):
        """Configura a página baseada no dispositivo"""
        device_type = self.device_info["device_type"]

        if device_type == "smartphone":
            st.set_page_config(
                page_title="VitrineSCV",
                page_icon="📱",
                layout="centered",
                initial_sidebar_state="collapsed",
                menu_items={
                    'Get Help': None,
                    'Report a bug': None,
                    'About': "VitrineSCV - Sistema de Controle de Vendas"
                }
            )
        elif device_type in ["tablet", "small_tablet"]:
            st.set_page_config(
                page_title="VitrineSCV - Tablet",
                page_icon="📱",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        else:  # desktop
            st.set_page_config(
                page_title="VitrineSCV - Sistema de Controle de Vendas",
                page_icon="💼",
                layout="wide",
                initial_sidebar_state="expanded"
            )

    def apply_mobile_css(self):
        """Aplica CSS responsivo baseado no dispositivo"""
        device_type = self.device_info["device_type"]
        width = self.device_info["width"]

        # CSS base responsivo
        css = """
        <style>
        /* Reset e base */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }

        /* Botões touch-friendly */
        .stButton > button {
            min-height: 44px;
            font-size: 16px !important;
            border-radius: 8px;
            font-weight: 500;
        }

        /* Inputs otimizados para mobile */
        .stTextInput > div > div > input,
        .stSelectbox select,
        .stNumberInput > div > div > input {
            font-size: 16px !important;
            padding: 12px !important;
            border-radius: 8px;
        }

        /* Métricas responsivas */
        .metric-container {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        """

        # CSS específico por dispositivo
        if device_type == "smartphone":
            css += """
            /* Mobile específico */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }

            .stButton > button {
                width: 100%;
                margin-bottom: 0.5rem;
            }

            .stDataFrame {
                font-size: 12px;
                overflow-x: auto;
            }

            /* Ocultar elementos não essenciais no mobile */
            .st-emotion-cache-1y4p8pa {
                padding: 0.5rem;
            }

            /* Sidebar compacta no mobile */
            .css-1d391kg {
                width: 280px;
            }
            """

        elif device_type in ["tablet", "small_tablet"]:
            css += """
            /* Tablet específico */
            .main .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
                max-width: 1000px;
            }

            .stColumns > div {
                padding: 0.5rem;
            }
            """

        else:  # desktop
            css += """
            /* Desktop específico */
            .main .block-container {
                max-width: 1200px;
                padding: 3rem 1rem;
            }
            """

        css += "</style>"
        st.markdown(css, unsafe_allow_html=True)

    def create_responsive_layout(self):
        """Cria layout responsivo baseado no dispositivo"""
        device_type = self.device_info["device_type"]

        if device_type == "smartphone":
            return self.create_mobile_layout()
        elif device_type in ["tablet", "small_tablet"]:
            return self.create_tablet_layout()
        else:
            return self.create_desktop_layout()

    def create_mobile_layout(self):
        """Layout otimizado para smartphone"""
        # Header compacto
        st.markdown("# 📱 VitrineSCV")

        # Menu hambúrguer
        with st.expander("📋 Menu Principal", expanded=False):
            menu_option = st.selectbox(
                "Escolha uma opção:",
                ["Dashboard", "Clientes", "Produtos", "Pedidos", "Relatórios", "Configurações"],
                key="mobile_menu"
            )

        # Informações do dispositivo (debug)
        if st.checkbox("ℹ️ Info do Dispositivo"):
            st.json(self.device_info)

        return menu_option

    def create_tablet_layout(self):
        """Layout otimizado para tablet"""
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("# 📱 VitrineSCV - Tablet")
        with col2:
            st.markdown(f"**{self.device_info['width']}x{self.device_info['height']}**")

        # Menu lateral expandido
        with st.sidebar:
            st.markdown("### 🎯 Navegação")
            menu_option = st.radio(
                "Escolha uma seção:",
                ["Dashboard", "Clientes", "Produtos", "Pedidos", "Relatórios", "Configurações"],
                key="tablet_menu"
            )

            # Métricas rápidas na sidebar
            st.markdown("---")
            st.markdown("### 📊 Resumo Rápido")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Vendas", "125", "12%")
            with col2:
                st.metric("Clientes", "1.2K", "5%")

        return menu_option

    def create_desktop_layout(self):
        """Layout otimizado para desktop"""
        # Header completo
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("# 💼 VitrineSCV - Sistema de Controle de Vendas")
        with col2:
            st.markdown(f"**Resolução:** {self.device_info['width']}x{self.device_info['height']}")
        with col3:
            st.markdown(f"**Dispositivo:** {self.device_info['device_type'].title()}")

        # Sidebar completa
        with st.sidebar:
            st.markdown("### 🎯 Navegação Principal")
            menu_option = st.selectbox(
                "Selecione o módulo:",
                ["Dashboard", "Clientes", "Produtos", "Pedidos", "Relatórios", "Configurações"],
                key="desktop_menu"
            )

            st.markdown("---")
            st.markdown("### 📊 Métricas Principais")

            # Grid de métricas
            metrics_data = [
                ("Vendas Hoje", "R$ 12.5K", "8.2%"),
                ("Clientes Ativos", "1.247", "3.1%"),
                ("Pedidos Pendentes", "23", "-5%"),
                ("Comissões", "R$ 2.1K", "12%")
            ]

            for label, value, delta in metrics_data:
                st.metric(label, value, delta)

        return menu_option

    def render_content(self, menu_option):
        """Renderiza o conteúdo baseado na opção do menu"""
        device_type = self.device_info["device_type"]

        if menu_option == "Dashboard":
            self.render_dashboard()
        elif menu_option == "Clientes":
            self.render_clientes()
        elif menu_option == "Produtos":
            self.render_produtos()
        elif menu_option == "Pedidos":
            self.render_pedidos()
        elif menu_option == "Relatórios":
            self.render_relatorios()
        else:
            self.render_configuracoes()

    def render_dashboard(self):
        """Renderiza o dashboard responsivo"""
        device_type = self.device_info["device_type"]

        st.markdown("## 📊 Dashboard")

        if device_type == "smartphone":
            # Layout vertical para mobile
            st.metric("Vendas do Mês", "R$ 125.000", "12%")
            st.metric("Clientes Ativos", "1.247", "5%")
            st.metric("Pedidos", "89", "8%")

            # Gráfico otimizado para mobile
            chart_data = pd.DataFrame({
                'Dia': list(range(1, 8)),
                'Vendas': [1000, 1200, 900, 1500, 1800, 1100, 1400]
            })

            fig = px.line(chart_data, x='Dia', y='Vendas', 
                         title="Vendas da Semana",
                         height=300)
            fig.update_layout(
                font_size=12,
                title_font_size=14
            )
            st.plotly_chart(fig, use_container_width=True)

        elif device_type in ["tablet", "small_tablet"]:
            # Layout em grid para tablet
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Vendas do Mês", "R$ 125.000", "12%")
            with col2:
                st.metric("Clientes Ativos", "1.247", "5%")
            with col3:
                st.metric("Pedidos", "89", "8%")

            # Gráficos lado a lado
            col1, col2 = st.columns(2)
            with col1:
                chart_data = pd.DataFrame({
                    'Categoria': ['Eletrônicos', 'Roupas', 'Casa'],
                    'Vendas': [30000, 45000, 25000]
                })
                fig = px.pie(chart_data, names='Categoria', values='Vendas',
                           title="Vendas por Categoria")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                chart_data = pd.DataFrame({
                    'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                    'Vendas': [80000, 95000, 120000, 110000, 125000]
                })
                fig = px.bar(chart_data, x='Mês', y='Vendas',
                           title="Vendas Mensais")
                st.plotly_chart(fig, use_container_width=True)

        else:  # desktop
            # Layout completo para desktop
            col1, col2, col3, col4 = st.columns(4)
            metrics = [
                ("Vendas do Mês", "R$ 125.000", "12%"),
                ("Clientes Ativos", "1.247", "5%"),
                ("Pedidos", "89", "8%"),
                ("Comissões", "R$ 8.500", "15%")
            ]

            for col, (label, value, delta) in zip([col1, col2, col3, col4], metrics):
                with col:
                    st.metric(label, value, delta)

            # Gráficos em layout avançado
            col1, col2 = st.columns([2, 1])
            with col1:
                # Gráfico principal
                chart_data = pd.DataFrame({
                    'Data': pd.date_range('2024-01-01', periods=30, freq='D'),
                    'Vendas': [1000 + i*50 + (i%7)*200 for i in range(30)]
                })
                fig = px.line(chart_data, x='Data', y='Vendas',
                            title="Evolução de Vendas - Últimos 30 dias")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Ranking de produtos
                st.markdown("### 🏆 Top Produtos")
                products_data = pd.DataFrame({
                    'Produto': ['Smartphone XYZ', 'Notebook ABC', 'Fone Premium'],
                    'Vendas': [25, 18, 12]
                })
                st.dataframe(products_data, use_container_width=True)

    def render_clientes(self):
        """Renderiza a tela de clientes"""
        st.markdown("## 👥 Gestão de Clientes")

        # Interface adaptada por dispositivo
        device_type = self.device_info["device_type"]

        if device_type == "smartphone":
            # Mobile: formulário vertical
            with st.form("cliente_form"):
                nome = st.text_input("Nome do Cliente")
                email = st.text_input("E-mail")
                telefone = st.text_input("Telefone")
                submit = st.form_submit_button("💾 Salvar Cliente", use_container_width=True)
        else:
            # Tablet/Desktop: formulário em colunas
            with st.form("cliente_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome do Cliente")
                    telefone = st.text_input("Telefone")
                with col2:
                    email = st.text_input("E-mail")
                    submit = st.form_submit_button("💾 Salvar Cliente")

    def render_produtos(self):
        """Renderiza a tela de produtos"""
        st.markdown("## 🏷️ Catálogo de Produtos")
        st.info("📱 Interface otimizada para " + self.device_info["device_type"])

    def render_pedidos(self):
        """Renderiza a tela de pedidos"""
        st.markdown("## 📋 Gestão de Pedidos")
        st.info("📱 Interface otimizada para " + self.device_info["device_type"])

    def render_relatorios(self):
        """Renderiza a tela de relatórios"""
        st.markdown("## 📊 Relatórios e Análises")
        st.info("📱 Interface otimizada para " + self.device_info["device_type"])

    def render_configuracoes(self):
        """Renderiza a tela de configurações"""
        st.markdown("## ⚙️ Configurações")
        st.info("📱 Interface otimizada para " + self.device_info["device_type"])

        # Mostrar informações do dispositivo
        st.markdown("### 📱 Informações do Dispositivo")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Tipo:** {self.device_info['device_type']}")
            st.markdown(f"**Largura:** {self.device_info['width']}px")
            st.markdown(f"**Touch:** {'Sim' if self.device_info['is_touch'] else 'Não'}")
        with col2:
            st.markdown(f"**Altura:** {self.device_info['height']}px")
            st.markdown(f"**Orientação:** {self.device_info['orientation']}°")

def main():
    """Função principal da aplicação"""
    # Inicializar sistema responsivo
    app = VitrineSCVResponsive()

    # Criar layout responsivo
    menu_option = app.create_responsive_layout()

    # Renderizar conteúdo
    app.render_content(menu_option)

    # Footer responsivo
    st.markdown("---")
    device_info = app.device_info
    st.markdown(f"🔧 **VitrineSCV v2.0** | Dispositivo: {device_info['device_type']} | {device_info['width']}x{device_info['height']}")

if __name__ == "__main__":
    main()
