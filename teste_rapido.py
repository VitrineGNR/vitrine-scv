
# Teste Rápido da Aplicação
import subprocess
import sys
import os

def verificar_instalacao():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando instalação...")

    try:
        import streamlit
        import pandas
        import plotly
        import openpyxl
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def executar_aplicacao():
    """Executa a aplicação Streamlit"""
    print("🚀 Iniciando aplicação...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_controle_vendas.py"])
    except KeyboardInterrupt:
        print("\n⏹️ Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

def main():
    print("=" * 50)
    print("🎯 TESTE RÁPIDO - SISTEMA DE VENDAS")
    print("=" * 50)

    # Verificar se os arquivos existem
    arquivos_necessarios = [
        "app_controle_vendas.py",
        "requirements.txt"
    ]

    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            print("📋 Certifique-se de ter todos os arquivos na mesma pasta")
            return

    print("✅ Todos os arquivos encontrados!")

    # Verificar instalação
    if not verificar_instalacao():
        resposta = input("\n🤔 Instalar dependências automaticamente? (s/n): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            if not instalar_dependencias():
                return
        else:
            print("💡 Execute: pip install -r requirements.txt")
            return

    # Executar aplicação
    print("\n🎉 Tudo pronto! Iniciando aplicação...")
    print("💡 A aplicação abrirá no navegador em: http://localhost:8501")
    print("📱 Para acessar no iPad, use o IP do seu computador")
    print("⏹️ Para parar, pressione Ctrl+C\n")

    executar_aplicacao()

if __name__ == "__main__":
    main()
