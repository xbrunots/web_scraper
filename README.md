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
