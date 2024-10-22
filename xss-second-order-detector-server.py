from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Set up the Selenium WebDriver (Chrome example)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

@app.route('/')
def open_specific_page():
    url = "https://0a9500fe03c1b1c682c3ecc400ea0090.web-security-academy.net/post?postId=5"  # The specific page you want to open for every request
    driver.get(url)
    return jsonify({"status": "success", "message": f"Opened {url}"}), 200

if __name__ == '__main__':
    app.run(port=5000)
