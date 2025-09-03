@echo off
echo 🚀 Testando Web Scraper API localmente (sem Docker)

echo ✅ Verificando arquivos necessarios...
if not exist "main.py" (
    echo ❌ main.py nao encontrado!
    pause
    exit /b 1
)

if not exist "api.py" (
    echo ❌ api.py nao encontrado!
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt nao encontrado!
    pause
    exit /b 1
)

echo ✅ Todos os arquivos encontrados!

echo.
echo 🧪 Iniciando teste da API...
echo 📍 URL: http://127.0.0.1:8000
echo 📖 Docs: http://127.0.0.1:8000/docs
echo.
echo ⚠️  Pressione Ctrl+C para parar
echo.

python main.py