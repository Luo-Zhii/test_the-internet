import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestFloatingMenu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/floating_menu'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_menu_visible_top(self):
        """TC1: Verify that the menu is visible at the very top on initial load."""
        self.driver.get(self.url)
        menu = self.wait.until(EC.visibility_of_element_located((By.ID, "menu")))
        self.assertTrue(menu.is_displayed(), "Menu should be visible initially.")

    def test_tc2_menu_visible_on_scroll(self):
        """TC2: Ensure the menu 'floats' securely and remains visible even on bottom scroll."""
        self.driver.get(self.url)
        menu = self.wait.until(EC.visibility_of_element_located((By.ID, "menu")))
        
        # Execute heavy scroll to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Ensure it is still technically "displayed" viewport-wise
        self.assertTrue(menu.is_displayed(), "Menu should float and stay visible.")
        
        # Ensure deep child links are interactable
        home_link = self.driver.find_element(By.LINK_TEXT, "Home")
        about_link = self.driver.find_element(By.LINK_TEXT, "About")
        
        self.assertTrue(home_link.is_displayed() and about_link.is_displayed())

    def test_tc3_menu_anchor_links_work(self):
        """TC3: Click one of the floating links and ensure it triggers hash navigation correctly."""
        self.driver.get(self.url)
        home_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
        home_link.click()
        
        self.assertIn("#home", self.driver.current_url, "Clicking 'Home' link should alter the anchor URL hash.")

if __name__ == "__main__":
    unittest.main()
