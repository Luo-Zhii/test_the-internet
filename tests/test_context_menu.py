import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException # Imported for robust exception handling
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestContextMenu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        # Explicit wait setup / Thiết lập chờ đợi rõ ràng
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/context_menu'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_context_menu_success_and_cleanup(self):
        """
        TC1: Right-click triggers JS alert & ensures cleanup.
        TC1: Click chuột phải kích hoạt cảnh báo JS & đảm bảo dọn dẹp trạng thái.
        """
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        
        # Perform right click / Thực hiện click chuột phải
        actions = ActionChains(self.driver)
        actions.context_click(hot_spot).perform()
        
        # Verify alert presence / Xác minh sự hiện diện của cảnh báo
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        
        # Use try-finally for Fail-Safe strategy (Lý thuyết trò chơi: An toàn khi thất bại)
        try:
            self.assertEqual(alert.text, "You selected a context menu", "Alert text does not match expected output.")
        finally:
            # This line ALWAYS runs, even if assertEqual fails, preventing Deadlock.
            # Dòng này LUÔN LUÔN chạy, ngay cả khi kiểm tra thất bại, ngăn chặn Treo hệ thống.
            alert.accept()

    def test_tc2_left_click_ignores_menu(self):
        """
        TC2: Verify that standard left click does not trigger the alert.
        TC2: Xác minh rằng click chuột trái tiêu chuẩn không kích hoạt cảnh báo.
        """
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        
        # Perform standard left click / Thực hiện click chuột trái
        actions = ActionChains(self.driver)
        actions.click(hot_spot).perform()
        
        # Wait up to 2 seconds to fail fast / Chờ tối đa 2 giây để báo lỗi nhanh
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.alert_is_present())
            self.fail("FAILED: Alert incorrectly triggered on left-click.")
        except TimeoutException:
            # TimeoutException is expected here, meaning no alert appeared.
            # Lỗi TimeoutException được mong đợi ở đây, nghĩa là không có cảnh báo nào xuất hiện.
            self.assertTrue(True, "Successfully confirmed alert does not appear on left click.")

    def test_tc3_boundary_click_outside_hotspot(self):
        """
        TC3: Boundary Test - Right click OUTSIDE the box should NOT trigger alert.
        TC3: Kiểm thử Ranh giới - Click chuột phải BÊN NGOÀI hộp KHÔNG ĐƯỢC kích hoạt cảnh báo.
        """
        self.driver.get(self.url)
        
        # Locate an element outside the box (e.g., the page header)
        # Tìm một phần tử nằm ngoài hộp (ví dụ: tiêu đề trang)
        outside_element = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        
        # Perform right click on the outside element / Click chuột phải vào phần tử bên ngoài
        actions = ActionChains(self.driver)
        actions.context_click(outside_element).perform()
        
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.alert_is_present())
            # If an alert pops up, it means the developer wrote a global event listener by mistake.
            # Nếu cảnh báo hiện lên, nghĩa là lập trình viên đã viết nhầm bộ lắng nghe sự kiện toàn cục.
            alert = self.driver.switch_to.alert
            alert.accept() # Clean up before failing / Dọn dẹp trước khi đánh rớt
            self.fail("FAILED: Alert triggered when clicking outside the designated hotspot.")
        except TimeoutException:
            self.assertTrue(True, "Boundary test passed: No alert triggered outside the hotspot.")

if __name__ == "__main__":
    unittest.main()