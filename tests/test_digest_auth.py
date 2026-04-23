import unittest
import logging
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_HOST = "the-internet.herokuapp.com/digest_auth"
SUCCESS_TEXT = "Congratulations! You must have the proper credentials."


class TestDigestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _assert_success_absent(self, timeout: float = 2):
        """Helper: assert the success message does NOT appear within the given timeout."""
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//p[contains(text(),'{SUCCESS_TEXT}')]")
                )
            )
            self.fail("Success message should NOT be present, but it appeared.")
        except TimeoutException:
            logger.info("[OUTPUT] TimeoutException caught – success message correctly absent.")

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Valid credentials (admin:admin)
    # ─────────────────────────────────────────────────────────────────
    def test_digest_auth_happy_path_tc1(self):
        encoded_user = urllib.parse.quote("admin")
        encoded_pass = urllib.parse.quote("admin")
        url = f"https://{encoded_user}:{encoded_pass}@{BASE_HOST}"
        logger.info(f"[INPUT]  TC1 – Navigating with valid credentials. URL: https://admin:admin@{BASE_HOST}")
        self.driver.get(url)

        logger.info("[INPUT]  Waiting for <p> tag containing the success confirmation message.")
        success_p = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//p[contains(text(),'Congratulations')]")
            )
        )

        logger.info(f"[OUTPUT] Success element visible. Text: '{success_p.text}'.")
        self.assertTrue(success_p.is_displayed(), "Success paragraph should be visible.")
        self.assertIn(
            "Congratulations",
            success_p.text,
            f"Expected 'Congratulations' in text. Got: '{success_p.text}'"
        )
        logger.info("[OUTPUT] TC1 PASSED – Digest auth with valid credentials succeeded.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Negative: Invalid password (admin:wrong)
    # ─────────────────────────────────────────────────────────────────
    def test_digest_auth_invalid_creds_tc2(self):
        encoded_user = urllib.parse.quote("admin")
        encoded_pass = urllib.parse.quote("wrong")
        url = f"https://{encoded_user}:{encoded_pass}@{BASE_HOST}"
        logger.info(f"[INPUT]  TC2 – Navigating with INVALID password. URL: https://admin:wrong@{BASE_HOST}")
        self.driver.get(url)

        logger.info("[INPUT]  Asserting success message is absent (2s short-wait).")
        self._assert_success_absent(timeout=2)

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"[INPUT]  Page body text: '{body_text}'.")
        self.assertNotIn(SUCCESS_TEXT, body_text, "Success message must NOT be present with wrong password.")
        logger.info("[OUTPUT] TC2 PASSED – Invalid password correctly denied access.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Security: No credentials in URL
    # ─────────────────────────────────────────────────────────────────
    def test_digest_auth_unauthorized_tc3(self):
        url = f"https://{BASE_HOST}"
        logger.info(f"[INPUT]  TC3 – Navigating WITHOUT credentials. URL: {url}")
        self.driver.get(url)

        logger.info("[INPUT]  Asserting success message is absent (2s short-wait).")
        self._assert_success_absent(timeout=2)

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"[INPUT]  Page body text: '{body_text}'.")
        self.assertNotIn(SUCCESS_TEXT, body_text, "Success message must NOT be present without credentials.")
        logger.info("[OUTPUT] TC3 PASSED – Unauthorized URL correctly denied access.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Robustness: Special characters in password via urllib.parse.quote()
    # ─────────────────────────────────────────────────────────────────
    def test_digest_auth_special_chars_tc4(self):
        username = "admin"
        password = "admin@123"  # Contains special char '@' that must be percent-encoded
        encoded_user = urllib.parse.quote(username, safe="")
        encoded_pass = urllib.parse.quote(password, safe="")
        url = f"https://{encoded_user}:{encoded_pass}@{BASE_HOST}"

        logger.info(f"[INPUT]  TC4 – Testing URL construction with special-char password.")
        logger.info(f"[INPUT]  Raw password: '{password}' → Encoded: '{encoded_pass}'.")
        logger.info(f"[INPUT]  Constructed URL (safe to log): https://admin:{encoded_pass}@{BASE_HOST}")

        # Validate the URL encoding is correct before even navigating
        self.assertIn("%40", encoded_pass, "The '@' character must be percent-encoded as '%40'.")
        logger.info("[OUTPUT] URL encoding assertion passed – '@' correctly encoded as '%40'.")

        logger.info("[INPUT]  Navigating to the constructed URL.")
        self.driver.get(url)

        # The Heroku app does not accept 'admin@123' as a valid password,
        # so we assert the success message is absent as the expected outcome.
        logger.info("[INPUT]  Asserting success message is absent (site does not accept this password).")
        self._assert_success_absent(timeout=2)

        logger.info("[OUTPUT] TC4 PASSED – URL constructed correctly with urllib.parse.quote(); "
                    "special-char password was safely encoded and the invalid credential was properly rejected.")


if __name__ == "__main__":
    unittest.main()
