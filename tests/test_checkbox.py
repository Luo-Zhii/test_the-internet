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

    def tearDown(self):
        self.driver.quit()

    def test_checkbox_interaction(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        
        # Select checkboxes
        checkbox1 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkboxes"]/input[1]')))
        checkbox2 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkboxes"]/input[2]')))
        
        # Initial check (assuming defaults: checkbox1 is unchecked, checkbox2 is checked)
        if not checkbox1.is_selected():
            checkbox1.click()
        
        if checkbox2.is_selected():
            checkbox2.click()
            
        # Verify states
        self.assertTrue(checkbox1.is_selected(), "Checkbox 1 should be selected")
        self.assertFalse(checkbox2.is_selected(), "Checkbox 2 should not be selected")
        
        # Click checkbox1 again
        checkbox1.click()
        self.assertFalse(checkbox1.is_selected(), "Checkbox 1 should now be unselected")

if __name__ == "__main__":
    unittest.main()
