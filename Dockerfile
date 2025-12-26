# استخدام صورة بايثون الأساسية
FROM python:3.9-slim

# تحديث النظام وتثبيت الأدوات الأساسية (Chrome + Tor)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    tor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# تثبيت متصفح Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# إعداد ملفات المشروع
WORKDIR /app
COPY . /app

# تثبيت مكتبات البايثون
RUN pip install --no-cache-dir -r requirements.txt

# فتح منفذ للسيرفر الوهمي (لإبقاء البوت يعمل)
EXPOSE 10000

# أمر التشغيل: تشغيل Tor في الخلفية ثم تشغيل البوت
CMD service tor start && python main.py
