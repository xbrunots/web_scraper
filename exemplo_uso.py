#!/usr/bin/env python3
"""
Exemplo Simples: Como Usar a API de Scraping
===========================================

Este script demonstra como usar a API para fazer scraping
sem gerar arquivos, apenas retornando dados.
"""

import requests
import json

def exemplo_api_simples():
    """Exemplo básico de uso da API"""
    
    api_url = "http://127.0.0.1:8000"
    
    print("🚀 Exemplo de Uso da API de Scraping")
    print("=" * 40)
    
    # 1. Fazer scraping
    print("1️⃣ Fazendo scraping...")
    scrape_data = {
        "url": "https://www.letras.mus.br/gabriel-guedes/santo-pra-sempre/",
        "target_tags": ["h1", "p", "div"],
        "min_text_length": 10,
        "include_attributes": True
    }
    
    response = requests.post(f"{api_url}/scrape", json=scrape_data)
    
    if response.status_code == 200:
        result = response.json()
        result_id = result['result_id']
        
        print(f"✅ Scraping realizado!")
        print(f"   ID: {result_id}")
        print(f"   Título: {result['title']}")
        print(f"   Elementos: {result['total_elements']}")
        
        # 2. Filtrar por termo
        print("\n2️⃣ Filtrando por 'santo'...")
        filter_response = requests.get(f"{api_url}/results/{result_id}/filter?search_term=santo")
        
        if filter_response.status_code == 200:
            filter_result = filter_response.json()
            print(f"✅ Encontrados {filter_result['filtered_total']} elementos com 'santo'")
            
            # Mostrar alguns resultados
            for i, elem in enumerate(filter_result['elements'][:3]):
                print(f"   {i+1}. [{elem['tag']}] {elem['text'][:60]}...")
        
        # 3. Obter dados completos em JSON
        print("\n3️⃣ Obtendo dados estruturados...")
        json_response = requests.get(f"{api_url}/results/{result_id}/json")
        
        if json_response.status_code == 200:
            json_result = json_response.json()
            print(f"✅ Dados completos obtidos!")
            print(f"   Total de elementos: {len(json_result['data']['elements'])}")
            
            # Salvar localmente se necessário (opcional)
            with open(f"dados_{result_id}.json", "w", encoding="utf-8") as f:
                json.dump(json_result['data'], f, ensure_ascii=False, indent=2)
            print(f"   💾 Dados salvos em dados_{result_id}.json")
        
        # 4. Estatísticas
        print("\n4️⃣ Estatísticas gerais...")
        stats_response = requests.get(f"{api_url}/stats")
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            if "total_results" in stats:
                print(f"✅ Total de resultados: {stats['total_results']}")
                print(f"   Elementos coletados: {stats['total_elements_scraped']}")
            else:
                print(f"ℹ️  {stats.get('message', 'Sem estatísticas')}")
            
        print(f"\n🎉 Exemplo concluído! Todos os dados foram retornados pela API.")
        
    else:
        print(f"❌ Erro no scraping: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        exemplo_api_simples()
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando!")
        print("   Inicie com: python main.py")
        print("   Então acesse: http://127.0.0.1:8000/docs")
