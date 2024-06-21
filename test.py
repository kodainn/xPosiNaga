# from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer,BertTokenizer, BertForSequenceClassification

# # パイプラインの準備
# model = AutoModelForSequenceClassification.from_pretrained('llm-book/bert-base-japanese-v3-wrime-sentiment') 
# tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
# classifier = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)

# result = classifier("自然言語処理の勉強はとても楽しい")
# print(result)

import requests
from bs4 import BeautifulSoup
 
url="https://review.rakuten.co.jp/item/1/373057_10001391/1.1/"
# html=requests.get(url)
# soup=BeautifulSoup(html.text,'html.parser')
# products=soup.find_all(class_="content review")
# for product in products:
#     print(product.find('a').attrs['href'])


html=requests.get(url)
soup=BeautifulSoup(html.text,'html.parser')
user_review = soup.find_all(class_="review-body--1pESv")
guest_review = soup.find_all(class_="no-ellipsis--IKXkO")
print("-----------------------ユーザー--------------------")
for review in user_review:
    print(review.get_text(strip=True))

print("----------------------guest------------------------")
for review in guest_review:
    print(review.get_text(strip=True))

