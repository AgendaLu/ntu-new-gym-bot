# main.py

import os
import time
import threading
import socket
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def get_ntu_gym_current_people():
    options = Options()
    options.binary_location = "/opt/render/project/src/.chromium/chrome-linux/chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/opt/render/project/src/.chromium/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://rent.pe.ntu.edu.tw/")
    time.sleep(5)

    try:
        span = driver.find_element(By.XPATH, '//*[@id="CMain"]/div[4]/div/div[1]/div[1]/div[2]/div[1]/span')
        current_people = span.text
    except Exception as e:
        current_people = "錯誤"
        print("❌ 錯誤：", e)

    driver.quit()
    return f"🏋️‍♂️ 台大新體現在人數：{current_people} 人"

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()
    if text == 'p':
        reply = get_ntu_gym_current_people()
        update.message.reply_text(reply)
    else:
        update.message.reply_text("請輸入 'p' 查詢台大新體目前人數")

# 加在 run_telegram_bot() 的上方或 main 的開頭

def dummy_web_server():
    port = int(os.environ.get("PORT", 10000))
    sock = socket.socket()
    sock.bind(("0.0.0.0", port))
    sock.listen(1)
    print(f"🌀 假裝的 web server 綁定在 port {port}（只是為了騙過 Render）")
    while True:
        conn, addr = sock.accept()
        conn.send(b"Hello from dummy web server!\n")
        conn.close()

# 在 main 執行區啟動這個背景假 server
threading.Thread(target=dummy_web_server, daemon=True).start()

def run_telegram_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("✅ Bot 已啟動")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_telegram_bot()
