import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestKeyPresses(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_special_key_presses(self):
        self.driver.get('https://the-internet.herokuapp.com/key_presses')
        
        test_keys = [
            (Keys.SPACE, "SPACE"),
            (Keys.RETURN, "ENTER"),
            (Keys.TAB, "TAB"),
            (Keys.ESCAPE, "ESCAPE"),
            (Keys.BACKSPACE, "BACK_SPACE")
        ]
        
        actions = ActionChains(self.driver)
        for key, expected_name in test_keys:
            actions.send_keys(key).perform()
            # Wait for result to be visible AFTER sending the key
            result_text = self.wait.until(EC.visibility_of_element_located((By.ID, "result")))
            self.assertEqual(f"You entered: {expected_name}", result_text.text)

    def test_alphanumeric_key_presses(self):
        self.driver.get('https://the-internet.herokuapp.com/key_presses')
        
        test_chars = ["A", "z", "5"]
        
        actions = ActionChains(self.driver)
        for char in test_chars:
            actions.send_keys(char).perform()
            # Wait for result to be visible AFTER sending the key
            result_text = self.wait.until(EC.visibility_of_element_located((By.ID, "result")))
            self.assertEqual(f"You entered: {char.upper()}", result_text.text)

if __name__ == "__main__":
    unittest.main()
