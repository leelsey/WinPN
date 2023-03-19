# WinPN

### WIndows Proxy Network
WinPN is a proxy network CLI Controller for Windows.

## 1. Tested environments
1) OS: Windows 10 or later
2) Python: 3.8.0 or later

## 2. Usage
```powerappsfl
# usage: winpn [-h] [-a] [-s] [-l] [-m]

# optional arguments:
#  -h, --help            Show this help message and exit
#  -a, --auto            Enable/disable automatic proxy configuration
#  -s, --server          Enable/disable manual proxy server
#  -l, --localproxy      Enable manual proxy server with localhost
#  -m, --modify          Address for the automatic proxy or the server proxy

# example:
winpn -a [on/off]
winpn -m [on/off]
winpn -l [port]
winpn -a on -m [http://ip:port]
winpn -m on -m [ip:port]
```

## 3. Setup development environment
1) Setup python's virtual enviroment.
```powershell
python -m venv venv
```
2) Activate venv.
```powershell
.\venv\Scripts\Activate.ps1
```
If not did setup PowerSehll execution policy, try this berfore activate venv.
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```
3) Install requirements.
```powershell
pip install -r requirements.txt
```

## 4. Interpreter run
### WinWB
1) Open Windows Terminal (PowerShell or CMD) with run as administrator.
2) Run script.
```powershell
python .\winpn.py
```

## 5. Build .exe file
### WinWB
1) Build through pyinstaller.
```powershell
pyinstaller --uac-admin --onefile --name=wpn winpn.py
```
2) It's created in the dist directory.