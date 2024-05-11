import requests
import queue
import threading
from bs4 import BeautifulSoup

req = requests.session()
q = queue.Queue()
valid = []


def get():
    res = req.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(res.text, "lxml")
    proxy_list = soup.find('textarea').get_text()
    proxy_list = proxy_list.split('\n')[3:-1]
    for i, p in enumerate(proxy_list, start=1):
        q.put(p)


def check():
    while not q.empty():
        ip = q.get()
        proxy = {
            "http": ip,
            "https": ip
        }
        try:
            res = req.get("https://ipinfo.io/json", proxies=proxy)
        except requests.RequestException:
            continue
        if res.status_code == 200:
            if ip.endswith(":3128"):
                valid.append(ip)
            else:
                print(ip)


def run():
    while True:
        try:
            ip = valid[0]
            proxy = {
                "http": ip,
                "https": ip
            }
            res = req.get("https://ipinfo.io/json", proxies=proxy)
            print(res.json())
            break
        except IndexError:
            continue


if __name__ == '__main__':
    get()
    threading.Thread(target=run).start()
    for _ in range(10):
        th = threading.Thread(target=check)
        th.start()
