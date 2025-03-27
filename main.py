import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import time

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def get_ntu_gym_current_people():
    options = Options()
    options.binary_location = "/opt/render/project/src/.chromium/chrome-linux/chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        executable_path="/opt/render/project/src/.chromium/chromedriver",
        options=options
    )

    driver.get("https://rent.pe.ntu.edu.tw/")
    time.sleep(5)

    try:
        span = driver.find_element(By.XPATH, '//*[@id="CMain"]/div[4]/div/div[1]/div[1]/div[2]/div[1]/span')
        current_people = span.text
    except Exception as e:
        current_people = "錯誤"

    driver.quit()
    return f"🏋️‍♂️ 台大新體現在人數：{current_people} 人"

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()
    if text == 'p':
        reply = get_ntu_gym_current_people()
        update.message.reply_text(reply)
    else:
        update.message.reply_text("請輸入 'p' 查詢台大新體目前人數")

def run_telegram_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("✅ Bot 已啟動")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_telegram_bot()
