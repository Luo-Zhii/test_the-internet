import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

BASE_URL = "https://the-internet.herokuapp.com"
REDIRECTOR_URL = f"{BASE_URL}/redirector"
EXPECTED_REDIRECT_URL = f"{BASE_URL}/status_codes"


class TestRedirectLink(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Click redirect link and verify URL changes
    # ─────────────────────────────────────────────────────────────────
    def test_redirect_link_url_change_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Redirector page.")
        self.driver.get(REDIRECTOR_URL)

        logger.info("[INPUT]  Locating the redirect link by href attribute.")
        redirect_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='redirect']"))
        )
        url_before = self.driver.current_url
        logger.info(f"[INPUT]  URL before click: '{url_before}'.")

        redirect_link.click()

        logger.info("[INPUT]  Waiting for URL to change to the redirected destination.")
        self.wait.until(EC.url_contains("status_codes"))

        url_after = self.driver.current_url
        logger.info(f"[OUTPUT] URL after redirect: '{url_after}'.")

        logger.info("[OUTPUT] Asserting URL has changed and matches expected destination.")
        self.assertNotEqual(url_before, url_after, "URL should have changed after redirect.")
        self.assertEqual(
            url_after, EXPECTED_REDIRECT_URL,
            f"Expected redirect to '{EXPECTED_REDIRECT_URL}' but got '{url_after}'"
        )
        logger.info("[OUTPUT] TC1 PASSED – Redirect navigated to Status Codes page successfully.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Verify content on the redirected page
    # ─────────────────────────────────────────────────────────────────
    def test_redirect_link_destination_content_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Redirector page and following redirect.")
        self.driver.get(REDIRECTOR_URL)

        redirect_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='redirect']"))
        )
        redirect_link.click()

        logger.info("[INPUT]  Waiting for redirect destination heading 'Status Codes'.")
        heading = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )
        logger.info(f"[OUTPUT] Destination heading: '{heading.text}'.")

        logger.info("[OUTPUT] Asserting destination page heading contains 'Status Codes'.")
        self.assertIn(
            "Status Codes", heading.text,
            f"Expected 'Status Codes' in heading, got: '{heading.text}'"
        )
        logger.info("[OUTPUT] TC2 PASSED – Redirect destination page content verified.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path: Navigate to invalid redirect endpoint directly
    # ─────────────────────────────────────────────────────────────────
    def test_redirect_invalid_endpoint_tc3(self):
        invalid_url = f"{BASE_URL}/redirect/nonexistent_page_404"
        logger.info(f"[INPUT]  TC3 – Navigating directly to invalid endpoint: '{invalid_url}'.")
        self.driver.get(invalid_url)

        logger.info("[INPUT]  Waiting for page body to load.")
        body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = body.text
        logger.info(f"[OUTPUT] Page body text: '{body_text[:200]}'.")

        logger.info("[OUTPUT] Asserting the success/status-codes page is NOT reached.")
        self.assertNotIn(
            "Status Codes", body_text,
            "Invalid endpoint should not show the Status Codes page."
        )
        logger.info("[OUTPUT] TC3 PASSED – Invalid endpoint correctly did not redirect to Status Codes.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path: Attempt to find redirect link on wrong page
    # ─────────────────────────────────────────────────────────────────
    def test_redirect_link_absent_on_wrong_page_tc4(self):
        wrong_url = f"{BASE_URL}/status_codes"
        logger.info(f"[INPUT]  TC4 – Navigating to wrong page (already-redirected destination): '{wrong_url}'.")
        self.driver.get(wrong_url)

        logger.info("[INPUT]  Attempting to find redirect link (href='redirect') with 2s short-wait.")
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='redirect']"))
            )
            self.fail("Redirect link should NOT exist on the Status Codes destination page.")
        except TimeoutException:
            logger.info("[OUTPUT] TimeoutException caught – redirect link correctly absent on destination page.")

        logger.info("[OUTPUT] TC4 PASSED – Redirect link not present on wrong/destination page.")


if __name__ == "__main__":
    unittest.main()
