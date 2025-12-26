# استخدام نسخة بايثون مستقرة
FROM python:3.9-slim

# تحديث النظام وتثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    tor \
    && rm -rf /var/lib/apt/lists/*

# تثبيت متصفح جوجل كروم (الطريقة الحديثة والمستقرة)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# إعداد المجلد الرئيسي
WORKDIR /app
COPY . /app

# تثبيت مكتبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# فتح المنفذ المطلوب لـ Render
EXPOSE 10000

# تشغيل Tor في الخلفية ثم تشغيل البوت
CMD service tor start && python main.py
