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

    def tearDown(self):
        self.driver.quit()

    def test_floating_menu_visibility_on_scroll(self):
        self.driver.get('https://the-internet.herokuapp.com/floating_menu')
        
        # Verify menu is visible initially
        menu = self.wait.until(EC.visibility_of_element_located((By.ID, "menu")))
        self.assertTrue(menu.is_displayed())
        
        # Scroll down
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Verify menu is still visible (floating)
        self.assertTrue(menu.is_displayed())
        
        # Verify a specific menu item is clickable after scroll
        home_link = self.driver.find_element(By.LINK_TEXT, "Home")
        self.assertTrue(home_link.is_displayed())

if __name__ == "__main__":
    unittest.main()
