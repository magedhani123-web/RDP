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

# --- إعداد السيرفر الوهمي للبقاء حياً ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Imperial Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- إعدادات البوت والقناة ---
VIDEO_ID = "MrKhyV4Gcog"
DIRECT_URL = f"https://youtube.com/shorts/{VIDEO_ID}"
TOR_PROXY = "socks5://127.0.0.1:9050"

# مكتبة الأنظمة (تعدد الأجهزة)
DEVICES = [
    {"name": "iPhone 15 Pro", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15", "plat": "iPhone", "w": 393, "h": 852},
    {"name": "Samsung S23 Ultra", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/119.0.0.0 Mobile", "plat": "Linux armv8l", "w": 360, "h": 800},
    {"name": "Xiaomi 13 Pro", "ua": "Mozilla/5.0 (Linux; Android 13; 2210132G) Chrome/118.0.0.0 Mobile", "plat": "Linux armv8l", "w": 393, "h": 873},
    {"name": "Windows 11 Desktop", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0", "plat": "Win32", "w": 1920, "h": 1080},
    {"name": "MacBook Air M2", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36", "plat": "MacIntel", "w": 1440, "h": 900}
]

def inject_stealth(driver, dev):
    """حقن أكواد التخفي وتزييف الجهاز"""
    js = f"""
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    Object.defineProperty(navigator, 'platform', {{get: () => '{dev["plat"]}'}});
    // تزييف البطارية لتبدو حقيقية
    navigator.getBattery = () => Promise.resolve({{charging: true, level: 0.85}});
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

def get_driver(dev):
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--user-agent={dev["ua"]}')
    options.add_argument(f"--window-size={dev['w']},{dev['h']}")
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.binary_location = "/usr/bin/google-chrome"

    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
        inject_stealth(driver, dev)
        return driver
    except Exception as e:
        print(f"❌ Driver Error: {e}")
        return None

def bot_loop():
    while True:
        dev = random.choice(DEVICES)
        print(f"\n--- 👑 جلسة إمبراطورية جديدة | الجهاز: {dev['name']} ---")
        
        driver = get_driver(dev)
        if driver:
            try:
                driver.get(DIRECT_URL)
                time.sleep(7)
                
                # 1. تغيير السرعة عشوائياً (0.75x, 1x, 1.25x)
                speed = random.choice([0.75, 1, 1.25, 1.5])
                try:
                    video = driver.find_element(By.TAG_NAME, "video")
                    driver.execute_script(f"arguments[0].playbackRate = {speed};", video)
                    driver.execute_script("arguments[0].play();", video)
                    print(f"⚡ السرعة المطبقة: {speed}x")
                except: pass
                
                # 2. المشاهدة بمدة عشوائية
                watch_time = random.randint(60, 95)
                print(f"📺 مشاهدة جارية لـ {watch_time} ثانية...")
                
                # محاكاة حركة السكرول (البشرية)
                time.sleep(watch_time // 2)
                driver.execute_script(f"window.scrollBy(0, {random.randint(100, 400)});")
                time.sleep(watch_time // 2)
                
                print("✅ اكتملت الجلسة بنجاح")
            except Exception as e:
                print(f"❌ خطأ أثناء الجلسة: {str(e)[:50]}")
            finally:
                driver.quit()
        
        # استراحة عشوائية بين الجلسات لتجنب كشف البوت
        wait_gap = random.randint(15, 30)
        print(f"😴 استراحة لـ {wait_gap} ثانية...")
        time.sleep(wait_gap)

if __name__ == "__main__":
    # تشغيل Flask في الخلفية لإبقاء الرابط فعالاً
    threading.Thread(target=run_flask, daemon=True).start()
    
    # تشغيل حلقة البوت الإمبراطورية
    bot_loop()
