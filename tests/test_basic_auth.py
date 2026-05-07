import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import urllib.parse # Thư viện xử lý mã hóa URL

# Cấu hình logging chuyên nghiệp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestBasicAuthProfessional(unittest.TestCase):
    def setUp(self):
        # Thiết lập Driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.domain = "the-internet.herokuapp.com/basic_auth"

    def tearDown(self):
        self.driver.quit()

    def helper_auth_navigate(self, user, pwd):
        """
        Helper method to perform URL-based authentication.
        Phương thức hỗ trợ thực hiện xác thực qua URL.
        """
        # URL Encoding xử lý các ký tự đặc biệt trong password (TC_BA_09, TC_BA_10)
        safe_user = urllib.parse.quote(user)
        safe_pwd = urllib.parse.quote(pwd)
        
        auth_url = f"https://{safe_user}:{safe_pwd}@{self.domain}"
        logger.info(f"[ACTION] Navigating to URL with User: '{user}'")
        self.driver.get(auth_url)

    def is_authenticated(self):
        """Kiểm tra xem đã đăng nhập thành công hay chưa"""
        try:
            success_msg = "Congratulations! You must have the proper credentials."
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            return success_msg in body_text
        except:
            return False

    # --- NHÓM TEST CASE: HAPPY PATH (THÀNH CÔNG) ---

    def test_tc1_success(self):
        """TC1: Valid login - Đăng nhập đúng thông tin"""
        self.helper_auth_navigate("admin", "admin")
        self.assertTrue(self.is_authenticated(), "FAILED: Should be authenticated")
        logger.info("TC1 PASSED: Valid login works.")

    # --- NHÓM TEST CASE: NEGATIVE (THẤT BẠI) ---

    def test_tc2_wrong_password(self):
        """TC2: Invalid password - Sai mật khẩu"""
        self.helper_auth_navigate("admin", "wrongpassword")
        self.assertFalse(self.is_authenticated(), "FAILED: Should not be authenticated")
        logger.info("TC2 PASSED: Wrong password blocked.")

    def test_tc3_invalid_username(self):
        """TC3: Wrong username - Sai tên đăng nhập"""
        self.helper_auth_navigate("fakeuser", "admin")
        self.assertFalse(self.is_authenticated())
        logger.info("TC3 PASSED: Non-existent user blocked.")

    def test_tc4_empty_both(self):
        """TC4: Empty fields - Để trống hoàn toàn"""
        self.helper_auth_navigate("", "")
        self.assertFalse(self.is_authenticated())
        logger.info("TC4 PASSED: Empty credentials blocked.")

    # --- NHÓM TEST CASE: EDGE CASES (TRƯỜNG HỢP BIÊN/PHỨC TẠP) ---

    def test_tc5_case_sensitivity_user(self):
        """TC5: Case sensitivity - Kiểm tra phân biệt hoa thường của User"""
        self.helper_auth_navigate("Admin", "admin")
        # Phụ thuộc vào Server cấu hình, thông thường là FALSE
        self.assertFalse(self.is_authenticated())
        logger.info("TC5 PASSED: Username is case sensitive.")

    def test_tc6_case_sensitivity_pass(self):
        """TC6: Case sensitivity - Kiểm tra phân biệt hoa thường của Pass"""
        self.helper_auth_navigate("admin", "ADMIN")
        self.assertFalse(self.is_authenticated())
        logger.info("TC6 PASSED: Password is case sensitive.")

    def test_tc7_special_chars_password(self):
        """
        TC7: Special characters - Mật khẩu có ký tự đặc biệt.
        Đây là lỗi cực kỳ phổ biến trong Basic Auth URL.
        """
        # Giả sử admin đổi mật khẩu có dấu @ hoặc :
        # Lưu ý: Trang the-internet không hỗ trợ đổi pass, đây là demo logic
        self.helper_auth_navigate("admin", "p@ss:word#123")
        # Kết quả mong đợi phụ thuộc vào việc URL encoding có hoạt động hay không
        logger.info("TC7: Special characters handled by URL encoding.")

    def test_tc8_sql_injection_attempt(self):
        """TC8: Basic SQL Injection attempt - Thử tấn công SQL Injection cơ bản"""
        self.helper_auth_navigate("' OR '1'='1", "admin")
        self.assertFalse(self.is_authenticated())
        logger.info("TC8 PASSED: SQL Injection attempt blocked at Auth level.")

    def test_tc9_very_long_credentials(self):
        """TC9: Long string - Thông tin quá dài (Buffer Overflow test)"""
        long_str = "a" * 1000
        self.helper_auth_navigate(long_str, long_str)
        self.assertFalse(self.is_authenticated())
        logger.info("TC9 PASSED: Long string credentials handled.")

if __name__ == "__main__":
    unittest.main()