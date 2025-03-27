#!/usr/bin/env bash
mkdir -p .chromium
cd .chromium

# 下載 Chrome
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chrome-linux64.zip
unzip chrome-linux64.zip

# 下載 ChromeDriver
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip

mv chrome-linux64 chrome-linux
mv chromedriver-linux64/chromedriver .

echo "✅ Chromium 安裝完成"
