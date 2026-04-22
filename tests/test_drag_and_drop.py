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

    def tearDown(self):
        self.driver.quit()

    def test_drag_and_drop_html5(self):
        self.driver.get("https://the-internet.herokuapp.com/drag_and_drop")
        
        source = self.wait.until(EC.presence_of_element_located((By.ID, "column-a")))
        target = self.wait.until(EC.presence_of_element_located((By.ID, "column-b")))
        
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
        
        # Verify swap
        self.assertEqual(source.text, "B")
        self.assertEqual(target.text, "A")

if __name__ == "__main__":
    unittest.main()
