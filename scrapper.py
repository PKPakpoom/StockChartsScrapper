from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class StockChartsScrapper():
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)

    def go_url(self, url: str) -> None:
        self.driver.get(url=url)

    def fill_input(self, xpath: str, value: str):
        self.driver.find_element(By.XPATH, xpath).send_keys(value)

    def get_children(self, xpath: str) -> list[webdriver.Remote._web_element_cls]:
        return self.driver.find_elements(By.XPATH, xpath)
    
    def get_children_by_class_name(self, class_name: str) -> list[webdriver.Remote._web_element_cls]:
        return self.driver.find_elements(By.CLASS_NAME, class_name)
                                                      
    def click_btn(self, xpath: str) -> None:
        self.driver.find_element(By.XPATH, xpath).click()

    def get_data(self, xpath: str) -> str:
        return self.driver.find_element(By.XPATH, xpath).text
    
    def close(self):
        self.driver.close()