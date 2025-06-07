# MyMeet Scraper

Скрипт парсит главную страницу сайта [mymeet.ai](http://mymeet.ai), извлекая:

- весь текст (включая динамически загружаемый контент),
- все изображения,
- и сохраняет результат в отдельные директории `text/` и `images/`.

Работает внутри Docker, использует `Selenium + Chromium` для полной эмуляции браузера.

---

## 📦 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone git@github.com:grichenkov/mymeet_scraper.git
cd mymeet_scraper
```


### 2. Собрать Docker-образ
```bash
docker build -t mymeet-scraper .
```

### 3. Запустить парсинг
```bash
docker run --rm -v "$(pwd)/app:/app" --shm-size=1g mymeet-scraper
```

### 4. Зависимости

```bash
pip install -r requirements.txt
```