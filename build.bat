@echo off
echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Gerando executavel...
pyinstaller CalculadoraFinanceira.spec

echo.
echo Concluido! O executavel esta em: dist\CalculadoraFinanceira.exe
pause
