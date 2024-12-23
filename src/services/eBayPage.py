from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class eBayPage:

    locators = {
        "next_page": "a.pagination__next"
    }

    def __init__(self, driver):
        self.driver = driver.driver

    def get_next_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination__next"))
        ).click()

