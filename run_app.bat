@echo off
echo =================================================
echo  EQ Clone - Iniciando...
echo =================================================

echo [1/2] Verificando e instalando dependencias...
py -m pip install -r requirements.txt

echo.
echo [2/2] Lanzando aplicacion...
py -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo HUB UNA ERROR AL INICIAR LA APP.
    echo Asegurate de tener Python instalado y agregado al PATH.
    pause
)
