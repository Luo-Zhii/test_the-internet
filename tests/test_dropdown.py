import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestDropdown(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_dropdown_selection(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        
        dropdown_element = self.wait.until(EC.visibility_of_element_located((By.ID, "dropdown")))
        dropdown = Select(dropdown_element)
        
        # Verify initial state/options count
        self.assertEqual(len(dropdown.options), 3, "Dropdown should have 3 options including placeholder")
        
        # Select Option 1
        dropdown.select_by_index(1)
        self.assertEqual(dropdown.first_selected_option.text, "Option 1")
        
        # Select Option 2
        dropdown.select_by_visible_text("Option 2")
        self.assertEqual(dropdown.first_selected_option.text, "Option 2")

if __name__ == "__main__":
    unittest.main()
