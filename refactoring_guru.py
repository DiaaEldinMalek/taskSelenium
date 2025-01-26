from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import requests
import json


class GuruScraper:

    def __init__(self, driver: webdriver.Chrome, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.driver = driver

    def _click_button_at_xpath(self, xpath):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()

    def load_url(self):
        self.driver.get(self.url)

    def navigate_to_mainpage(self):
        main_page_xpath = "/html/body/header/nav/div[1]/div/div[2]/div[1]/a/img"
        self._click_button_at_xpath(main_page_xpath)

    def navigate_to_login(self):
        login_button_xpath = "/html/body/div/nav/div/ul/li[3]/a"
        self._click_button_at_xpath(login_button_xpath)

    def login(self):
        email_input_id = "email"
        password_input_id = "password"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, email_input_id))
        ).send_keys(self.email)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, password_input_id))
        ).send_keys(self.password)
        self._click_button_at_xpath(
            "/html/body/main/div/div[2]/div/div/form/div[3]/div[1]/button/span"
        )

    def navigate_to_design_patterns_mainpage(self):
        design_patterns_xpath = (
            "/html/body/div/main/div/div[2]/div[3]/div[2]/div/div[2]/a"
        )
        self._click_button_at_xpath(design_patterns_xpath)

    def open_design_pattern_catalogue(self):
        catalogue_xpath = "/html/body/div/main/div/div/div/div[6]/span/a"
        self._click_button_at_xpath(catalogue_xpath)

    def extract_all_patterns_from_catalogue(self):
        all_patterns = []
        pattern_types = ["creational", "structural", "behavioral"]
        content = self.driver.page_source
        page = bs4.BeautifulSoup(content, "html.parser")

        for pattern_type in pattern_types:
            all_links = page.find("div", class_=f"{pattern_type}-patterns").find_all(
                "a"
            )
            for link in all_links:
                url = f"{self.url}{link['href']}"
                pattern_data = self.load_pattern_data(requests.get(url).content)
                pattern_data["type"] = pattern_type
                all_patterns.append(pattern_data)

        return all_patterns

    def load_pattern_data(self, content):

        page = bs4.BeautifulSoup(content, "html.parser")
        title = page.find("h1", class_="title").text
        print("Scraping pattern:", title)
        intent_desc = page.find("h2", id="intent").parent.find_all("p")
        problem_desc = page.find("h2", id="problem").parent.find_all("p")
        solution_desc = page.find("h2", id="solution").parent.find_all("p")
        structure_desc = page.find("h2", id="structure").parent.find_all("p")

        result = {
            "title": title,
            "intent": "\n\n".join([p.text for p in intent_desc]),
            "problem": "\n\n".join([p.text for p in problem_desc]),
            "solution": "\n\n".join([p.text for p in solution_desc]),
            "structure": "\n\n".join([p.text for p in structure_desc]),
        }
        return result

    def main(self):
        self.load_url()
        self.navigate_to_login()
        self.login()
        self.navigate_to_mainpage()
        self.navigate_to_design_patterns_mainpage()
        self.open_design_pattern_catalogue()
        all_patterns = self.extract_all_patterns_from_catalogue()

        with open("patterns.json", "w") as file:
            json.dump(all_patterns, file)
