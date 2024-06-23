import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from threading import Thread
from json import dumps


load_dotenv('.env')

def get_rakuten_search_product_urls(search_text):
    url = os.getenv("RAKUTEN_PRODUCT_SERACH_URL") + search_text
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    products = soup.find_all(class_="content review")
    review_urls = [ product.find('a').attrs['href'] for product in products]
    
    return review_urls


def get_amazon_search_product_urls(search_text):
    url = os.getenv("AMAZON_PRODUCT_SEARCH_URL") + search_text
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    products = soup.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    review_urls = [ product.attrs['href'] for product in products]
    
    return review_urls


def get_rakuten_review_comments(url, review_comments):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    reviews = soup.find_all(class_="review-body--1pESv")
    for review in reviews:
        review_comments.append(review.get_text(strip=True))


def get_amazon_review_comments(path, review_comments):
    html = requests.get(os.getenv("AMAZON_DOMAIN_URL") + path)
    soup = BeautifulSoup(html.text,'html.parser')
    reviews = soup.find_all(class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")
    for review in reviews:
        review_comments.append(review.get_text(strip=True))

        
async def send_socket_message(websocket, result):
    await websocket.send_json(result)


async def send_rakuten_review_comment_posinaga(search_text, model, websocket):
    try:
        review_comments = []
        product_urls = get_rakuten_search_product_urls(search_text)
        task_list = [ Thread(target=get_rakuten_review_comments, args=(url, review_comments, )) for url in product_urls]
        
        for task in task_list:
            task.start()
        
        for task in task_list:
            task.join()
        
        for review_comment in review_comments:
            send_message = {"action": "processing", "resource": "rakuten", "result": model.predict(review_comment[:500])}
            await send_socket_message(websocket, send_message)
        
        end_message = {"action": "rakuten_end"}
        await send_socket_message(websocket, end_message)
    except Exception as e:
        exception_server_message = {"action": "stop", "message": e}
        await websocket.send_json(exception_server_message)


async def send_amazon_review_comment_posinaga(search_text, model, websocket):
    try:
        review_comments = []
        product_urls = get_amazon_search_product_urls(search_text)
        task_list = [ Thread(target=get_amazon_review_comments, args=(url, review_comments, )) for url in product_urls]
        
        for task in task_list:
            task.start()
        
        for task in task_list:
            task.join()
        
        for review_comment in review_comments:
            send_message = {"action": "processing", "resource": "amazon", "result": model.predict(review_comment[:500])}
            await send_socket_message(websocket, send_message)
        
        end_message = {"action": "amazon_end"}
        await send_socket_message(websocket, end_message)
    except Exception as e:
        exception_server_message = {"action": "stop", "message": e}
        await websocket.send_json(exception_server_message)