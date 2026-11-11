
@echo off
setlocal
cd /d "%~dp0"

title Teste de Erro - Projeto B

echo ==========================================
echo       TESTE DE FALHA CONTROLADA
echo ==========================================
echo.

".venv\Scripts\python.exe" -m testes.teste_codigo_saida

set "RESULTADO=%ERRORLEVEL%"

echo.
echo ==========================================

if "%RESULTADO%"=="0" (
    echo SUCESSO: Codigo de saida 0.
) else (
    echo ERRO DETECTADO: Codigo de saida %RESULTADO%.
)

echo ==========================================
echo.
pause
exit /b %RESULTADO%
