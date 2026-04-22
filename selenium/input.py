from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_inputs():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        driver.get("https://the-internet.herokuapp.com/inputs")
        time.sleep(1)

        input_field = driver.find_element(By.CSS_SELECTOR, "input[type='number']")

        # TC1: Nhập số hợp lệ
        print("=== TC1: Nhập số hợp lệ ===")
        input_field.clear()
        input_field.send_keys("123")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: 123 | Giá trị hiển thị: {value}")
        assert value == "123", f"FAIL: Expected '123', got '{value}'"
        print("PASS")

        # TC2: Nhập số âm
        print("\n=== TC2: Nhập số âm ===")
        input_field.clear()
        input_field.send_keys("-50")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: -50 | Giá trị hiển thị: {value}")
        assert value == "-50", f"FAIL: Expected '-50', got '{value}'"
        print("PASS")

        # TC3: Nhập số thập phân
        print("\n=== TC3: Nhập số thập phân ===")
        input_field.clear()
        input_field.send_keys("3.14")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: 3.14 | Giá trị hiển thị: {value}")
        assert value == "3.14", f"FAIL: Expected '3.14', got '{value}'"
        print("PASS")

        # TC4: Nhập chữ cái (không hợp lệ)
        print("\n=== TC4: Nhập chữ cái (không hợp lệ) ===")
        input_field.clear()
        input_field.send_keys("abc")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: abc | Giá trị hiển thị: '{value}'")
        assert value == "", f"FAIL: Expected '', got '{value}'"
        print("PASS - Input bị chặn, không nhận chữ cái")

        # TC5: Nhập ký tự đặc biệt
        print("\n=== TC5: Nhập ký tự đặc biệt ===")
        input_field.clear()
        input_field.send_keys("!@#$")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: !@#$ | Giá trị hiển thị: '{value}'")
        assert value == "", f"FAIL: Expected '', got '{value}'"
        print("PASS - Input bị chặn, không nhận ký tự đặc biệt")

        # TC6: Nhập số rất lớn
        print("\n=== TC6: Nhập số rất lớn ===")
        input_field.clear()
        input_field.send_keys("999999999999")
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị nhập: 999999999999 | Giá trị hiển thị: {value}")
        assert value == "999999999999", f"FAIL: Expected '999999999999', got '{value}'"
        print("PASS")

        # TC7: Để trống
        print("\n=== TC7: Để trống ===")
        input_field.clear()
        time.sleep(1)
        value = input_field.get_attribute("value")
        print(f"Giá trị khi để trống: '{value}'")
        assert value == "", f"FAIL: Expected '', got '{value}'"
        print("PASS")

    except AssertionError as e:
        print(f"❌ {e}")

    finally:
        time.sleep(2)
        driver.quit()


test_inputs()