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
        self.url = "https://the-internet.herokuapp.com/dropdown"

    def tearDown(self):
        self.driver.quit()

    def get_dropdown(self):
        """Helper to get the dropdown select element."""
        element = self.wait.until(EC.visibility_of_element_located((By.ID, "dropdown")))
        return Select(element)

    def test_tc1_default_placeholder(self):
        """TC1: Default Option should be 'Please select an option' and it should be disabled."""
        self.driver.get(self.url)
        dropdown = self.get_dropdown()
        
        self.assertEqual(len(dropdown.options), 3, "Dropdown should have 3 options.")
        first_option = dropdown.first_selected_option
        self.assertEqual(first_option.text, "Please select an option", "Default text incorrect.")
        self.assertFalse(first_option.is_enabled(), "The placeholder should be disabled from manual selection.")

    def test_tc2_select_option_1(self):
        """TC2: Select Option 1 by index and verify."""
        self.driver.get(self.url)
        dropdown = self.get_dropdown()
        
        dropdown.select_by_index(1)
        self.assertEqual(dropdown.first_selected_option.text, "Option 1")

    def test_tc3_select_option_2(self):
        """TC3: Select Option 2 by visible text and verify."""
        self.driver.get(self.url)
        dropdown = self.get_dropdown()
        
        dropdown.select_by_visible_text("Option 2")
        self.assertEqual(dropdown.first_selected_option.text, "Option 2")

    def test_tc4_switch_between_options(self):
        """TC4: Validate that switching from an option accurately overrides the previous."""
        self.driver.get(self.url)
        dropdown = self.get_dropdown()
        
        dropdown.select_by_value("1")
        self.assertEqual(dropdown.first_selected_option.text, "Option 1")
        
        dropdown.select_by_value("2")
        self.assertEqual(dropdown.first_selected_option.text, "Option 2")

if __name__ == "__main__":
    unittest.main()
