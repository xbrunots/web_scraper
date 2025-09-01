"""
Utilitários e helpers para o Web Scraper
"""

import re
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Optional
import json
from datetime import datetime

def is_valid_url(url: str) -> bool:
    """Verifica se uma URL é válida"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def normalize_url(url: str) -> str:
    """Normaliza uma URL adicionando protocolo se necessário"""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def clean_text(text: str) -> str:
    """Limpa e normaliza texto extraído"""
    if not text:
        return ""
    
    # Remove espaços extras e quebras de linha
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def extract_domain(url: str) -> str:
    """Extrai o domínio de uma URL"""
    try:
        return urlparse(url).netloc
    except:
        return ""

def sanitize_filename(filename: str) -> str:
    """Remove caracteres inválidos para nomes de arquivo"""
    # Remove caracteres problemáticos
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove espaços duplos
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

def get_timestamp() -> str:
    """Retorna timestamp formatado"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_tags(tags: List[str]) -> List[str]:
    """Valida e filtra tags HTML"""
    valid_tags = []
    html_tags = {
        'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio',
        'b', 'base', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button',
        'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
        'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt',
        'em', 'embed',
        'fieldset', 'figcaption', 'figure', 'footer', 'form',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html',
        'i', 'iframe', 'img', 'input', 'ins',
        'kbd',
        'label', 'legend', 'li', 'link',
        'main', 'map', 'mark', 'meta', 'meter',
        'nav', 'noscript',
        'object', 'ol', 'optgroup', 'option', 'output',
        'p', 'param', 'picture', 'pre', 'progress',
        'q',
        'rb', 'rp', 'rt', 'rtc', 'ruby',
        's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup',
        'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
        'u', 'ul',
        'var', 'video',
        'wbr'
    }
    
    for tag in tags:
        if tag.lower() in html_tags:
            valid_tags.append(tag.lower())
    
    return valid_tags if valid_tags else ['div', 'p', 'h1', 'h2', 'h3']

def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo para leitura humana"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def create_summary(elements: List) -> Dict:
    """Cria resumo estatístico dos elementos"""
    if not elements:
        return {}
    
    tag_count = {}
    text_lengths = []
    attr_count = 0
    
    for element in elements:
        # Contar tags
        tag = getattr(element, 'tag', 'unknown')
        tag_count[tag] = tag_count.get(tag, 0) + 1
        
        # Comprimento do texto
        text = getattr(element, 'text', '')
        if text:
            text_lengths.append(len(text))
        
        # Contar atributos
        attrs = getattr(element, 'attributes', {})
        if attrs:
            attr_count += len(attrs)
    
    avg_text_length = sum(text_lengths) / len(text_lengths) if text_lengths else 0
    
    return {
        'total_elements': len(elements),
        'unique_tags': len(tag_count),
        'tag_distribution': tag_count,
        'average_text_length': round(avg_text_length, 2),
        'total_attributes': attr_count,
        'elements_with_text': len(text_lengths)
    }

def export_to_csv(elements: List, filename: str) -> str:
    """Exporta elementos para CSV"""
    import csv
    
    if not elements:
        return ""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['tag', 'text', 'parent_tag', 'children_count', 'attributes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for element in elements:
            writer.writerow({
                'tag': getattr(element, 'tag', ''),
                'text': getattr(element, 'text', '').replace('\n', ' ').replace('\r', ''),
                'parent_tag': getattr(element, 'parent_tag', ''),
                'children_count': getattr(element, 'children_count', 0),
                'attributes': json.dumps(getattr(element, 'attributes', {}))
            })
    
    return filename

def filter_by_text_length(elements: List, min_length: int = 0, max_length: int = None) -> List:
    """Filtra elementos por comprimento do texto"""
    filtered = []
    
    for element in elements:
        text = getattr(element, 'text', '')
        text_length = len(text)
        
        if text_length >= min_length:
            if max_length is None or text_length <= max_length:
                filtered.append(element)
    
    return filtered

def get_unique_domains(results: List) -> List[str]:
    """Extrai domínios únicos dos resultados"""
    domains = set()
    
    for result in results:
        url = getattr(result, 'url', '')
        if url:
            domain = extract_domain(url)
            if domain:
                domains.add(domain)
    
    return sorted(list(domains))

class ScrapingLogger:
    """Logger especializado para operações de scraping"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file or f"scraping_{get_timestamp()}.log"
        self.logs = []
    
    def log(self, level: str, message: str, url: str = None):
        """Adiciona uma entrada de log"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message,
            'url': url
        }
        
        self.logs.append(log_entry)
        
        # Escrever no arquivo se especificado
        if self.log_file:
            self._write_to_file(log_entry)
    
    def _write_to_file(self, entry: Dict):
        """Escreve entrada no arquivo de log"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                log_line = f"[{entry['timestamp']}] {entry['level']}: {entry['message']}"
                if entry['url']:
                    log_line += f" | URL: {entry['url']}"
                f.write(log_line + '\n')
        except Exception:
            pass  # Ignorar erros de log
    
    def info(self, message: str, url: str = None):
        """Log de informação"""
        self.log('INFO', message, url)
    
    def error(self, message: str, url: str = None):
        """Log de erro"""
        self.log('ERROR', message, url)
    
    def warning(self, message: str, url: str = None):
        """Log de aviso"""
        self.log('WARNING', message, url)
    
    def get_logs(self) -> List[Dict]:
        """Retorna todos os logs"""
        return self.logs
    
    def export_logs(self, filename: str = None) -> str:
        """Exporta logs para arquivo JSON"""
        filename = filename or f"logs_{get_timestamp()}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
        
        return filename
