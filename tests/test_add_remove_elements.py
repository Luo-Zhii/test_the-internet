import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestAddRemoveElements(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_add_remove_multiple_elements(self):
        self.driver.get('https://the-internet.herokuapp.com/add_remove_elements/')
        
        add_button_locator = (By.XPATH, "//button[text()='Add Element']")
        add_button = self.wait.until(EC.element_to_be_clickable(add_button_locator))
        
        # Add 10 elements
        for _ in range(10):
            add_button.click()
            
        # Verify 10 elements were added
        remove_buttons_locator = (By.CLASS_NAME, "added-manually")
        self.wait.until(EC.presence_of_all_elements_located(remove_buttons_locator))
        remove_buttons = self.driver.find_elements(*remove_buttons_locator)
        self.assertEqual(len(remove_buttons), 10)
        
        # Remove 8 elements
        for i in range(8):
            remove_buttons[i].click()
            
        # Verify 2 elements remain
        remaining_elements = self.driver.find_elements(*remove_buttons_locator)
        self.assertEqual(len(remaining_elements), 2)

if __name__ == "__main__":
    unittest.main()
