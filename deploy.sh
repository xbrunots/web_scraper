#!/bin/bash

# Script de deploy para EasyPanel
# Execute este script na raiz do projeto

echo "🚀 Preparando deploy para EasyPanel..."

# 1. Verificar se os arquivos necessários existem
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile não encontrado!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado!"
    exit 1
fi

echo "✅ Arquivos de configuração encontrados"

# 2. Construir imagem Docker localmente para testar
echo "🔨 Construindo imagem Docker para teste..."
docker build -t web-scraper-api .

if [ $? -eq 0 ]; then
    echo "✅ Build do Docker bem-sucedido"
else
    echo "❌ Falha no build do Docker"
    exit 1
fi

# 3. Testar container localmente
echo "🧪 Testando container localmente..."
docker run -d --name web-scraper-test -p 8001:8000 web-scraper-api

sleep 10

# Verificar se a API está respondendo
if curl -s http://localhost:8001/ > /dev/null; then
    echo "✅ Container funcionando corretamente"
    docker stop web-scraper-test
    docker rm web-scraper-test
else
    echo "❌ Container não está respondendo"
    docker stop web-scraper-test
    docker rm web-scraper-test
    exit 1
fi

echo ""
echo "🎉 Projeto pronto para deploy no EasyPanel!"
echo ""
echo "📋 Próximos passos:"
echo "1. Faça push do código para seu repositório Git"
echo "2. No EasyPanel, crie um novo projeto"
echo "3. Conecte seu repositório Git"
echo "4. Configure a porta 8000"
echo "5. Deploy automático será iniciado"
echo ""
echo "🔗 Configurações importantes:"
echo "• Porta do container: 8000"
echo "• Health check: GET /"
echo "• Recursos mínimos: 512MB RAM, 0.5 CPU"