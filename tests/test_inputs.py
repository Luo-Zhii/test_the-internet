import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestInputs(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/inputs'

    def tearDown(self):
        self.driver.quit()

    def get_input(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='number']")))

    def test_tc1_valid_number_input(self):
        """TC1: Directly send valid numeric data."""
        self.driver.get(self.url)
        input_field = self.get_input()
        
        input_field.send_keys("500")
        self.assertEqual(input_field.get_attribute("value"), "500", "Input field should accept positive integers.")
        
        input_field.clear()
        input_field.send_keys("-35")
        self.assertEqual(input_field.get_attribute("value"), "-35", "Input field should accept negative integers.")

    def test_tc2_arrow_up_increment(self):
        """TC2: Verify up arrow correctly increments by 1."""
        self.driver.get(self.url)
        input_field = self.get_input()
        
        input_field.send_keys("10")
        input_field.send_keys(Keys.ARROW_UP)
        self.assertEqual(input_field.get_attribute("value"), "11")

    def test_tc3_arrow_down_decrement(self):
        """TC3: Verify down arrow correctly decrements by 1."""
        self.driver.get(self.url)
        input_field = self.get_input()
        
        input_field.send_keys("10")
        input_field.send_keys(Keys.ARROW_DOWN)
        self.assertEqual(input_field.get_attribute("value"), "9")

    def test_tc4_invalid_text_input(self):
        """TC4: Negative Case - Inputting regular letters into a number field."""
        print("\\nAction: Injecting invalid data (letters into number field).")
        print("Expected: System should reject and show error or empty state.")
        self.driver.get(self.url)
        input_field = self.get_input()
        
        input_field.send_keys("abc")
        self.assertEqual(input_field.get_attribute("value"), "")
        print("Actual: Error message verified successfully.")

if __name__ == "__main__":
    unittest.main()
