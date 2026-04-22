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

    def tearDown(self):
        self.driver.quit()

    def test_number_input_field(self):
        self.driver.get('https://the-internet.herokuapp.com/inputs')
        
        input_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
        
        # Test direct entry
        test_value = "123456"
        input_field.send_keys(test_value)
        self.assertEqual(input_field.get_attribute("value"), test_value)
        
        # Test increment via keyboard
        input_field.send_keys(Keys.ARROW_UP)
        self.assertEqual(input_field.get_attribute("value"), str(int(test_value) + 1))
        
        # Test decrement via keyboard
        input_field.send_keys(Keys.ARROW_DOWN)
        self.assertEqual(input_field.get_attribute("value"), test_value)

if __name__ == "__main__":
    unittest.main()
