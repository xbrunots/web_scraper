from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class ScraperStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"

@dataclass
class ScrapedElement:
    """Representa um elemento extraído do scraping"""
    tag: str
    text: str
    attributes: Dict[str, str]
    children_count: int
    parent_tag: Optional[str] = None

@dataclass
class ScraperResult:
    """Resultado do scraping de uma página"""
    url: str
    title: str
    status: ScraperStatus
    timestamp: str
    elements: List[ScrapedElement]
    total_elements: int
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

@dataclass
class ScraperConfig:
    """Configuração para o scraper"""
    target_tags: List[str]
    max_depth: int = 5
    include_attributes: bool = True
    include_text_only: bool = False
    min_text_length: int = 1
    headers: Optional[Dict[str, str]] = None
