import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

login = '9vjSgf'
password = '4mTD2v'

proxy = {
    "scheme": "socks5",
    "hostname": "217.29.53.104",
    "port": 12243,
    "username": "9vjSgf",
    "password": "4mTD2v"
}

def get_location(url):
    response = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.find('div', class_='ip').text.strip()
    location = soup.find('div', class_='value-country').text.strip()
    print(ip)
    print(location)

def main():
    return get_location(url='https://2ip.ru')

if __name__ == '__main__':
    main()
