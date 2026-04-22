import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestDragAndDrop(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/drag_and_drop"

    def tearDown(self):
        self.driver.quit()

    def helper_html5_drag_and_drop(self, source, target):
        """Helper to bypass WebDriver's poor HTML5 drag/drop ActionChain support by injecting dynamic JS."""
        js_drag_and_drop = """
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function (key, value) { this.data[key] = value; },
                getData: function (key) { return this.data[key]; }
            };
            return event;
        }

        function dispatchEvent(element, event, transferData) {
            if (transferData !== undefined) {
                event.dataTransfer = transferData;
            }
            if (element.dispatchEvent) {
                element.dispatchEvent(event);
            } else if (element.fireEvent) {
                element.fireEvent("on" + event.type, event);
            }
        }

        function simulateHTML5DragAndDrop(element, destination) {
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(element, dragStartEvent);
            var dropEvent = createEvent('drop');
            dispatchEvent(destination, dropEvent, dragStartEvent.dataTransfer);
            var dragEndEvent = createEvent('dragend');
            dispatchEvent(element, dragEndEvent, dropEvent.dataTransfer);
        }

        var source = arguments[0];
        var destination = arguments[1];
        simulateHTML5DragAndDrop(source, destination);
        """
        self.driver.execute_script(js_drag_and_drop, source, target)

    def test_tc1_drag_a_to_b(self):
        """TC1: Drag Block A over to Block B and verify swap."""
        self.driver.get(self.url)
        col_a = self.wait.until(EC.presence_of_element_located((By.ID, "column-a")))
        col_b = self.wait.until(EC.presence_of_element_located((By.ID, "column-b")))
        
        self.assertEqual(col_a.text, "A")
        self.assertEqual(col_b.text, "B")
        
        self.helper_html5_drag_and_drop(col_a, col_b)
        
        self.assertEqual(col_a.text, "B", "Block A visual text should be swapped to B.")
        self.assertEqual(col_b.text, "A", "Block B visual text should be swapped to A.")

    def test_tc2_drag_b_to_a(self):
        """TC2: Drag Block B over to Block A back to back."""
        self.driver.get(self.url)
        col_a = self.wait.until(EC.presence_of_element_located((By.ID, "column-a")))
        col_b = self.wait.until(EC.presence_of_element_located((By.ID, "column-b")))
        
        # Do it twice
        self.helper_html5_drag_and_drop(col_a, col_b)
        self.helper_html5_drag_and_drop(col_b, col_a)
        
        self.assertEqual(col_a.text, "A", "Block A visual text should revert to A.")
        self.assertEqual(col_b.text, "B", "Block B visual text should revert to B.")

if __name__ == "__main__":
    unittest.main()
