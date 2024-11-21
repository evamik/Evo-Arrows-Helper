@echo off
setlocal enabledelayedexpansion

set SOURCE_DIR=%cd%
set BUILD_DIR=%cd%\built_project
set TEMP_DIR=%cd%\Evo Arrows Helper

if exist "Evo Arrows Helper.zip" (
    del "Evo Arrows Helper.zip"
)

if exist "%BUILD_DIR%" (
    rmdir /S /Q "%BUILD_DIR%"
)

mkdir "%BUILD_DIR%"

python -m compileall -b -f "%SOURCE_DIR%"

for /R "%SOURCE_DIR%" %%F in (*.pyc) do (
    if not "%%~dpF"=="%BUILD_DIR%\" if /I not "%%~xF"==".zip" (
        set "REL_PATH=%%~dpF"
        set "REL_PATH=!REL_PATH:%SOURCE_DIR%=!"
        if "!REL_PATH:~0,1!" == "\" set "REL_PATH=!REL_PATH:~1!"
        if not exist "%BUILD_DIR%\!REL_PATH!" mkdir "%BUILD_DIR%\!REL_PATH!"
        move "%%F" "%BUILD_DIR%\!REL_PATH!"
    )
)

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

copy start.bat "%TEMP_DIR%"
copy requirements.txt "%TEMP_DIR%"
copy README.md "%TEMP_DIR%"

move "%BUILD_DIR%" "%TEMP_DIR%\dist"

powershell -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('Evo Arrows Helper', 'Evo Arrows Helper.zip')"

rmdir /S /Q "Evo Arrows Helper"

echo Build complete: Evo Arrows Helper.zip
pause