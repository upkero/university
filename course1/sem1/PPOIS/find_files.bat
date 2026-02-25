
@echo off

if "%~2"=="" (
    echo Использование: %~nx0 <путь_к_папке> <атрибут>
    exit /b 1
)

set "DIRECTORY=%~1"
set "PERMISSIONS=%~2"

if not exist "%DIRECTORY%" (
    echo Данной папки нет
    exit /b 1
)

if exist result.txt del result.txt
for /r "%DIRECTORY%" %%f in (*) do (
    attrib "%%f" | find "%PERMISSIONS%" >nul
    if not errorlevel 1 echo %%f >> result.txt
)

echo Результаты сохранены в result.txt
