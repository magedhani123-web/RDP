import threading
import time
import random
import os
import shutil
import requests
from flask import Flask
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- إعداد السيرفر الوهمي (لإبقاء Render يعمل) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- إعدادات البوت ---
VIDEO_ID = "MrKhyV4Gcog" # ضع معرف الفيديو هنا
DIRECT_URL = f"https://youtube.com/shorts/{VIDEO_ID}"
TOR_PROXY = "socks5://127.0.0.1:9050"

def get_driver():
    options = uc.ChromeOptions()
    # إعدادات خاصة جداً لسيرفرات Render لتقليل استهلاك الرام
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=375,812') # حجم موبايل لتوفير الموارد
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    
    # تحديد مسار Chrome يدوياً لأن Render قد يضيعه
    options.binary_location = "/usr/bin/google-chrome"

    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
        return driver
    except Exception as e:
        print(f"❌ Driver Error: {e}")
        return None

def bot_loop():
    while True:
        print("\n--- 🚀 بدء جلسة جديدة ---")
        driver = get_driver()
        if driver:
            try:
                driver.get(DIRECT_URL)
                time.sleep(5)
                
                # محاولة التشغيل
                try:
                    driver.execute_script("document.querySelector('video').play()")
                except: pass
                
                watch_time = random.randint(50, 70)
                print(f"📺 مشاهدة لمدة {watch_time} ثانية...")
                time.sleep(watch_time)
                
                print("✅ انتهت المشاهدة")
            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                driver.quit()
        
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    # تشغيل السيرفر في خيط منفصل
    t1 = threading.Thread(target=run_flask)
    t1.start()
    
    # تشغيل البوت
    bot_loop()
