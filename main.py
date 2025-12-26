import threading
import time
import random
import os
from flask import Flask
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/')
def home():
    return "Lite Imperial Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

VIDEO_ID = "MrKhyV4Gcog"
DIRECT_URL = f"https://m.youtube.com/shorts/{VIDEO_ID}" # استخدام نسخة الموبايل الخفيفة
TOR_PROXY = "socks5://127.0.0.1:9050"

DEVICES = [
    {"ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15", "w": 360, "h": 640},
    {"ua": "Mozilla/5.0 (Linux; Android 13; SM-G991B) Chrome/118.0.0.0 Mobile", "w": 360, "h": 640}
]

def get_driver():
    dev = random.choice(DEVICES)
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--user-agent={dev["ua"]}')
    options.add_argument(f"--window-size={dev['w']},{dev['h']}")
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    
    # --- أهم إعدادات لتقليل الرام ---
    options.add_argument('--disable-extensions')
    options.add_argument('--blink-settings=imagesEnabled=false') # منع تحميل الصور نهائياً
    options.binary_location = "/usr/bin/google-chrome"

    try:
        # استخدام subprocess لضمان عدم بقاء عمليات معلقة في الرام
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
        return driver
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def bot_loop():
    while True:
        print("\n--- ⚡ بدء جلسة خفيفة (RAM Optimized) ---")
        driver = get_driver()
        if driver:
            try:
                driver.get(DIRECT_URL)
                time.sleep(10)
                
                # تشغيل الفيديو وتعديل السرعة
                try:
                    video = driver.find_element(By.TAG_NAME, "video")
                    driver.execute_script("arguments[0].playbackRate = 1.25; arguments[0].play();", video)
                except: pass
                
                watch_time = random.randint(55, 75)
                print(f"📺 مشاهدة جارية ({watch_time}s)...")
                time.sleep(watch_time)
                
                print("✅ اكتملت الجلسة")
            except Exception as e:
                print(f"❌ Error during session")
            finally:
                driver.quit() # إغلاق المتصفح تماماً لتحرير الرام
        
        # استراحة أطول قليلاً للسماح للسيرفر بتنظيف الرام
        wait = random.randint(30, 60)
        print(f"😴 استراحة {wait} ثانية لتنظيف الذاكرة...")
        time.sleep(wait)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot_loop()
