# Web Scraper API

Sistema de web scraping com API REST simples e eficiente. **Retorna dados diretamente** - sem armazenamento ou IDs, todos os dados são entregues imediatamente na resposta.

## 🚀 Instalação e Uso

```bash
# 1. Instalar dependências
pip install fastapi beautifulsoup4 requests uvicorn

# 2. Iniciar API
python main.py

# 3. Acessar
# API: http://127.0.0.1:8000
# Documentação: http://127.0.0.1:8000/docs
```

## 📡 Endpoints Disponíveis

### 1. Scraping Simples

```bash
POST /scrape
{
  "url": "https://letras.mus.br/legiao-urbana/46967/",
  "target_tags": ["h1", "p", "div"],
  "include_attributes": true,
  "min_text_length": 5,
  "max_depth": 3
}
```

### 2. Scraping Múltiplo

```bash
POST /scrape/multiple
{
  "urls": [
    "https://letras.mus.br/legiao-urbana/46967/",
    "https://letras.mus.br/legiao-urbana/46968/"
  ],
  "target_tags": ["h1", "p"],
  "delay": 1.0
}
```

### 3. Scraping com Filtros

```bash
POST /scrape/filter?tag=h1&search_term=Perfeição
{
  "url": "https://letras.mus.br/legiao-urbana/46967/",
  "target_tags": ["h1", "h2", "p"],
  "include_attributes": true
}
```

## 📋 Exemplo de Resposta

```json
{
  "status": "success",
  "url": "https://letras.mus.br/legiao-urbana/46967/",
  "title": "Perfeição - Legião Urbana - LETRAS.MUS.BR",
  "total_elements": 167,
  "timestamp": "2025-09-01T13:24:15.952034",
  "metadata": {
    "response_status": 200,
    "content_type": "text/html; charset=utf-8",
    "page_size": 138321
  },
  "elements": [
    {
      "tag": "h1",
      "text": "Perfeição",
      "attributes": {"class": "song-title"},
      "parent_tag": "div",
      "children_count": 0
    },
    {
      "tag": "p",
      "text": "Vamos celebrar a estupidez humana...",
      "attributes": {},
      "parent_tag": "div",
      "children_count": 0
    }
  ]
}

## 💡 Exemplo Prático - PowerShell

```powershell
# Fazer scraping direto
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/scrape" -Method Post -ContentType "application/json" -Body '{"url": "https://letras.mus.br/legiao-urbana/46967/", "target_tags": ["h1", "p", "div"], "min_text_length": 10}'

# Dados já estão na resposta!
Write-Host "Status: $($response.status)"
Write-Host "URL: $($response.url)" 
Write-Host "Elementos encontrados: $($response.total_elements)"
Write-Host "Título: $($response.title)"

# Filtrar elementos por tag específica
$h1_elements = $response.elements | Where-Object { $_.tag -eq "h1" }
Write-Host "Elementos H1 encontrados: $($h1_elements.Count)"

# Salvar resultado completo
$response | ConvertTo-Json -Depth 10 | Out-File "scraping_resultado.json" -Encoding UTF8

# Exemplo com filtros na API
$filtered_response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/scrape/filter?tag=p&search_term=Perfeição" -Method Post -ContentType "application/json" -Body '{"url": "https://letras.mus.br/legiao-urbana/46967/", "target_tags": ["h1", "p"]}'

Write-Host "Elementos filtrados: $($filtered_response.filtered_total)"
```

## 🔧 Estrutura do Projeto

```txt
scraper/
├── main.py        # Entrada principal - inicia apenas a API
├── api.py         # API REST simplificada (retorno direto)
├── scraper.py     # Lógica de scraping com BeautifulSoup
├── models.py      # Modelos de dados (ScraperResult, etc)
└── utils.py       # Funções utilitárias
```

## ⚡ Recursos

- ✅ **API REST simplificada**
- ✅ **Retorno direto (sem IDs ou armazenamento)**
- ✅ Scraping de uma ou múltiplas URLs
- ✅ Filtros por tag, texto e atributos
- ✅ Dados estruturados em JSON
- ✅ Configuração flexível (tags, profundidade, etc)
- ✅ Tratamento de erros robusto
- ✅ Documentação automática (FastAPI)
- ✅ Metadados detalhados (status HTTP, tamanho, etc)

## 🎯 Casos de Uso Testados

- 🎵 **Sites de letras** (letras.mus.br - totalmente funcional)
- 📰 Sites de notícias e blogs
- 🛒 E-commerce (extração de produtos e preços)
- � Qualquer site para extração de dados estruturados
- 🔍 Análise de conteúdo web automatizada

## 🚀 Próximos Passos

1. **Teste a API**: `python main.py`
2. **Acesse a documentação**: <http://127.0.0.1:8000/docs>
3. **Faça sua primeira requisição** com o endpoint `/scrape`
4. **Os dados chegam imediatamente** - sem necessidade de consultas adicionais!

## 🌐 Deploy no EasyPanel

Este projeto está pronto para deploy no EasyPanel! Todos os arquivos de configuração estão incluídos:

- ✅ `Dockerfile` - Container otimizado para produção
- ✅ `docker-compose.yml` - Para teste local
- ✅ `easypanel.yml` - Configuração específica do EasyPanel
- ✅ `.dockerignore` - Arquivos ignorados no build
- ✅ `DEPLOY_EASYPANEL.md` - **Guia completo de deploy**

### Deploy Rápido:

```bash
# 1. Push para seu repositório
git add . && git commit -m "Ready for EasyPanel" && git push

# 2. No EasyPanel:
# - New Project → Import from Git
# - Selecione o repositório
# - Configure porta 8000
# - Deploy automático!
```

**🔗 Após deploy**: `https://your-app.easypanel.host/docs`

---

**📚 Leia o guia completo**: [`DEPLOY_EASYPANEL.md`](./DEPLOY_EASYPANEL.md)
