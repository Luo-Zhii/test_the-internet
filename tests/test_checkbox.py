import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestCheckbox(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/checkboxes"

    def tearDown(self):
        self.driver.quit()
        
    def get_checkbox(self, index):
        """Helper to get a checkbox by its index (1-based)."""
        xpath = f'//*[@id="checkboxes"]/input[{index}]'
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def test_tc1_default_state_validation(self):
        """TC1: Verify the default state: Checkbox 1 is unchecked and Checkbox 2 is checked."""
        self.driver.get(self.url)
        cb1 = self.get_checkbox(1)
        cb2 = self.get_checkbox(2)
        
        self.assertFalse(cb1.is_selected(), "Checkbox 1 should be unchecked by default.")
        self.assertTrue(cb2.is_selected(), "Checkbox 2 should be checked by default.")

    def test_tc2_check_first_checkbox(self):
        """TC2: Check the initially unchecked checkbox."""
        self.driver.get(self.url)
        cb1 = self.get_checkbox(1)
        
        if not cb1.is_selected():
            cb1.click()
            
        self.assertTrue(cb1.is_selected(), "Checkbox 1 should be successfully checked.")

    def test_tc3_uncheck_second_checkbox(self):
        """TC3: Uncheck the initially checked checkbox."""
        self.driver.get(self.url)
        cb2 = self.get_checkbox(2)
        
        if cb2.is_selected():
            cb2.click()
            
        self.assertFalse(cb2.is_selected(), "Checkbox 2 should be successfully unchecked.")

    def test_tc4_toggle_both_checkboxes(self):
        """TC4: Stress test - continuously toggle states to determine boolean reliability."""
        self.driver.get(self.url)
        cb1 = self.get_checkbox(1)
        cb2 = self.get_checkbox(2)
        
        # Toggle CB 1
        cb1.click()
        self.assertTrue(cb1.is_selected())
        cb1.click()
        self.assertFalse(cb1.is_selected())
        
        # Toggle CB 2
        cb2.click()
        self.assertFalse(cb2.is_selected())
        cb2.click()
        self.assertTrue(cb2.is_selected())

if __name__ == "__main__":
    unittest.main()
