import os
import time
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://mymeet.ai/ru"
OUTPUT_DIR_TEXT = "text"
OUTPUT_DIR_IMAGES = "images"

logging.basicConfig(level=logging.ERROR)

def create_dirs():
    os.makedirs(OUTPUT_DIR_TEXT, exist_ok=True)
    os.makedirs(OUTPUT_DIR_IMAGES, exist_ok=True)

def get_page_content(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ru-RU")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html

def extract_main_text(soup):
    content = []
    for tag in soup.find_all(["p", "h1", "h2", "h3", "span"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 5:
            content.append(text)
    return "\n".join(content)

def save_text(text):
    filepath = os.path.join(OUTPUT_DIR_TEXT, "content.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

def download_image(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            filename = "image.jpg"
        filepath = os.path.join(OUTPUT_DIR_IMAGES, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        logging.error(f"Ошибка загрузки изображения: {url} ({e})")

def scrape():
    create_dirs()
    html = get_page_content(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = extract_main_text(soup)
    if text:
        save_text(text)

    images = soup.find_all("img")
    for img in images:
        src = img.get("src")
        if src:
            img_url = urljoin(BASE_URL, src)
            download_image(img_url)

if __name__ == "__main__":
    scrape()
