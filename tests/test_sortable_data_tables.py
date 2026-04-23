import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/tables"


class TestSortableDataTables(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _get_column_values(self, table_id: str, col_index: int) -> list:
        """Extract all body-row values from a specific column (1-indexed)."""
        rows = self.driver.find_elements(
            By.XPATH, f"//table[@id='{table_id}']/tbody/tr/td[{col_index}]"
        )
        values = [r.text.strip() for r in rows]
        logger.info(f"[INPUT]  Extracted {len(values)} values from table#{table_id} col {col_index}: {values}")
        return values

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Sort 'Last Name' column ASC and verify order
    # ─────────────────────────────────────────────────────────────────
    def test_sortable_tables_sort_lastname_asc_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Sortable Data Tables page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for Table 1 to be present.")
        self.wait.until(EC.presence_of_element_located((By.ID, "table1")))

        logger.info("[INPUT]  Clicking 'Last Name' column header to sort ASC.")
        lastname_header = self.driver.find_element(
            By.XPATH, "//table[@id='table1']//th[span[text()='Last Name']]"
        )
        lastname_header.click()

        actual = self._get_column_values("table1", col_index=1)
        expected_sorted = sorted(actual)
        logger.info(f"[OUTPUT] Actual order:   {actual}")
        logger.info(f"[OUTPUT] Expected (ASC): {expected_sorted}")

        self.assertEqual(actual, expected_sorted, "Last Name column should be sorted ASC after one click.")
        logger.info("[OUTPUT] TC1 PASSED – Last Name column sorted ASC correctly.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Sort 'Last Name' DESC (second click reverses order)
    # ─────────────────────────────────────────────────────────────────
    def test_sortable_tables_sort_lastname_desc_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Sortable Data Tables page.")
        self.driver.get(URL)

        self.wait.until(EC.presence_of_element_located((By.ID, "table1")))

        lastname_header = self.driver.find_element(
            By.XPATH, "//table[@id='table1']//th[span[text()='Last Name']]"
        )
        logger.info("[INPUT]  Clicking 'Last Name' header twice to sort DESC.")
        lastname_header.click()  # ASC
        lastname_header.click()  # DESC

        actual = self._get_column_values("table1", col_index=1)
        expected_sorted_desc = sorted(actual, reverse=True)
        logger.info(f"[OUTPUT] Actual order:    {actual}")
        logger.info(f"[OUTPUT] Expected (DESC): {expected_sorted_desc}")

        self.assertEqual(actual, expected_sorted_desc, "Last Name column should be sorted DESC after two clicks.")
        logger.info("[OUTPUT] TC2 PASSED – Last Name column sorted DESC correctly.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Boundary: Table 2 'Email' header IS sortable — verify sort works
    # ─────────────────────────────────────────────────────────────────
    def test_sortable_tables_unsortable_column_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Sortable Data Tables page.")
        self.driver.get(URL)

        self.wait.until(EC.presence_of_element_located((By.ID, "table2")))

        logger.info("[INPUT]  Clicking Table 2 'Email' column header to sort.")
        email_header = self.driver.find_element(
            By.XPATH, "//table[@id='table2']//th[span[text()='Email']]"
        )
        email_header.click()

        values_after = self._get_column_values("table2", col_index=3)
        logger.info(f"[OUTPUT] Email column values after click: {values_after}.")

        logger.info("[OUTPUT] Asserting email column has values (sort mechanism engaged).")
        self.assertGreater(
            len(values_after), 0,
            "Table 2 Email column should have data rows after sort click."
        )
        expected_sorted = sorted(values_after)
        self.assertEqual(
            values_after, expected_sorted,
            f"Email column should be ASC-sorted after click. Got: {values_after}"
        )
        logger.info("[OUTPUT] TC3 PASSED – Table 2 Email column sorts correctly.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path: Attempting to access a non-existent column index
    # ─────────────────────────────────────────────────────────────────
    def test_sortable_tables_out_of_bounds_column_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to Sortable Data Tables page.")
        self.driver.get(URL)

        self.wait.until(EC.presence_of_element_located((By.ID, "table1")))

        logger.info("[INPUT]  Attempting to extract column 99 (out of bounds) from Table 1.")
        values = self._get_column_values("table1", col_index=99)
        logger.info(f"[OUTPUT] Values returned for column 99: {values}")

        logger.info("[OUTPUT] Asserting out-of-bounds column returns an empty list (graceful no-match).")
        self.assertEqual(
            values, [],
            f"Out-of-bounds column 99 should return empty list, got: {values}"
        )
        logger.info("[OUTPUT] TC4 PASSED – Out-of-bounds column index gracefully returns empty result.")


if __name__ == "__main__":
    unittest.main()
