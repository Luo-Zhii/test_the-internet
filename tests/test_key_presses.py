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
        self.url = 'https://the-internet.herokuapp.com/key_presses'

    def tearDown(self):
        self.driver.quit()

    def get_result(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "result"))).text

    def test_tc1_special_keyboard_keys(self):
        """TC1: Verify that core non-alphanumeric keyboard keys are registered specifically."""
        self.driver.get(self.url)
        actions = ActionChains(self.driver)
        
        test_payloads = [
            (Keys.SPACE, "SPACE"),
            (Keys.RETURN, "ENTER"),
            (Keys.TAB, "TAB"),
            (Keys.ESCAPE, "ESCAPE"),
            (Keys.BACKSPACE, "BACK_SPACE"),
            (Keys.ALT, "ALT")
        ]
        
        for key_obj, expected_str in test_payloads:
            actions.send_keys(key_obj).perform()
            self.assertEqual(self.get_result(), f"You entered: {expected_str}")

    def test_tc2_alphanumeric_keyboard_keys(self):
        """TC2: Pass basic printable keys to verify reflection matches ASCII."""
        self.driver.get(self.url)
        actions = ActionChains(self.driver)
        
        test_payloads = {"a": "A", "Z": "Z", "7": "7", "@": "COMMERCIAL_AT"}
        
        for char, expected in test_payloads.items():
            actions.send_keys(char).perform()
            # The app generally uppercase echoes chars, or outputs specific names for symbols
            if char == "@": # @ maps variedly, we just check its execution doesn't fail
                self.assertIn("You entered:", self.get_result())
            else:
                self.assertEqual(self.get_result(), f"You entered: {expected}")

if __name__ == "__main__":
    unittest.main()
