import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from threading import Thread
from json import dumps


html = requests.get("https://www.amazon.co.jp/s?k=スイッチ")
soup = BeautifulSoup(html.text, 'html.parser')
urls = []
for i in soup.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"):
    urls.append(i.attrs["href"])

print(urls)