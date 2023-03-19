import argparse, winreg


DEFAULT_AUTO_PROXY_URL = "http://0.0.0.0:8080" # Default address for the automatic proxy, it's sample
DEFAULT_PROXY_SERVER = "127.0.0.1:8080" # Default address for the proxy server, it's sample
INTERNET_SETTINGS = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
REG_PROXY_KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTERNET_SETTINGS, 0, winreg.KEY_ALL_ACCESS)
AUTO_PROXY_KEY = 'AutoConfigURL'
PROXY_SERVER_KEY = 'ProxyServer'
PROXY_ENABLE_KEY = 'ProxyEnable'


def toggle_auto_proxy(status, address):
    if status:
        winreg.SetValueEx(REG_PROXY_KEY, AUTO_PROXY_KEY, 0, winreg.REG_SZ, address)
    else:
        winreg.DeleteValue(REG_PROXY_KEY, AUTO_PROXY_KEY)
    winreg.CloseKey(REG_PROXY_KEY)


def toggle_proxy_server(status, address):
    if status:
        winreg.SetValueEx(REG_PROXY_KEY, PROXY_ENABLE_KEY, 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(REG_PROXY_KEY, PROXY_SERVER_KEY, 0, winreg.REG_SZ, address)
    else:
        winreg.SetValueEx(REG_PROXY_KEY, PROXY_ENABLE_KEY, 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(REG_PROXY_KEY)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", choices=['on', 'off'], help="Enable/disable automatic proxy configuration")
    parser.add_argument("-s", "--server", choices=['on', 'off'], help="Enable/disable manual proxy server")
    parser.add_argument("-l", "--localproxy", nargs=1, metavar="Localhost Proxy", help="Enable manual proxy server with localhost")
    parser.add_argument("-m", "--modify", nargs=1, metavar="Address", help="Address for the automatic proxy or the server proxy")
    args = parser.parse_args()

    if args.auto == 'on':
        if args.modify:
            proxy_path = args.modify[0]
        else:
            proxy_path = DEFAULT_AUTO_PROXY_URL
        toggle_auto_proxy(True, proxy_path)
    elif args.auto == 'off':
        toggle_auto_proxy(False, None)

    if args.server == 'on':
        if args.modify:
            proxy_path = args.modify[0]
        else:
            proxy_path = DEFAULT_PROXY_SERVER
        toggle_proxy_server(True, proxy_path)
    elif args.server == 'off':
        toggle_proxy_server(False, None)

    if args.localproxy:
        proxy_path = args.localproxy[0]
        toggle_proxy_server(True, '127.0.0.1:'+proxy_path)
