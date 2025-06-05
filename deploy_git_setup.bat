
@echo off
setlocal EnableDelayedExpansion

echo Verificando se o Git está instalado...
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Git não está instalado ou não está no PATH.
    echo Baixe e instale aqui: https://git-scm.com/downloads
    pause
    exit /b
)

echo.
echo ✅ Git encontrado. Inicializando repositório...

:: Cria arquivos básicos se não existirem
if not exist requirements.txt (
    echo Flask==2.2.5> requirements.txt
    echo requirements.txt criado.
)

if not exist .gitignore (
    echo __pycache__/> .gitignore
    echo visitadas.txt>> .gitignore
    echo *.pyc>> .gitignore
    echo .env>> .gitignore
    echo .gitignore criado.
)

:: Inicia o repositório Git
git init
git add .
git commit -m "Commit inicial do projeto Flask da Agência Stiff"

echo.
set /p REPO_URL="👉 Cole aqui o link do seu repositório GitHub (ex: https://github.com/seuusuario/seurepo.git): "

git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️ Falha ao enviar para o GitHub. Tentando forçar push...
    git push -f origin main
)

echo.
echo ✅ Projeto enviado com sucesso para o GitHub!
pause
