import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
import os


class Driver:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(self.sleep_time)
        self.end_session()

    def __init__(self, url, num_of_iterations, sleep_time):
        load_dotenv()
        options = Options()
        service = Service()
        options.add_argument('--no-eadless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.url = url
        self.num_of_iterations = num_of_iterations
        self.sleep_time = sleep_time
        self.username = os.getenv("LOGIN")
        self.password = os.getenv("PASSWORD")

    def open(self):
        self.driver.get(self.url)

    def end_session(self):
        self.driver.quit()

    def get_page_source(self):
        for num in range(1, self.num_of_iterations + 1):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self.driver.page_source
