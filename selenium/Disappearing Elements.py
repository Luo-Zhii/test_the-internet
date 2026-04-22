from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_disappearing_elements():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get("https://the-internet.herokuapp.com/disappearing_elements")

        menu_before = driver.find_elements(By.CSS_SELECTOR, "ul li a")
        menu_before_texts = [item.text for item in menu_before]

        print(f"Số menu hiện tại: {len(menu_before_texts)}")
        for text in menu_before_texts:
            print(text)

        driver.refresh()
        time.sleep(2)
        
        menu_after = driver.find_elements(By.CSS_SELECTOR, "ul li a")
        menu_after_texts = [item.text for item in menu_after]

        print(f"Số menu sau khi refresh: {len(menu_after_texts)}")
        for text in menu_after_texts:
            print(text)

        for text in menu_after_texts:
            if text not in menu_before_texts:
                print(f"Menu mới xuất hiện: {text}")
        
        for text in menu_before_texts:
            if text not in menu_after_texts:
                print(f"Menu biến mất: {text}")
        
    finally:
        time.sleep(2)
        driver.quit()


test_disappearing_elements()