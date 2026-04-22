from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://admin:admin@the-internet.herokuapp.com/basic_auth"
driver.get(url)

# Lấy nội dung sau khi login
heading = driver.find_element(By.TAG_NAME, "h3").text
message = driver.find_element(By.TAG_NAME, "p").text

print("Heading:", heading)
print("Message:", message)

# ===== VALIDATION =====
assert "Basic Auth" in heading
assert "Congratulations" in message

print("PASS: Login success")

time.sleep(10)

driver.quit()