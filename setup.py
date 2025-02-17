import PyInstaller.__main__ as pyinst
from main import VERSION


if __name__ == "__main__":
    pyinst.run([
        'main.py',
        '--onefile',
        '--nowindow',
        '--log-level=WARN',
        f'-n RadiusVKBot_v{VERSION}',
        '--icon=./icon.ico',
    ])
