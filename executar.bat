
@echo off
setlocal
cd /d "%~dp0"

title Projeto B - Automacao de Relatorios

echo ==========================================
echo       AUTOMACAO DE RELATORIOS
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado.
    echo.
    echo Instale as dependencias antes de executar.
    pause
    exit /b 1
)

echo Iniciando processamento...
echo.

".venv\Scripts\python.exe" main.py

set "RESULTADO=%ERRORLEVEL%"

echo.
echo ==========================================

if "%RESULTADO%"=="0" (
    echo Processamento encerrado.
    echo Confira o resultado e os logs acima.
) else (
    echo ERRO: O processamento retornou codigo %RESULTADO%.
    echo Consulte os logs para mais detalhes.
)

echo ==========================================
echo.
pause
exit /b %RESULTADO%
