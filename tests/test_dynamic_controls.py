import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestDynamicControls(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def tearDown(self):
        self.driver.quit()

    def test_checkbox_remove_and_add(self):
        self.driver.get('https://the-internet.herokuapp.com/dynamic_controls')
        
        # Remove Checkbox
        remove_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkbox-example > button")))
        remove_btn.click()
        
        # Wait for "It's gone!" message
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's gone!")
        
        # Verify checkbox is gone
        self.wait.until(EC.invisibility_of_element_located((By.ID, "checkbox")))
        
        # Add Checkbox
        add_btn = self.driver.find_element(By.CSS_SELECTOR, "#checkbox-example > button")
        add_btn.click()
        
        # Wait for "It's back!" message
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's back!")
        
        # Verify checkbox is present
        self.wait.until(EC.presence_of_element_located((By.ID, "checkbox")))

    def test_input_enable_and_disable(self):
        self.driver.get('https://the-internet.herokuapp.com/dynamic_controls')
        
        input_field = self.driver.find_element(By.CSS_SELECTOR, "#input-example > input")
        enable_btn = self.driver.find_element(By.CSS_SELECTOR, "#input-example > button")
        
        # Initial state
        self.assertFalse(input_field.is_enabled())
        
        # Enable
        enable_btn.click()
        self.wait.until(EC.element_to_be_clickable(input_field))
        
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's enabled!")
        self.assertTrue(input_field.is_enabled())
        
        # Disable
        disable_btn = self.driver.find_element(By.CSS_SELECTOR, "#input-example > button")
        disable_btn.click()
        self.wait.until(lambda d: not input_field.is_enabled())
        
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's disabled!")
        self.assertFalse(input_field.is_enabled())

if __name__ == "__main__":
    unittest.main()
