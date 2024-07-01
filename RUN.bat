@echo off
REM Cambia el directorio al lugar donde se encuentra el script Python dentro de la carpeta 'scripts'
cd scripts

REM Ejecuta el archivo Python
python Main.py

REM Vuelve al directorio anterior
cd ..

REM Espera a que el usuario presione una tecla antes de cerrar la ventana
pause
