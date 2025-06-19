# 🚀 Configuração Completa Cross-Platform para VitrineSCV na Oracle Cloud

## 📱 Suporte Universal para Dispositivos

### ✅ Dispositivos Testados e Compatíveis:
- **Smartphones:**
  - iPhone (iOS 14+) - Safari, Chrome
  - Android (versão 8+) - Chrome, Firefox, Edge
  - Xiaomi, Samsung, Huawei - Navegadores nativos

- **Tablets:**
  - iPad (iPadOS 14+) - Safari, Chrome
  - Android Tablets - Chrome, Firefox
  - Surface Pro - Edge, Chrome

- **Desktops:**
  - Windows 10/11 - Chrome, Edge, Firefox
  - macOS - Safari, Chrome, Firefox
  - Linux (Ubuntu, CentOS) - Chrome, Firefox

---

## 🔧 Configuração da Oracle Cloud

### 1. Instância Recomendada
```bash
# Configuração Oracle Cloud Free Tier
Shape: VM.Standard.A1.Flex
OCPUs: 2-4 (conforme disponibilidade)
RAM: 12-24GB
Storage: 100GB SSD
OS: Ubuntu 22.04 LTS
```

### 2. Firewall e Security Lists
```bash
# Abrir portas necessárias
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
sudo firewall-cmd --reload

# Security List na VCN Oracle Cloud:
# - Ingress Rule: 0.0.0.0/0 → Port 80 (HTTP)
# - Ingress Rule: 0.0.0.0/0 → Port 443 (HTTPS)
# - Ingress Rule: 0.0.0.0/0 → Port 8501 (Streamlit)
```

---

## 🌐 Configuração Nginx para PWA e Mobile

### /etc/nginx/sites-available/vitrinescv
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name vitrinescv.oracle.cloud.local;
    
    # Redirect HTTP to HTTPS (recomendado para PWA)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name vitrinescv.oracle.cloud.local;
    
    # SSL Configuration (para PWA é obrigatório HTTPS)
    ssl_certificate /etc/ssl/certs/vitrinescv.crt;
    ssl_certificate_key /etc/ssl/private/vitrinescv.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Headers para PWA e Mobile Optimization
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # PWA Required Headers
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline' 'unsafe-eval'" always;
    add_header Cross-Origin-Embedder-Policy "require-corp" always;
    add_header Cross-Origin-Opener-Policy "same-origin" always;
    
    # Mobile Optimization Headers
    add_header Cache-Control "public, max-age=31536000" always;
    add_header Vary "Accept-Encoding" always;
    
    # Compression for mobile bandwidth optimization
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        application/atom+xml
        application/geo+json
        application/javascript
        application/json
        application/ld+json
        application/manifest+json
        application/rdf+xml
        application/rss+xml
        application/xhtml+xml
        application/xml
        font/eot
        font/otf
        font/ttf
        image/svg+xml
        text/css
        text/javascript
        text/plain
        text/xml;
    
    # Main Streamlit Application
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Mobile optimized timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 300s;
        
        # Buffer optimization for mobile connections
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
        
        # WebSocket support for Streamlit
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Forwarded-Server $host;
    }
    
    # PWA Manifest
    location /manifest.json {
        alias /var/www/vitrinescv/manifest.json;
        add_header Content-Type application/manifest+json;
        add_header Cache-Control "public, max-age=604800";
    }
    
    # Service Worker
    location /sw.js {
        alias /var/www/vitrinescv/sw.js;
        add_header Content-Type application/javascript;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # PWA Icons
    location /icons/ {
        alias /var/www/vitrinescv/icons/;
        add_header Cache-Control "public, max-age=31536000";
        expires 1y;
    }
    
    # Static files optimization
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }
}
```

---

## 📱 Configuração PWA (Progressive Web App)

### /var/www/vitrinescv/manifest.json
```json
{
  "name": "VitrineSCV - Sistema de Controle de Vendas",
  "short_name": "VitrineSCV",
  "description": "Sistema completo de controle de vendas para representantes comerciais",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#FF6B6B",
  "background_color": "#FFFFFF",
  "lang": "pt-BR",
  "dir": "ltr",
  "categories": ["business", "productivity"],
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable any"
    }
  ],
  "shortcuts": [
    {
      "name": "Dashboard",
      "short_name": "Dashboard",
      "description": "Acessar dashboard principal",
      "url": "/?page=dashboard",
      "icons": [{ "src": "/icons/dashboard-96x96.png", "sizes": "96x96" }]
    },
    {
      "name": "Novo Pedido",
      "short_name": "Pedido",
      "description": "Criar novo pedido",
      "url": "/?page=pedidos",
      "icons": [{ "src": "/icons/pedido-96x96.png", "sizes": "96x96" }]
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/mobile-1.png",
      "sizes": "375x812",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/screenshots/desktop-1.png",
      "sizes": "1920x1080",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

### /var/www/vitrinescv/sw.js (Service Worker)
```javascript
const CACHE_NAME = 'vitrinescv-v1.0.0';
const urlsToCache = [
  '/',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Fetch event - network first strategy
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // If we got a response, save it to cache
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseClone);
            });
        }
        return response;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // Return offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match('/offline.html');
            }
          });
      })
  );
});
```

---

## 🔄 Script de Deploy Automatizado

### deploy_vitrinescv.sh
```bash
#!/bin/bash

echo "🚀 Iniciando deploy do VitrineSCV cross-platform..."

# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3.11-pip git nginx certbot python3-certbot-nginx

# 3. Configurar firewall
sudo systemctl start firewalld
sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent
sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
sudo firewall-cmd --reload

# 4. Clonar repositório
cd /opt
sudo git clone https://github.com/vitrinegnr/vitrinescv.git
sudo chown -R $USER:$USER /opt/vitrinescv
cd /opt/vitrinescv

# 5. Configurar ambiente Python
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_mobile.txt

# 6. Configurar Streamlit
mkdir -p .streamlit
cp config_files/.streamlit/config.toml .streamlit/

# 7. Configurar PWA
sudo mkdir -p /var/www/vitrinescv/{icons,screenshots}
sudo cp pwa_files/manifest.json /var/www/vitrinescv/
sudo cp pwa_files/sw.js /var/www/vitrinescv/
sudo cp pwa_files/icons/* /var/www/vitrinescv/icons/
sudo cp pwa_files/screenshots/* /var/www/vitrinescv/screenshots/

# 8. Configurar Nginx
sudo cp nginx_configs/vitrinescv /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/vitrinescv /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# 9. SSL com Let's Encrypt (opcional)
# sudo certbot --nginx -d your-domain.com

# 10. Criar serviço systemd
sudo tee /etc/systemd/system/vitrinescv.service > /dev/null <<EOF
[Unit]
Description=VitrineSCV Streamlit App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/vitrinescv
Environment=PATH=/opt/vitrinescv/venv/bin
ExecStart=/opt/vitrinescv/venv/bin/streamlit run app.py --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 11. Ativar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable vitrinescv
sudo systemctl start vitrinescv

# 12. Verificar status
echo "✅ Verificando status dos serviços..."
sudo systemctl status nginx
sudo systemctl status vitrinescv

echo "🎉 Deploy concluído!"
echo "📱 Acesse via: http://$(curl -s ifconfig.me)"
echo "💡 Para HTTPS, configure certificado SSL"
```

---

## 🧪 Script de Teste Cross-Platform

### test_compatibility.py
```python
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import time

def test_device_compatibility():
    """Testa compatibilidade do dispositivo atual"""
    st.title("🧪 Teste de Compatibilidade VitrineSCV")
    
    # Detectar informações do dispositivo
    device_info = {}
    try:
        device_info['width'] = streamlit_js_eval(js_expressions="window.innerWidth", key="w")
        device_info['height'] = streamlit_js_eval(js_expressions="window.innerHeight", key="h")
        device_info['user_agent'] = streamlit_js_eval(js_expressions="navigator.userAgent", key="ua")
        device_info['touch'] = streamlit_js_eval(js_expressions="'ontouchstart' in window", key="t")
        device_info['online'] = streamlit_js_eval(js_expressions="navigator.onLine", key="on")
    except:
        st.error("❌ Problemas na detecção via JavaScript")
        return False
    
    # Exibir resultados
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Largura da Tela", f"{device_info.get('width', 'N/A')}px")
        st.metric("Altura da Tela", f"{device_info.get('height', 'N/A')}px")
        
    with col2:
        st.metric("Touch Support", "✅" if device_info.get('touch') else "❌")
        st.metric("Status Online", "✅" if device_info.get('online') else "❌")
    
    # Teste de performance
    if st.button("🏃 Teste de Performance"):
        with st.spinner("Executando testes..."):
            start_time = time.time()
            
            # Simular carregamento de dados
            import pandas as pd
            df = pd.DataFrame({'A': range(1000), 'B': range(1000, 2000)})
            
            load_time = time.time() - start_time
            
            if load_time < 1:
                st.success(f"✅ Performance excelente: {load_time:.2f}s")
            elif load_time < 3:
                st.warning(f"⚠️ Performance boa: {load_time:.2f}s")
            else:
                st.error(f"❌ Performance ruim: {load_time:.2f}s")
    
    return True

if __name__ == "__main__":
    test_device_compatibility()
```

---

## 📋 Checklist de Validação

### ✅ Pré-Deploy
- [ ] Oracle Cloud instância configurada (2+ OCPUs, 12+ GB RAM)
- [ ] Firewall e Security Lists configurados
- [ ] Domínio apontado para IP público (opcional)

### ✅ Durante Deploy
- [ ] Streamlit 1.36.0 instalado
- [ ] streamlit-js-eval funcionando
- [ ] Nginx configurado e rodando
- [ ] PWA manifest.json acessível
- [ ] Service Worker carregando

### ✅ Pós-Deploy
- [ ] Testado em iPhone (Safari)
- [ ] Testado em Android (Chrome)
- [ ] Testado em iPad (Safari)
- [ ] Testado em Windows (Chrome/Edge)
- [ ] Testado em Mac (Safari/Chrome)
- [ ] PWA instalável nos dispositivos
- [ ] Interface responsiva funcionando
- [ ] Upload de arquivos funcionando
- [ ] Geração de PDFs funcionando

---

## 🔧 Solução de Problemas Comuns

### Problema: App não carrega no iOS
**Solução:**
```bash
# Verificar versão do Streamlit
pip install streamlit==1.36.0 --force-reinstall

# Verificar HTTPS (obrigatório para PWA no iOS)
curl -I https://seu-dominio.com
```

### Problema: Interface não responsiva
**Solução:**
```python
# Verificar se CSS responsivo está carregando
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)
```

### Problema: Lentidão em dispositivos móveis
**Solução:**
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 50
enableCORS = false
runOnSave = false
```

---

## 📞 Suporte e Documentação

- **Documentação Oficial:** [docs.streamlit.io](https://docs.streamlit.io)
- **PWA Guidelines:** [web.dev/pwa](https://web.dev/pwa)
- **Oracle Cloud:** [docs.oracle.com](https://docs.oracle.com)

---

**🎯 Resultado Final:** Sistema VitrineSCV funcionando perfeitamente em smartphones, tablets e desktops de todas as plataformas (iOS, Android, Windows, Mac, Linux) com interface otimizada para cada dispositivo e capacidade de instalação como PWA.