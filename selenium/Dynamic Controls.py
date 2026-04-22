from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://the-internet.herokuapp.com/dynamic_controls")

print("===== TEST DYNAMIC CONTROLS =====")

# ===== TEST 1: Remove checkbox =====
remove_btn = driver.find_element(By.XPATH, "//button[text()='Remove']")
checkbox = driver.find_element(By.ID, "checkbox")

assert checkbox.is_displayed()
remove_btn.click()

# Wait checkbox biến mất
wait.until(EC.invisibility_of_element_located((By.ID, "checkbox")))

message = driver.find_element(By.ID, "message").text
print("Message:", message)

assert "It's gone!" in message
print("PASS: Remove checkbox")

# ===== TEST 2: Add checkbox lại =====
add_btn = driver.find_element(By.XPATH, "//button[text()='Add']")
add_btn.click()

# Wait checkbox xuất hiện lại
wait.until(EC.presence_of_element_located((By.ID, "checkbox")))

checkbox = driver.find_element(By.ID, "checkbox")
assert checkbox.is_displayed()

message = driver.find_element(By.ID, "message").text
assert "It's back!" in message

print("PASS: Add checkbox")

# ===== TEST 3: Enable input =====
enable_btn = driver.find_element(By.XPATH, "//button[text()='Enable']")
input_box = driver.find_element(By.XPATH, "//input[@type='text']")

assert not input_box.is_enabled()

enable_btn.click()

# Wait input enabled
wait.until(lambda d: d.find_element(By.XPATH, "//input[@type='text']").is_enabled())

input_box = driver.find_element(By.XPATH, "//input[@type='text']")
assert input_box.is_enabled()

message = driver.find_element(By.ID, "message").text
assert "It's enabled!" in message

print("PASS: Enable input")

# ===== TEST 4: Disable input =====
disable_btn = driver.find_element(By.XPATH, "//button[text()='Disable']")
disable_btn.click()

# Wait input disabled
wait.until(lambda d: not d.find_element(By.XPATH, "//input[@type='text']").is_enabled())

input_box = driver.find_element(By.XPATH, "//input[@type='text']")
assert not input_box.is_enabled()

message = driver.find_element(By.ID, "message").text
assert "It's disabled!" in message

print("PASS: Disable input")

driver.quit()