@echo off
REM Compile all Python files to .pyc
python -m compileall .

REM Create the dist directory if it doesn't exist
if not exist dist (
    mkdir dist
)

REM Move and rename all .pyc files to the dist directory
for /r %%f in (*.cpython-*.pyc) do (
    set "filename=%%~nf"
    setlocal enabledelayedexpansion
    set "filename=!filename:.cpython-312=!"
    move "%%f" "dist\!filename!.pyc"
    endlocal
)

REM Create a temporary directory for the zip structure
if not exist temp_zip (
    mkdir temp_zip
)

REM Copy start.bat and requirements.txt to the temporary directory
copy start.bat temp_zip
copy requirements.txt temp_zip

REM Move the dist directory to the temporary directory
move dist temp_zip

REM Delete the existing zip file if it exists
if exist "Evo Arrows Helper.zip" (
    del "Evo Arrows Helper.zip"
)

REM Compress the temp_zip folder into a zip file using PowerShell
powershell -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('temp_zip', 'Evo Arrows Helper.zip')"

REM Clean up the temporary directory
rmdir /S /Q temp_zip

echo Build complete: Evo Arrows Helper.zip