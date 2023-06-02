import threading
import tkinter as tk
import tkinter.ttk as ttk
import socket
import time
import requests
import winreg

proxy_list = [
    '112.244.231.189:9000'
]

def get_ip_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        country = data.get('country', '')
        city = data.get('city', '')
        return f"{country}, {city}"
    else:
        return "N/A"

def set_system_proxy(proxy_address):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(registry_key, "ProxyServer", 0, winreg.REG_SZ, proxy_address)
        winreg.CloseKey(registry_key)
        print(f"System proxy set to: {proxy_address}")
    except Exception as e:
        print("Failed to set system proxy:", str(e))

def test_proxies():
    proxy_output.delete(1.0, tk.END)  # 清空输出框内容

    total_proxies = len(proxy_list)
    response_times = []
    current_proxy_index = 0

    def test_proxy():
        nonlocal current_proxy_index

        if current_proxy_index >= total_proxies:
            if response_times:
                fastest_proxy = min(response_times, key=lambda x: x[1])[0]
                set_system_proxy(fastest_proxy)
            else:
                proxy_output.insert(tk.END, "No available proxies.\n")
            progress_bar['value'] = 100
            proxy_status.set("Testing completed.")
            return

        proxy = proxy_list[current_proxy_index]
        proxy_addr = proxy.replace("http://", "")
        set_system_proxy(proxy)
        try:
            start_time = time.time()
            response = requests.get("http://http://translate.google.cn/", timeout=2)
            elapsed_time = time.time() - start_time
            if response.status_code == 200:
                location = get_ip_location(proxy_addr)
                response_times.append((proxy, elapsed_time, location))
                proxy_output.insert(tk.END, f"Proxy: {proxy} - Location: {location} - Response Time: {elapsed_time:.2f} seconds\n")
            else:
                proxy_output.insert(tk.END, f"Proxy: {proxy} - Failed to connect to Google\n")
        except requests.exceptions.RequestException:
            proxy_output.insert(tk.END, f"Proxy: {proxy} - Failed to connect\n")

        current_proxy_index += 1
        progress = current_proxy_index / total_proxies * 100
        progress_bar['value'] = progress
        proxy_status.set(f"Testing proxies... {progress:.2f}%")

        # 延迟一段时间后再进行下一次测试
        window.after(100, test_proxy)

    # 创建线程并启动
    test_proxy()

# 创建窗口
window = tk.Tk()
window.title("Proxy Tester")

# 创建组件
proxy_label = tk.Label(window, text="Proxy List:")
proxy_output = tk.Text(window, width=50, height=10)
test_button = tk.Button(window, text="Test Proxies", command=test_proxies)
proxy_status = tk.StringVar()
status_label = tk.Label(window, textvariable=proxy_status)
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')

# 布局组件
proxy_label.pack()
proxy_output.pack()
test_button.pack()
status_label.pack()
progress_bar.pack()

# 运行窗口
window.mainloop()
