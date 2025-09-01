from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

from scraper import WebScraper
from models import ScraperConfig

# Modelos Pydantic para a API
class ScrapeRequest(BaseModel):
    url: HttpUrl
    target_tags: Optional[List[str]] = ["div", "p", "h1", "h2", "h3", "a"]
    max_depth: Optional[int] = 5
    include_attributes: Optional[bool] = True
    min_text_length: Optional[int] = 1

class MultipleScrapeRequest(BaseModel):
    urls: List[HttpUrl]
    target_tags: Optional[List[str]] = ["div", "p", "h1", "h2", "h3", "a"]
    delay: Optional[float] = 1.0
    include_attributes: Optional[bool] = True

# Inicializar FastAPI
app = FastAPI(
    title="Web Scraper API",
    description="API para fazer web scraping direto - retorna dados imediatamente",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Web Scraper API - Retorno Direto",
        "version": "1.0.0",
        "description": "Faz scraping e retorna dados imediatamente",
        "endpoints": {
            "scrape": "/scrape - Faz scraping de uma URL",
            "scrape_multiple": "/scrape/multiple - Faz scraping de múltiplas URLs"
        }
    }

@app.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    """Faz scraping de uma URL e retorna todos os dados diretamente"""
    try:
        # Criar configuração do scraper
        config = ScraperConfig(
            target_tags=request.target_tags,
            max_depth=request.max_depth,
            include_attributes=request.include_attributes,
            min_text_length=request.min_text_length
        )
        
        # Inicializar scraper e fazer o scraping
        scraper = WebScraper(config)
        result = scraper.scrape_url(str(request.url))
        
        # Retornar todos os dados diretamente
        return {
            "status": result.status.value,
            "url": result.url,
            "title": result.title,
            "total_elements": result.total_elements,
            "timestamp": result.timestamp,
            "metadata": result.metadata,
            "error_message": result.error_message,
            "elements": [
                {
                    "tag": elem.tag,
                    "text": elem.text,
                    "attributes": elem.attributes,
                    "children_count": elem.children_count,
                    "parent_tag": elem.parent_tag
                }
                for elem in result.elements
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no scraping: {str(e)}")

@app.post("/scrape/multiple")
async def scrape_multiple_urls(request: MultipleScrapeRequest):
    """Faz scraping de múltiplas URLs e retorna todos os dados diretamente"""
    try:
        # Criar configuração do scraper
        config = ScraperConfig(
            target_tags=request.target_tags,
            include_attributes=request.include_attributes
        )
        
        # Inicializar scraper e fazer o scraping
        scraper = WebScraper(config)
        urls = [str(url) for url in request.urls]
        results = scraper.scrape_multiple_urls(urls, request.delay)
        
        # Retornar dados de todas as URLs
        return {
            "total_urls": len(urls),
            "successful_scrapes": len([r for r in results if r.status.value == "success"]),
            "failed_scrapes": len([r for r in results if r.status.value == "error"]),
            "total_elements": sum(r.total_elements for r in results),
            "results": [
                {
                    "status": r.status.value,
                    "url": r.url,
                    "title": r.title,
                    "total_elements": r.total_elements,
                    "timestamp": r.timestamp,
                    "metadata": r.metadata,
                    "error_message": r.error_message,
                    "elements": [
                        {
                            "tag": elem.tag,
                            "text": elem.text,
                            "attributes": elem.attributes,
                            "children_count": elem.children_count,
                            "parent_tag": elem.parent_tag
                        }
                        for elem in r.elements
                    ]
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no scraping múltiplo: {str(e)}")

# Endpoint para filtrar dados diretamente no scraping
@app.post("/scrape/filter")
async def scrape_and_filter(
    request: ScrapeRequest,
    tag: Optional[str] = Query(None, description="Filtrar por tag específica"),
    search_term: Optional[str] = Query(None, description="Buscar por termo no texto"),
    attribute_name: Optional[str] = Query(None, description="Filtrar por nome do atributo"),
    attribute_value: Optional[str] = Query(None, description="Valor do atributo")
):
    """Faz scraping e aplica filtros diretamente"""
    try:
        # Primeiro fazer o scraping normal
        config = ScraperConfig(
            target_tags=request.target_tags,
            max_depth=request.max_depth,
            include_attributes=request.include_attributes,
            min_text_length=request.min_text_length
        )
        
        scraper = WebScraper(config)
        result = scraper.scrape_url(str(request.url))
        
        if result.status.value != "success":
            raise HTTPException(status_code=500, detail=result.error_message)
        
        # Aplicar filtros
        filtered_elements = result.elements
        
        if tag:
            filtered_elements = [elem for elem in filtered_elements if elem.tag == tag]
        
        if search_term:
            search_term_lower = search_term.lower()
            filtered_elements = [elem for elem in filtered_elements 
                               if search_term_lower in elem.text.lower()]
        
        if attribute_name:
            if attribute_value:
                filtered_elements = [elem for elem in filtered_elements 
                                   if elem.attributes.get(attribute_name) == attribute_value]
            else:
                filtered_elements = [elem for elem in filtered_elements 
                                   if attribute_name in elem.attributes]
        
        # Retornar dados filtrados
        return {
            "status": result.status.value,
            "url": result.url,
            "title": result.title,
            "original_total": result.total_elements,
            "filtered_total": len(filtered_elements),
            "timestamp": result.timestamp,
            "filters_applied": {
                "tag": tag,
                "search_term": search_term,
                "attribute_name": attribute_name,
                "attribute_value": attribute_value
            },
            "metadata": result.metadata,
            "elements": [
                {
                    "tag": elem.tag,
                    "text": elem.text,
                    "attributes": elem.attributes,
                    "children_count": elem.children_count,
                    "parent_tag": elem.parent_tag
                }
                for elem in filtered_elements
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no scraping com filtros: {str(e)}")
