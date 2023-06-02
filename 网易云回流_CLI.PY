import random
import urllib.request
import subprocess
from bs4 import BeautifulSoup
import winreg

def generate_user_agent():
    # 生成随机的 User-Agent
    major_version = random.randint(60, 91)
    minor_version = random.randint(0, 9999)
    build_version = random.randint(0, 9999)
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{major_version}.0.{minor_version}.{build_version} Safari/537.36"
    return user_agent

def get_fastest_proxy():
    # 发送网络请求并获取网页内容
    url = 'https://proxy.ip3366.net/free/'
    req = urllib.request.Request(url, headers={'User-Agent': generate_user_agent()})
    response = urllib.request.urlopen(req)
    html_content = response.read()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找包含代理服务器信息的表格
    table = soup.find('table', class_='table table-bordered table-striped')

    # 提取表头信息
    headers = [header.text for header in table.find('thead').find_all('th')]

    # 初始化最快响应速度和对应的地址、位置
    fastest_speed = float('inf')
    fastest_address = ''
    fastest_area = ''

    # 遍历表格行并提取代理服务器信息
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        data = [column.text.strip() for column in columns]
        proxy = dict(zip(headers, data))
        
        # 提取响应速度并转换为浮点数
        response_speed = float(proxy['响应速度'][:-2])
        
        # 更新最快响应速度和对应的地址、位置
        if response_speed < fastest_speed:
            fastest_speed = response_speed
            fastest_address = proxy['IP'] + ':' + proxy['PORT']
            fastest_area = proxy['位置']

    return fastest_address, fastest_area, fastest_speed

def set_system_proxy(proxy_address):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(registry_key, "ProxyServer", 0, winreg.REG_SZ, proxy_address)
        winreg.CloseKey(registry_key)
        print(f"System proxy set to: {proxy_address}")
    except Exception as e:
        print("Failed to set system proxy: " + str(e))

def clear_system_proxy():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(registry_key, "ProxyServer", 0, winreg.REG_SZ, "")
        winreg.CloseKey(registry_key)
        print("System proxy cleared")
    except Exception as e:
        print("Failed to clear system proxy: " + str(e))

def update_proxy_info():
    try:
        # 获取最快的代理地址和位置
        fastest_proxy, area, speed = get_fastest_proxy()

        # 更新代理地址和位置显示
        print(f"最快的代理地址: {fastest_proxy}")
        print(f"地区: {area}")
        print(f"响应速度: {speed} ms")

        # 设置系统代理
        set_system_proxy(fastest_proxy)
    except Exception as e:
        print("Error: " + str(e))

# 更新代理信息
update_proxy_info()
