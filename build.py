import subprocess

# Define the path to UPX
upx_dir = r"C:\upx-4.2.4-win64\upx-4.2.4-win64"

pyinstaller_command = [
    "pyinstaller",
    "--onefile",
    "--strip",
    "--optimize=2",
    f"--upx-dir={upx_dir}",
    "--upx-exclude=vcruntime140.dll",
    "--hidden-import=pygetwindow",
    "--hidden-import=keyboard",
    "--hidden-import=Pillow",
    "--hidden-import=pytesseract",
    "--hidden-import=pyautogui",
    "--name=Evo Arrow Helper",
    "main.py"
]

subprocess.run(pyinstaller_command, check=True)