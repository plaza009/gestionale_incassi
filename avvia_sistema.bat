@echo off
echo ========================================
echo    SISTEMA GESTIONALE INCASSI
echo ========================================
echo.
echo Avvio del sistema...
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non è installato o non è nel PATH
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

REM Verifica se le dipendenze sono installate
echo Verifica dipendenze...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installazione dipendenze...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRORE: Impossibile installare le dipendenze
        pause
        exit /b 1
    )
)

echo.
echo Avvio del server...
echo.
echo Credenziali di accesso:
echo   Username: admin
echo   Password: admin123
echo.
echo Apri il browser su: http://localhost:5000
echo.
echo Premi Ctrl+C per fermare il server
echo.

python run.py

pause 