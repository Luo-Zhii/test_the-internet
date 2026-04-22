from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://the-internet.herokuapp.com/challenging_dom")

print("===== TEST CHALLENGING DOM =====")

# ===== TEST 1: Verify heading =====
heading = driver.find_element(By.TAG_NAME, "h3").text
assert "Challenging DOM" in heading
print("PASS: Heading correct")
time.sleep(2)
# ===== TEST 2: Verify 3 buttons =====
buttons = wait.until(
    lambda d: d.find_elements(By.XPATH, "//a[contains(@class,'button')]")
)

print("Number of buttons:", len(buttons))
assert len(buttons) == 3
print("PASS: Found 3 buttons")

# Debug class (optional)
for b in buttons:
    print("Button class:", b.get_attribute("class"))
time.sleep(2)
# ===== TEST 3: Click button -> page reload =====
buttons[0].click()

# Sau khi reload phải tìm lại element
buttons = wait.until(
    lambda d: d.find_elements(By.XPATH, "//a[contains(@class,'button')]")
)

assert len(buttons) == 3
print("PASS: Click button reload OK")
time.sleep(2)

# ===== TEST 4: Verify table =====
table = driver.find_element(By.XPATH, "//table")
rows = table.find_elements(By.XPATH, ".//tr")

assert len(rows) > 1
print("PASS: Table exists")
time.sleep(2)

# ===== TEST 5: Verify dữ liệu row đầu =====
first_row = table.find_elements(By.XPATH, ".//tr")[1]
cells = first_row.find_elements(By.TAG_NAME, "td")

print("Number of columns:", len(cells))
assert len(cells) >= 6
print("PASS: Table structure valid")
time.sleep(2)

# ===== TEST 6: Click edit/delete =====
edit_btn = first_row.find_element(By.LINK_TEXT, "edit")
delete_btn = first_row.find_element(By.LINK_TEXT, "delete")

edit_btn.click()
delete_btn.click()

print("PASS: Edit/Delete clickable")
time.sleep(2)

# ===== TEST 7: Refresh test (DOM thay đổi) =====
canvas_before = driver.find_element(By.TAG_NAME, "canvas").text

driver.refresh()

canvas_after = driver.find_element(By.TAG_NAME, "canvas").text

# Có thể giống hoặc khác, nhưng không được crash
print("Canvas checked after refresh")
print("PASS: Refresh OK")
time.sleep(2)

driver.quit()