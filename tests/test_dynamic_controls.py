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
        self.url = 'https://the-internet.herokuapp.com/dynamic_controls'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_checkbox_removal(self):
        """TC1: Wait for a checkbox to be removed from the DOM via click event."""
        self.driver.get(self.url)
        checkbox = self.wait.until(EC.presence_of_element_located((By.ID, "checkbox")))
        remove_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkbox-example > button")))
        
        remove_btn.click()
        self.wait.until(EC.staleness_of(checkbox))
        
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's gone!")
        self.assertEqual(len(self.driver.find_elements(By.ID, "checkbox")), 0)

    def test_tc2_checkbox_addition(self):
        """TC2: Remove checkbox first, then click Add, and verify DOM inclusion."""
        self.driver.get(self.url)
        # Remove it first
        self.driver.find_element(By.CSS_SELECTOR, "#checkbox-example > button").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        
        # Add it back
        add_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkbox-example > button")))
        add_btn.click()
        
        checkbox = self.wait.until(EC.presence_of_element_located((By.ID, "checkbox")))
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        
        self.assertEqual(msg.text, "It's back!")
        self.assertTrue(checkbox.is_displayed())

    def test_tc3_input_enable(self):
        """TC3: Ensure disabled input field becomes enabled after clicking Enable."""
        self.driver.get(self.url)
        input_field = self.driver.find_element(By.CSS_SELECTOR, "#input-example > input")
        enable_btn = self.driver.find_element(By.CSS_SELECTOR, "#input-example > button")
        
        self.assertFalse(input_field.is_enabled(), "Input must be initially disabled.")
        
        enable_btn.click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#input-example > input")))
        
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "It's enabled!")
        self.assertTrue(input_field.is_enabled())

    def test_tc4_input_disable(self):
        """TC4: Input field can be disabled again if currently enabled."""
        self.driver.get(self.url)
        input_field = self.driver.find_element(By.CSS_SELECTOR, "#input-example > input")
        
        # Enable it first
        self.driver.find_element(By.CSS_SELECTOR, "#input-example > button").click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#input-example > input")))
        
        # Disable it
        disable_btn = self.driver.find_element(By.CSS_SELECTOR, "#input-example > button")
        disable_btn.click()
        
        # Wait until it is no longer enabled
        self.wait.until(lambda d: not input_field.is_enabled())
        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        
        self.assertEqual(msg.text, "It's disabled!")
        self.assertFalse(input_field.is_enabled())

if __name__ == "__main__":
    unittest.main()
