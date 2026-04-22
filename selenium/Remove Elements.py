from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Mở trang
driver.get("https://the-internet.herokuapp.com/add_remove_elements/")

print("Test Add/Remove Elements")

# ===== TEST 1: Add 1 element =====
add_btn = driver.find_element(By.XPATH, "//button[text()='Add Element']")
add_btn.click()

# Verify có 1 nút Delete
delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
assert len(delete_buttons) == 1

print("PASS: Add 1 element")

# ===== TEST 2: Add multiple elements =====
for i in range(4):
    add_btn.click()

delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
assert len(delete_buttons) == 5

print("PASS: Add multiple elements")

# ===== TEST 3: Remove 1 element =====
delete_buttons[0].click()

wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "added-manually")) == 4)

delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
assert len(delete_buttons) == 4

print("PASS: Remove 1 element")

# ===== TEST 4: Remove all elements =====
while True:
    delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
    if len(delete_buttons) == 0:
        break
    delete_buttons[0].click()

delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
assert len(delete_buttons) == 0

print("PASS: Remove all elements")

driver.quit()