import unittest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize logger / Khởi tạo logger
logger = logging.getLogger(__name__)

class TestIFrame(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/iframe"

    def tearDown(self):
        self.driver.quit()

    def test_tc1_iframe_text_input(self):
        """TC1: Switch into the iFrame, set TinyMCE content via JS, and verify."""
        logger.info(f"Step 1: Navigating to iFrame page / Điều hướng tới trang iFrame")
        self.driver.get(self.url)
        
        logger.info("Step 2: Switching context into the iframe / Chuyển ngữ cảnh vào iframe")
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        logger.info("Step 3: Locating the TinyMCE body / Xác định body của TinyMCE")
        editor_body = self.wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
        
        # ACTION: Use JS to set the innerHTML directly
        # HÀNH ĐỘNG: Dùng JS để thiết lập trực tiếp innerHTML
        test_payload = "Standard Selenium Frame Input Test"
        logger.info(f"Step 4: Injecting payload via JS / Bơm payload qua JS: {test_payload}")
        self.driver.execute_script("arguments[0].innerHTML = arguments[1];", editor_body, test_payload)
        
        # Verify the content / Xác minh nội dung
        # We use innerText to ensure we get the rendered string
        # Dùng innerText để đảm bảo lấy đúng chuỗi đã render
        actual_text = self.driver.execute_script("return arguments[0].innerText;", editor_body).strip()
        logger.info(f"Step 5: Verifying text. Expected: '{test_payload}', Actual: '{actual_text}'")
        
        self.assertEqual(actual_text, test_payload, "Result: Content mismatch / Kết quả: Nội dung không khớp")
        
        # Switch back / Quay lại context mặc định
        self.driver.switch_to.default_content()
        logger.info("Step 6: Returned to main document / Đã quay lại document chính")

if __name__ == "__main__":
    unittest.main()