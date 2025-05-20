import pytest
import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ----------- Logging Setup -----------
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('test_log.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# ----------- Pytest Fixture -----------
@pytest.fixture
def driver():
    logger.info("Opening Chrome browser...")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    logger.info("Closing browser...")
    driver.quit()

# ----------- Screenshot Utility -----------
def save_screenshot(driver, name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    path = os.path.join("screenshots", f"{name}_{int(time.time())}.png")
    driver.save_screenshot(path)
    logger.info(f"Screenshot saved: {path}")

# ----------- Parabank Login Test -----------
def test_parabank_login(driver):
    logger.info("Opening Parabank website...")
    driver.get("https://parabank.parasoft.com/parabank/index.htm")
    try:
        logger.info("Filling in login form...")
        driver.find_element(By.NAME, "username").send_keys("john")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()

        time.sleep(2)  # Let the page load

        logger.info("Checking login success by URL...")
        assert "overview.htm" in driver.current_url
        logger.info("Test: Login successful!")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        save_screenshot(driver, "parabank_login_failure")
        raise
