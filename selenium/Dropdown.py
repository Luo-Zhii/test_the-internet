from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://the-internet.herokuapp.com/dropdown")

print("===== TEST DROPDOWN =====")

# Tìm dropdown
dropdown_element = driver.find_element(By.ID, "dropdown")

# Tạo object Select
dropdown = Select(dropdown_element)

# ===== TEST 1: Verify default =====
selected_option = dropdown.first_selected_option.text
print("Default:", selected_option)

assert selected_option == "Please select an option"
print("PASS: Default value correct")

# ===== TEST 2: Select Option 1 =====
dropdown.select_by_visible_text("Option 1")

selected_option = dropdown.first_selected_option.text
print("Selected:", selected_option)

assert selected_option == "Option 1"
print("PASS: Select Option 1")

# ===== TEST 3: Select Option 2 =====
dropdown.select_by_value("2")

selected_option = dropdown.first_selected_option.text
print("Selected:", selected_option)

assert selected_option == "Option 2"
print("PASS: Select Option 2")

# ===== TEST 4: Select bằng index =====
dropdown.select_by_index(1)  # Option 1

selected_option = dropdown.first_selected_option.text
assert selected_option == "Option 1"

print("PASS: Select by index")

# ===== TEST 5: Verify total options =====
options = dropdown.options
print("Total options:", len(options))

assert len(options) == 3
print("PASS: Correct number of options")

driver.quit()