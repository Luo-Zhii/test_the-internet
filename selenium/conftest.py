import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    # Initialize the Chrome driver using webdriver_manager
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Set a 10-second implicit wait as requested
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    # Yield the driver to the tests
    yield driver
    
    # Ensure driver.quit() is called afterward
    driver.quit()
