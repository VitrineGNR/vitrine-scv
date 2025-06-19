# 🚀 VitrineSCV - Guia de Deploy Oracle Cloud

## Status Atual do Projeto
- **Configuração Oracle Cloud**: 2 OCPUs + 12GB RAM (Always Free)
- **Sistema Operacional**: Ubuntu 22.04
- **Objetivo**: Deploy do sistema de controle de vendas para acesso via iPad

## Próximos Passos (Checklist)

### 1. ✅ Verificar Status da Instância Oracle Cloud
```bash
# Conectar via SSH
ssh -i /caminho/para/chave-privada.key ubuntu@SEU_IP_PUBLICO

# Verificar recursos
lscpu | grep "CPU(s):"
free -h | grep Mem
df -h
```

### 2. ⚙️ Configurar Ambiente Base
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências essenciais
sudo apt install python3.11 python3.11-venv python3.11-pip git nginx firewalld htop screen -y

# Configurar firewall
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --reload
```

### 3. 📦 Clonar e Configurar VitrineSCV
```bash
# Clonar repositório
cd ~
git clone https://github.com/vitrinegnr/vitrinescv.git
cd vitrinescv

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 🌐 Configurar Nginx (Proxy Reverso)
```bash
# Criar configuração Nginx
sudo nano /etc/nginx/sites-available/vitrinescv
```

**Cole este conteúdo (substitua SEU_IP pelo IP público):**
```nginx
server {
    listen 80;
    server_name SEU_IP;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Ativar configuração
sudo ln -s /etc/nginx/sites-available/vitrinescv /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 5. ▶️ Executar VitrineSCV
```bash
# Executar em sessão persistente
screen -S vitrinescv
cd ~/vitrinescv
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Para sair do screen: Ctrl+A, depois D
# Para reconectar: screen -r vitrinescv
```

### 6. ✅ Verificações Finais
- [ ] Acesso via navegador: `http://SEU_IP`
- [ ] Dashboard carrega corretamente
- [ ] Upload de planilhas funciona
- [ ] Geração de PDFs operacional
- [ ] Teste via iPad Safari

## Performance Esperada (2 OCPUs + 12GB)
- **Geração de PDFs**: 5-10 segundos
- **Dashboard**: 3-5 segundos de carregamento
- **Usuários simultâneos**: 5-8 sem problemas

## Troubleshooting Comum

### Erro de Conexão
```bash
# Verificar se serviços estão rodando
sudo systemctl status nginx
sudo systemctl status firewalld
ss -tlnp | grep 8501
```

### Erro de Dependências
```bash
# Reinstalar dependências
cd ~/vitrinescv
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Security Lists Oracle Cloud
Se não conseguir acessar, configure no console Oracle:
1. **VCN > Security Lists > Default Security List**
2. **Add Ingress Rules:**
   - Source CIDR: `0.0.0.0/0`
   - Destination Port: `80`
   - Protocol: TCP

## URLs de Acesso
- **Desktop**: `http://SEU_IP_PUBLICO`
- **iPad**: `http://SEU_IP_PUBLICO` (via Safari)

## Backup de Dados
```bash
# Configurar backup automático
crontab -e

# Adicionar linha para backup diário às 2h:
0 2 * * * tar -czf /home/ubuntu/backup-$(date +%Y%m%d).tar.gz /home/ubuntu/vitrinescv
```

---

**Recursos Always Free Utilizados:**
- ✅ 2 OCPUs / 4 OCPUs disponíveis
- ✅ 12GB RAM / 24GB disponíveis
- ✅ 47GB disco / 200GB disponíveis
- ✅ Custo: R$ 0,00/mês permanente