import requests
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import time
import logging

from models import ScrapedElement, ScraperResult, ScraperConfig, ScraperStatus

class WebScraper:
    def __init__(self, config: ScraperConfig = None):
        self.config = config or ScraperConfig(target_tags=["div", "p", "h1", "h2", "h3", "a"])
        self.session = requests.Session()
        
        # Headers padrão para evitar bloqueios
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if self.config.headers:
            default_headers.update(self.config.headers)
        
        self.session.headers.update(default_headers)
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def scrape_url(self, url: str) -> ScraperResult:
        """Faz o scraping de uma URL específica"""
        try:
            self.logger.info(f"Iniciando scraping de: {url}")
            
            # Fazer a requisição
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair título
            title = soup.title.string.strip() if soup.title else "Sem título"
            
            # Extrair elementos baseado nas tags configuradas
            elements = self._extract_elements(soup)
            
            # Filtrar elementos se necessário
            filtered_elements = self._filter_elements(elements)
            
            # Criar metadados
            metadata = {
                "response_status": response.status_code,
                "content_type": response.headers.get('content-type', ''),
                "page_size": len(response.content),
                "tags_found": {tag: len([e for e in filtered_elements if e.tag == tag]) for tag in self.config.target_tags}
            }
            
            return ScraperResult(
                url=url,
                title=title,
                status=ScraperStatus.SUCCESS,
                timestamp=datetime.now().isoformat(),
                elements=filtered_elements,
                total_elements=len(filtered_elements),
                metadata=metadata
            )
            
        except requests.RequestException as e:
            self.logger.error(f"Erro na requisição para {url}: {e}")
            return ScraperResult(
                url=url,
                title="",
                status=ScraperStatus.ERROR,
                timestamp=datetime.now().isoformat(),
                elements=[],
                total_elements=0,
                metadata={},
                error_message=str(e)
            )
        except Exception as e:
            self.logger.error(f"Erro inesperado ao fazer scraping de {url}: {e}")
            return ScraperResult(
                url=url,
                title="",
                status=ScraperStatus.ERROR,
                timestamp=datetime.now().isoformat(),
                elements=[],
                total_elements=0,
                metadata={},
                error_message=str(e)
            )

    def _extract_elements(self, soup: BeautifulSoup) -> List[ScrapedElement]:
        """Extrai elementos do HTML baseado na configuração"""
        elements = []
        
        for tag_name in self.config.target_tags:
            found_tags = soup.find_all(tag_name)
            
            for tag in found_tags:
                if isinstance(tag, Tag):
                    # Extrair texto
                    text = tag.get_text(strip=True)
                    
                    # Pular elementos vazios se configurado
                    if len(text) < self.config.min_text_length:
                        continue
                    
                    # Extrair atributos se configurado
                    attributes = {}
                    if self.config.include_attributes:
                        attributes = dict(tag.attrs) if tag.attrs else {}
                    
                    # Informações do elemento pai
                    parent_tag = tag.parent.name if tag.parent and tag.parent.name else None
                    
                    # Contar filhos
                    children_count = len(tag.find_all()) if hasattr(tag, 'find_all') else 0
                    
                    element = ScrapedElement(
                        tag=tag_name,
                        text=text,
                        attributes=attributes,
                        children_count=children_count,
                        parent_tag=parent_tag
                    )
                    
                    elements.append(element)
        
        return elements

    def _filter_elements(self, elements: List[ScrapedElement]) -> List[ScrapedElement]:
        """Aplica filtros adicionais nos elementos"""
        filtered = []
        
        for element in elements:
            # Filtro por comprimento de texto
            if self.config.include_text_only and not element.text.strip():
                continue
            
            filtered.append(element)
        
        return filtered

    def scrape_multiple_urls(self, urls: List[str], delay: float = 1.0) -> List[ScraperResult]:
        """Faz scraping de múltiplas URLs com delay entre requisições"""
        results = []
        
        for i, url in enumerate(urls):
            result = self.scrape_url(url)
            results.append(result)
            
            # Delay entre requisições para ser respeitoso
            if i < len(urls) - 1:
                time.sleep(delay)
        
        return results

    def filter_by_tag(self, result: ScraperResult, tag: str) -> List[ScrapedElement]:
        """Filtra elementos por tag específica"""
        return [element for element in result.elements if element.tag == tag]

    def search_by_text(self, result: ScraperResult, search_term: str) -> List[ScrapedElement]:
        """Busca elementos que contenham um termo específico"""
        search_term_lower = search_term.lower()
        return [
            element for element in result.elements 
            if search_term_lower in element.text.lower()
        ]

    def get_elements_by_attribute(self, result: ScraperResult, attr_name: str, attr_value: str = None) -> List[ScrapedElement]:
        """Filtra elementos por atributos"""
        if attr_value is None:
            return [element for element in result.elements if attr_name in element.attributes]
        else:
            return [
                element for element in result.elements 
                if element.attributes.get(attr_name) == attr_value
            ]

    def to_dict(self, result: ScraperResult) -> dict:
        """Converte resultado para dicionário"""
        return {
            "url": result.url,
            "title": result.title,
            "status": result.status.value,
            "timestamp": result.timestamp,
            "total_elements": result.total_elements,
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
