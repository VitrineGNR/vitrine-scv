# 🚀 VitrineSCV: Checklist de Implementação Imediata

## ✅ FASE 1: PREPARAÇÃO DA ORACLE CLOUD (30 minutos)

### Passo 1.1: Finalizar Criação da Instância Oracle Cloud
```bash
# Configuração exata para usar:
✅ Name: VitrineSCV-Production  
✅ Shape: VM.Standard.A1.Flex  
✅ OCPUs: 2  
✅ Memory: 12 GB  
✅ Image: Ubuntu 22.04  
✅ Network: Public subnet + Assign public IP  
✅ SSH Keys: Generate e baixar AGORA  
```

### Passo 1.2: Configurar Security Lists (5 minutos)
```bash
# Na console Oracle Cloud:
1. Networking > Virtual Cloud Networks > [Sua VCN] > Security Lists
2. Adicionar Ingress Rules:
   - Port 22: SSH (0.0.0.0/0)
   - Port 80: HTTP (0.0.0.0/0)  
   - Port 443: HTTPS (0.0.0.0/0)
   - Port 8000: FastAPI Dev (0.0.0.0/0)
```

### Passo 1.3: Primeiro Acesso SSH
```bash
# Conectar à instância (substitua SEU_IP):
ssh -i ~/Downloads/ssh-key-*.key ubuntu@SEU_IP_PUBLICO

# Se der erro de permissões:
chmod 600 ~/Downloads/ssh-key-*.key
```

---

## ✅ FASE 2: SETUP DO SERVIDOR (20 minutos)

### Passo 2.1: Instalação Básica
```bash
# Executar TODOS estes comandos em sequência:
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3.11 python3.11-venv python3.11-pip \
                    git nginx firewalld htop curl wget unzip
```

### Passo 2.2: Configurar Firewall Interno
```bash
# Configurar firewall da instância:
sudo systemctl start firewalld
sudo systemctl enable firewalld

sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent  
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --reload

# Verificar status:
sudo firewall-cmd --list-ports
```

### Passo 2.3: Configurar Git e GitHub
```bash
# Configurar Git:
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@gmail.com"

# Gerar chave SSH para GitHub:
ssh-keygen -t ed25519 -C "seu.email@gmail.com"

# Mostrar chave pública (copiar e adicionar no GitHub):
cat ~/.ssh/id_ed25519.pub
```

---

## ✅ FASE 3: ESTRUTURA DO PROJETO (15 minutos)

### Passo 3.1: Clonar ou Criar Repositório
```bash
# OPÇÃO A: Se já tem repositório VitrineSCV
git clone git@github.com:seu-usuario/vitrinescv.git
cd vitrinescv

# OPÇÃO B: Criar novo projeto
mkdir vitrinescv && cd vitrinescv
git init
git remote add origin git@github.com:seu-usuario/vitrinescv.git
```

### Passo 3.2: Estrutura de Diretórios
```bash
# Criar estrutura completa:
mkdir -p {app,static/{css,js,images},templates,tests,.github/workflows}

# Criar arquivo principal:
touch app/main.py requirements.txt .gitignore README.md
```

### Passo 3.3: Requirements.txt Básico
```bash
# Criar requirements.txt:
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
pandas==2.1.3
plotly==5.17.0
pillow==10.1.0
openpyxl==3.1.2
python-dotenv==1.0.0
aiofiles==23.2.1
EOF
```

---

## ✅ FASE 4: APLICAÇÃO BÁSICA FUNCIONANDO (25 minutos)

### Passo 4.1: Ambiente Virtual Python
```bash
# Criar e ativar ambiente virtual:
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências:
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4.2: FastAPI Básica Responsiva
```bash
# Criar app/main.py:
cat > app/main.py << 'EOF'
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="VitrineSCV", version="1.0.0")

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal responsivo"""
    user_agent = request.headers.get("user-agent", "").lower()
    
    # Detectar dispositivo móvel
    is_mobile = any(device in user_agent for device in 
                   ["mobile", "android", "iphone", "ipad"])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "is_mobile": is_mobile,
        "title": "VitrineSCV Dashboard"
    })

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "framework": "FastAPI", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### Passo 4.3: Template HTML Responsivo
```bash
# Criar templates/dashboard.html:
cat > templates/dashboard.html << 'EOF'
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- PWA Meta Tags -->
    <meta name="theme-color" content="#0d6efd">
    <meta name="apple-mobile-web-app-capable" content="yes">
    
    <style>
        /* Touch-friendly buttons */
        .btn { min-height: 44px; min-width: 44px; }
        
        /* Mobile adjustments */
        @media (max-width: 768px) {
            .container-fluid { padding: 10px; }
            body { font-size: 16px; }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                📊 VitrineSCV
            </a>
            
            {% if is_mobile %}
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            {% endif %}
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="/">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/api/health">Status</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container-fluid py-4">
        <div class="row">
            <div class="col-12">
                <div class="alert alert-success">
                    <h4>🎉 VitrineSCV Funcionando!</h4>
                    <p class="mb-0">
                        {% if is_mobile %}
                        <strong>📱 Dispositivo Móvel Detectado</strong> - Interface otimizada para touch
                        {% else %}
                        <strong>💻 Desktop/Tablet</strong> - Interface completa disponível
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
        
        <div class="row g-3">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">📈 Vendas</h5>
                        <p class="card-text">Módulo em desenvolvimento</p>
                        <button class="btn btn-primary">Acessar</button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">👥 Clientes</h5>
                        <p class="card-text">Módulo em desenvolvimento</p>
                        <button class="btn btn-primary">Acessar</button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">📦 Produtos</h5>
                        <p class="card-text">Módulo em desenvolvimento</p>
                        <button class="btn btn-primary">Acessar</button>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
EOF
```

---

## ✅ FASE 5: TESTAR A APLICAÇÃO (10 minutos)

### Passo 5.1: Executar Aplicação
```bash
# Ativar ambiente virtual (se não estiver ativo):
source venv/bin/activate

# Executar FastAPI:
cd vitrinescv
python app/main.py

# Deve aparecer:
# INFO: Uvicorn running on http://0.0.0.0:8000
```

### Passo 5.2: Testar Acesso
```bash
# Em outro terminal (ou pelo navegador):
curl http://localhost:8000/api/health

# Resposta esperada:
# {"status":"healthy","framework":"FastAPI","version":"1.0.0"}
```

### Passo 5.3: Testar via Navegador
```bash
# Acessar no navegador:
http://SEU_IP_PUBLICO:8000

# Deve mostrar o dashboard responsivo funcionando
```

---

## ✅ FASE 6: CONFIGURAR NGINX (15 minutos)

### Passo 6.1: Configurar Nginx como Proxy
```bash
# Criar configuração Nginx:
sudo tee /etc/nginx/sites-available/vitrinescv << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files
    location /static/ {
        alias /home/ubuntu/vitrinescv/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Ativar configuração:
sudo ln -sf /etc/nginx/sites-available/vitrinescv /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar e reiniciar Nginx:
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### Passo 6.2: Testar Nginx
```bash
# Testar acesso via porta 80:
curl -I http://SEU_IP_PUBLICO

# Acessar no navegador (sem porta):
http://SEU_IP_PUBLICO
```

---

## ✅ FASE 7: EXECUTAR EM MODO PRODUÇÃO (10 minutos)

### Passo 7.1: Configurar Systemd Service
```bash
# Criar serviço systemd:
sudo tee /etc/systemd/system/vitrinescv.service << 'EOF'
[Unit]
Description=VitrineSCV FastAPI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/vitrinescv
Environment=PATH=/home/ubuntu/vitrinescv/venv/bin
ExecStart=/home/ubuntu/vitrinescv/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Ativar e iniciar serviço:
sudo systemctl daemon-reload
sudo systemctl enable vitrinescv
sudo systemctl start vitrinescv

# Verificar status:
sudo systemctl status vitrinescv
```

### Passo 7.2: Verificação Final
```bash
# Verificar se tudo está funcionando:
curl http://SEU_IP_PUBLICO/api/health

# Verificar logs:
sudo journalctl -u vitrinescv -f
```

---

## 🎯 RESULTADO ESPERADO

Após completar todos os passos, você terá:

✅ **VitrineSCV rodando** em http://SEU_IP_PUBLICO  
✅ **Interface responsiva** funcionando em mobile/tablet/desktop  
✅ **FastAPI performático** com 12GB RAM disponível  
✅ **Nginx configurado** como proxy reverso  
✅ **Serviço automático** que reinicia em caso de falha  
✅ **Base sólida** para implementar funcionalidades específicas  

---

## 🚨 TROUBLESHOOTING RÁPIDO

### Problema: Não consegue conectar via SSH
```bash
# Verificar IP correto:
# Console Oracle Cloud > Compute > Instances > [Sua instância] > Public IP

# Verificar Security Lists:
# Console Oracle Cloud > Networking > VCN > Security Lists > Ingress Rules
# Deve ter: 0.0.0.0/0 port 22
```

### Problema: FastAPI não inicia
```bash
# Verificar ambiente virtual:
source venv/bin/activate
which python
which pip

# Reinstalar dependências:
pip install --force-reinstall -r requirements.txt
```

### Problema: Nginx erro 502
```bash
# Verificar se FastAPI está rodando:
curl http://localhost:8000/api/health

# Verificar logs:
sudo journalctl -u vitrinescv -f
sudo tail -f /var/log/nginx/error.log
```

---

## 📋 CHECKLIST FINAL

- [ ] Oracle Cloud instância criada (2 OCPUs + 12GB RAM)
- [ ] Security Lists configuradas (portas 22, 80, 443, 8000)
- [ ] SSH funcionando
- [ ] Python 3.11 + venv instalado
- [ ] FastAPI respondendo na porta 8000
- [ ] Nginx proxy configurado na porta 80  
- [ ] Systemd service criado e ativo
- [ ] Interface responsiva testada em mobile
- [ ] Health check funcionando: `/api/health`

**🎉 Parabéns! Seu VitrineSCV está funcionando na Oracle Cloud!**

**Próximo passo:** Implementar funcionalidades específicas (upload Excel, gerar PDF, etc.)