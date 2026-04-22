
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Mở trang test
driver.get("https://the-internet.herokuapp.com/drag_and_drop")

# Lấy 2 element A và B
column_a = driver.find_element(By.ID, "column-a")
column_b = driver.find_element(By.ID, "column-b")

# Hàm drag & drop bằng JS (ổn định nhất)
def drag_and_drop_js(source, target):
    driver.execute_script("""
    function createEvent(typeOfEvent) {
        var event = document.createEvent("CustomEvent");
        event.initCustomEvent(typeOfEvent, true, true, null);
        event.dataTransfer = {
            data: {},
            setData: function(key, value) { this.data[key] = value; },
            getData: function(key) { return this.data[key]; }
        };
        return event;
    }

    function dispatchEvent(element, event, transferData) {
        if (transferData !== undefined) {
            event.dataTransfer = transferData;
        }
        element.dispatchEvent(event);
    }

    var source = arguments[0];
    var target = arguments[1];

    var dragStartEvent = createEvent('dragstart');
    dispatchEvent(source, dragStartEvent);

    var dropEvent = createEvent('drop');
    dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

    var dragEndEvent = createEvent('dragend');
    dispatchEvent(source, dragEndEvent);
    """, source, target)

# ===== TEST CASE 1: A -> B =====
print("Test A -> B")

drag_and_drop_js(column_a, column_b)
time.sleep(2)

# Lấy text sau khi drag
text_a = column_a.text
text_b = column_b.text

print("Column A:", text_a)
print("Column B:", text_b)

assert "B" in text_a
assert "A" in text_b

print("PASS A -> B")

# ===== TEST CASE 2: B -> A =====
print("Test B -> A")

drag_and_drop_js(column_b, column_a)
time.sleep(10)

text_a = column_a.text
text_b = column_b.text

print("Column A:", text_a)
print("Column B:", text_b)

assert "A" in text_a
assert "B" in text_b

print("PASS B -> A")

driver.quit()