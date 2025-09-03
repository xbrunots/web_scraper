# 🚀 Deploy no EasyPanel - Web Scraper API

Guia completo para fazer deploy da API de Web Scraping no EasyPanel.

## 📋 Pré-requisitos

- Conta no [EasyPanel](https://easypanel.io)
- Repositório Git (GitHub, GitLab, etc.)
- Projeto funcionando localmente

## 🔧 Arquivos de Configuração Incluídos

### `Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `easypanel.yml` (Configuração específica)
```yaml
name: web-scraper-api
type: app
build:
  type: dockerfile
  dockerfile: Dockerfile
runtime:
  port: 8000
resources:
  memory: 512Mi
  cpu: 500m
healthCheck:
  path: /
  port: 8000
```

## 🚀 Passos para Deploy

### 1. Preparar o Repositório

```bash
# Adicionar arquivos ao Git
git add .
git commit -m "Add EasyPanel configuration files"
git push origin main
```

### 2. Configurar no EasyPanel

1. **Login no EasyPanel**
   - Acesse seu dashboard
   - Clique em "New Project"

2. **Conectar Repositório**
   - Escolha "Import from Git"
   - Conecte seu GitHub/GitLab
   - Selecione o repositório `web-scraper`

3. **Configurações do Projeto**
   - **Nome**: `web-scraper-api`
   - **Branch**: `main` (ou `develop`)
   - **Build Command**: Automático (usa Dockerfile)
   - **Port**: `8000`

4. **Variáveis de Ambiente** (opcional)
   ```
   PYTHONPATH=/app
   PYTHONUNBUFFERED=1
   ```

5. **Recursos**
   - **Memory**: 512MB (mínimo)
   - **CPU**: 0.5 cores (mínimo)

### 3. Deploy Automático

- EasyPanel detectará o `Dockerfile`
- Build será iniciado automaticamente
- Deploy acontece após build bem-sucedido
- Health check verificará se API está funcionando

## 🔗 URLs Após Deploy

Após o deploy, você terá:

- **API Principal**: `https://your-app.easypanel.host/`
- **Documentação**: `https://your-app.easypanel.host/docs`
- **Health Check**: `https://your-app.easypanel.host/`

## 🧪 Testando o Deploy

```bash
# Teste básico da API
curl https://your-app.easypanel.host/

# Teste de scraping
curl -X POST "https://your-app.easypanel.host/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://letras.mus.br/legiao-urbana/46967/",
    "target_tags": ["h1", "p"],
    "min_text_length": 5
  }'
```

## ⚙️ Configurações Avançadas

### Auto-scaling (Opcional)
```yaml
scaling:
  minReplicas: 1
  maxReplicas: 3
  targetCPU: 70
  targetMemory: 80
```

### Custom Domain
- No dashboard, vá em "Domains"
- Adicione seu domínio personalizado
- Configure DNS CNAME apontando para EasyPanel

### SSL/HTTPS
- Automaticamente configurado pelo EasyPanel
- Let's Encrypt gratuito
- Renovação automática

## 📊 Monitoramento

EasyPanel oferece:
- **Logs em tempo real**
- **Métricas de CPU/RAM**
- **Health checks automáticos**
- **Alertas por email/webhook**

## 🐛 Troubleshooting

### Build Failures
```bash
# Verificar logs no EasyPanel dashboard
# Ou testar localmente:
docker build -t test-scraper .
docker run -p 8000:8000 test-scraper
```

### App Not Starting
- Verifique se porta 8000 está exposta
- Confirme se `uvicorn api:app` funciona localmente
- Verifique logs do container

### Health Check Failing
- Endpoint `/` deve retornar status 200
- Verifique se API está realmente rodando na porta 8000

## 💰 Custos Estimados

Para esta API simples:
- **Starter Plan**: ~$5-10/mês
- **Recursos**: 512MB RAM, 0.5 CPU
- **Inclui**: SSL, domínio, backups

## 🔄 CI/CD Automático

EasyPanel faz deploy automático quando você faz push:
```bash
git add .
git commit -m "Update scraper"
git push origin main
# Deploy automático iniciado!
```

## ✅ Checklist Final

- [ ] Dockerfile criado e testado
- [ ] requirements.txt atualizado
- [ ] Repositório Git configurado
- [ ] EasyPanel project criado
- [ ] Porta 8000 configurada
- [ ] Deploy realizado com sucesso
- [ ] API respondendo corretamente
- [ ] Documentação acessível (/docs)
- [ ] Teste de scraping funcionando

**🎉 Sua API de Web Scraping está no ar!**