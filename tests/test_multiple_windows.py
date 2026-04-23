import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

logger = logging.getLogger(__name__)

class TestMultipleWindows(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/windows"

    def tearDown(self):
        self.driver.quit()

    def test_multiple_windows_switch_happy_path_tc1(self):
        self.driver.get(self.url)
        original_window = self.driver.current_window_handle
        
        logger.info("[INPUT] Clicking link to open new window.")
        self.driver.find_element(By.LINK_TEXT, "Click Here").click()
        
        # Đợi cho đến khi có đúng 2 tab (Cực kỳ quan trọng để tránh Flaky)
        self.wait.until(EC.number_of_windows_to_be(2))
        
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                logger.info("[INPUT] Switching context to New Window.")
                self.driver.switch_to.window(window_handle)
                break
                
        new_text = self.driver.find_element(By.TAG_NAME, "h3").text
        self.assertEqual(new_text, "New Window")
        
        logger.info("[INPUT] Closing New Window and reverting to Original.")
        self.driver.close()
        self.driver.switch_to.window(original_window)
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Click Here").is_displayed())
        logger.info("[OUTPUT] TC1 Passed: Tab lifecycle completed securely.")

    def test_multiple_windows_isolation_sad_path_tc2(self):
        self.driver.get(self.url)
        self.driver.find_element(By.LINK_TEXT, "Click Here").click()
        self.wait.until(EC.number_of_windows_to_be(2))
        
        logger.info("[INPUT] Attempting to read New Window text WITHOUT switching handle.")
        try:
            # Sẽ fail vì driver vẫn đang ở trang cũ
            text = self.driver.find_element(By.XPATH, "//h3[text()='New Window']").text
            self.fail("Context Leak: Driver saw new tab content without switching!")
        except NoSuchElementException:
            logger.info("[OUTPUT] TC2 Passed: Driver strictly isolated to current handle.")

    def test_invalid_window_handle_sad_path_tc3(self):
        self.driver.get(self.url)
        logger.info("[INPUT] Attempting to switch to a ghost window handle.")
        try:
            self.driver.switch_to.window("ghost_tab_999")
            self.fail("Driver switched to a non-existent window!")
        except NoSuchWindowException:
            logger.info("[OUTPUT] TC3 Passed: NoSuchWindowException caught.")

if __name__ == "__main__":
    unittest.main()