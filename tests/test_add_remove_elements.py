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
        self.url = "https://the-internet.herokuapp.com/add_remove_elements/"

    def tearDown(self):
        self.driver.quit()

    def get_delete_buttons(self):
        """Helper method to return all currently visible delete buttons."""
        try:
            return self.driver.find_elements(By.CLASS_NAME, "added-manually")
        except:
            return []

    def test_tc1_add_single_element(self):
        """TC1: Add a single element and verify it appears."""
        self.driver.get(self.url)
        add_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        add_btn.click()
        
        delete_btns = self.get_delete_buttons()
        self.assertEqual(len(delete_btns), 1, "Exactly 1 delete button should exist.")
        self.assertTrue(delete_btns[0].is_displayed(), "Delete button should be visible.")

    def test_tc2_remove_single_element(self):
        """TC2: Add a single element, then remove it."""
        self.driver.get(self.url)
        add_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        add_btn.click()
        
        delete_btns = self.get_delete_buttons()
        delete_btn = delete_btns[0]
        delete_btn.click()
        
        # Explicitly wait for staleness to ensure DOM is updated
        self.wait.until(EC.staleness_of(delete_btn))
        
        remaining_btns = self.get_delete_buttons()
        self.assertEqual(len(remaining_btns), 0, "No delete buttons should exist.")

    def test_tc3_add_multiple_elements(self):
        """TC3: Add multiple elements in succession to test dynamic DOM generation."""
        self.driver.get(self.url)
        add_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        
        for _ in range(5):
            add_btn.click()
            
        delete_btns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "added-manually")))
        self.assertEqual(len(delete_btns), 5, "Exactly 5 delete buttons should exist.")

    def test_tc4_remove_all_elements_dynamically(self):
        """TC4: Empty state boundary case - remove all elements one by one until none are left."""
        self.driver.get(self.url)
        add_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
        
        for _ in range(3):
            add_btn.click()
            
        delete_btns = self.driver.find_elements(By.CLASS_NAME, "added-manually")
        
        for btn in delete_btns:
            btn.click()
            self.wait.until(EC.staleness_of(btn))
            
        remaining_btns = self.get_delete_buttons()
        self.assertEqual(len(remaining_btns), 0, "All added elements should be completely removed.")

if __name__ == "__main__":
    unittest.main()
