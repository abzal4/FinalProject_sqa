import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome()
driver.maximize_window()

# Implicit Wait
driver.implicitly_wait(10)

driver.get("https://parabank.parasoft.com/parabank/index.htm")
print("Website is opened!")

# Functionality 1: Login
driver.find_element(By.NAME, "username").send_keys("john")
driver.find_element(By.NAME, "password").send_keys("demo")
driver.find_element(By.XPATH, "//input[@value='Log In']").click()
print("Login completed!")

# Explicit Wait
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Accounts Overview")))
print("You went to 'Action Review'")

# Functionality 1: Finding transaction
driver.find_element(By.LINK_TEXT, "Find Transactions").click()

wait.until(EC.visibility_of_element_located((By.ID, "transactionId")))

driver.find_element(By.ID, "transactionId").send_keys("12345")
driver.find_element(By.XPATH, "//button[contains(text(),'Find Transactions')]").click()
print("Finding transaction completed!")

# Fluent wait
def fluent_wait(locator, timeout=20, poll=2):
    end = time.time() + timeout
    while True:
        try:
            element = driver.find_element(*locator)
            if element.is_displayed():
                return element
        except NoSuchElementException:
            pass
        if time.time() > end:
            raise TimeoutError(f"Element {locator} found in {timeout} seconds")
        time.sleep(poll)

wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Accounts Overview")))
try:
    fluent_wait((By.ID, "accountTable"))
    print("Account table founded")
except:
    print("Account table not founded")

# Select Class
driver.find_element(By.LINK_TEXT, "Open New Account").click()
select = Select(driver.find_element(By.ID, "type"))
select.select_by_visible_text("SAVINGS")
print("Selected: SAVINGS")

driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
new_account_id = driver.find_element(By.ID, "newAccountId").text
print("New account created!")

# Action Class
account_link = driver.find_element(By.LINK_TEXT, "Accounts Overview")
actions = ActionChains(driver)
actions.move_to_element(account_link).click().perform()
print("Clicked with ActionChains")

time.sleep(2)
driver.quit()
