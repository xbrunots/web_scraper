#!/usr/bin/env python3
"""
Web Scraper API
Aplicação de scraping com API REST usando FastAPI

Uso:
    python main.py  - Inicia o servidor API

Acesso:
    http://127.0.0.1:8000 - API
    http://127.0.0.1:8000/docs - Documentação
"""

import uvicorn
from api import app

def run_api_server(host: str = "127.0.0.1", port: int = 8000):
    """Inicia o servidor da API"""
    print(f"🚀 Iniciando Web Scraper API em http://{host}:{port}")
    print("📖 Documentação disponível em: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

def main():
    """Função principal - inicia apenas a API"""
    run_api_server()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()