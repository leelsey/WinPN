import argparse, winreg

DEFAULT_AUTO_PROXY_URL = "http://0.0.0.0:8080" # Default address for the automatic proxy, it's sample
DEFAULT_PROXY_SERVER = "127.0.0.1:8080" # Default address for the proxy server, it's sample
INTERNET_SETTINGS = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings'
REG_PROXY_KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTERNET_SETTINGS, 0, winreg.KEY_ALL_ACCESS)
DETECT_PROXY_KEY = 'AutoDetect'
SCRIPT_PROXY_KEY = 'AutoConfigURL'
PROXY_ENABLE_KEY = 'ProxyEnable'
PROXY_SERVER_KEY = 'ProxyServer'


def toggle_detect_proxy(status):
    if status:
        winreg.SetValueEx(REG_PROXY_KEY, DETECT_PROXY_KEY, 0, winreg.REG_DWORD, 1)
        print("enablea automatically detect proxy")
    else:
        winreg.SetValueEx(REG_PROXY_KEY, DETECT_PROXY_KEY, 0, winreg.REG_DWORD, 0)
        print("disabled automatically detect proxy")
    winreg.CloseKey(REG_PROXY_KEY)
    exit()


def toggle_script_proxy(status, address):
    if status:
        winreg.SetValueEx(REG_PROXY_KEY, SCRIPT_PROXY_KEY, 0, winreg.REG_SZ, address)
        print("enabled automatic proxy script to: " + address)
    else:
        try:
            winreg.DeleteValue(REG_PROXY_KEY, SCRIPT_PROXY_KEY)
            print("disabled automatic proxy script")
        except FileNotFoundError:
            print("already disabled automatic proxy script")
    winreg.CloseKey(REG_PROXY_KEY)
    exit()


def toggle_proxy_server(status, address):
    if status:
        winreg.SetValueEx(REG_PROXY_KEY, PROXY_ENABLE_KEY, 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(REG_PROXY_KEY, PROXY_SERVER_KEY, 0, winreg.REG_SZ, address)
        print("enabled proxy server to: " + address)
    else:
        if winreg.QueryValueEx(REG_PROXY_KEY, PROXY_ENABLE_KEY)[0] == 0:
            print("already disabled proxy server")
        else:
            winreg.SetValueEx(REG_PROXY_KEY, PROXY_ENABLE_KEY, 0, winreg.REG_DWORD, 0)
            print("disabled windows proxy")
    winreg.CloseKey(REG_PROXY_KEY)
    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--detect", choices=['on', 'enable', 'e', 'off', 'disable', 'd'], help="Enable/disable automatically detect proxy")
    parser.add_argument("-s", "--script", choices=['on', 'enable', 'e', 'off', 'disable', 'd'], help="Enable/disable setup script proxy")
    parser.add_argument("-m", "--manual", choices=['on', 'enable', 'e', 'off', 'disable', 'd'], help="Enable/disable manual proxy server")
    parser.add_argument("-l", "--localproxy", nargs=1, metavar="Localhost Proxy", help="Enable manual proxy server with localhost")
    parser.add_argument("-a", "--address", nargs=1, metavar="Address", help="Address for the automatic proxy or the server proxy")
    args = parser.parse_args()

    if args.detect == 'on' or args.detect == 'enable' or args.detect == 'e':
        toggle_detect_proxy(True)
    elif args.detect == 'off' or args.detect == 'disable' or args.detect == 'd':
        toggle_detect_proxy(False)

    if args.script == 'on' or args.script == 'enable' or args.script == 'e':
        if args.address:
            proxy_path = args.address[0]
        else:
            proxy_path = DEFAULT_AUTO_PROXY_URL
        toggle_script_proxy(True, proxy_path)
    elif args.script == 'off' or args.script == 'disable' or args.script == 'd':
        toggle_script_proxy(False, None)

    if args.manual == 'on' or args.manual == 'enable' or args.manual == 'e':
        if args.address:
            proxy_path = args.address[0]
        else:
            proxy_path = DEFAULT_PROXY_SERVER
        toggle_proxy_server(True, proxy_path)
    elif args.manual == 'off' or args.manual == 'disable' or args.manual == 'd':
        toggle_proxy_server(False, None)

    if args.localproxy:
        proxy_path = args.localproxy[0]
        toggle_proxy_server(True, '127.0.0.1:'+proxy_path)
