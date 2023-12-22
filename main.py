import os, csv
from dotenv import load_dotenv
from scrapper import StockChartsScrapper
from selenium.webdriver.common.by import By

load_dotenv()

urls = {
    "login_url": "https://stockcharts.com/login/index.php",
    "get_stock_url": "https://stockcharts.com/h-hd/?",
    "get_stocks_name_url": "https://stockcharts.com/freecharts/catalog/?sl="
}

xpaths = {
    "username": """//*[@id="form_UserID"]""",
    "password": """//*[@id="form_UserPassword"]""",
    "submit": """//*[@id="loginform"]/fieldset/button""",
    "stock_data_path": """//*[@id="historical-data-body"]/div/pre""",
    "stock_names_upper_row": """//*[@id="symcat-links"]""",
    "stock_names_lower_row": """//*[@id="symcat-links-subsection"]""",
    "stock_table_head": """//*[@id="symcat-table"]/thead""",
    "stock_table_body": """//*[@id="symcat-table"]/tbody"""
}

class_name = {
    "stock_names_upper_row": "catalog",
    "stock_names_lower_row": "btn-white"
}

credential = {
    "username": os.getenv("user"),
    "password": os.getenv("password")
}

def login(driver: StockChartsScrapper) -> None:
    driver.go_url(url=urls["login_url"])
    driver.fill_input(xpath=xpaths["username"], value=credential["username"])
    driver.fill_input(xpath=xpaths["password"], value=credential["password"])
    driver.click_btn(xpath=xpaths["submit"])


def scrape_all_stocks(driver: StockChartsScrapper) -> None:
    all_upper_url = []
    all_lower_url = []
    driver.go_url(urls["get_stocks_name_url"])
    for ba in driver.get_children_by_class_name(class_name["stock_names_upper_row"]):
        all_upper_url.append(ba.get_attribute("href"))

    with open("./stocks.txt", "w") as f:
        for ua in all_upper_url:
            driver.go_url(ua)
            for bb in driver.get_children_by_class_name(class_name["stock_names_lower_row"]):
                all_lower_url.append(bb.get_attribute("href"))
            
            with open("./stocks.txt", "w") as f:
                for ub in all_lower_url:
                    print("-> getting stock names from {}".format(ub))
                    driver.go_url(ub)
                    table = driver.driver.find_element(By.XPATH, xpaths["stock_table_body"])
                    for row in table.find_elements(By.TAG_NAME, "tr"):
                        tds = row.find_elements(By.TAG_NAME, "td")
                        f.write(tds[1].text + "\n")
            all_lower_url = []
    print("-> done getting stock names")

def get_stock_data(driver: StockChartsScrapper, stock_name: str):
    driver.go_url(url=urls["get_stock_url"] + stock_name)
    data = driver.get_data(xpath=xpaths["stock_data_path"])
    
    if data.startswith("{"):
        print("{} not found".format(stock_name))
        return

    with open("./datas/{}.txt".format(stock_name), "w") as f:
        f.write(data)
    print("-> done getting {}".format(stock_name))


def txt_to_csv(from_path: str, to_path: str) -> None:
    with open(from_path, 'r') as txt_file:
        next(txt_file)
        columns = txt_file.readline().split()
        next(txt_file)
        with open(to_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(columns)
            while next(txt_file, "EOF") != "EOF":
                csv_writer.writerow(txt_file.readline().split())

def main():
    scrape = StockChartsScrapper()
    login(driver=scrape)

    if not os.path.exists("./datas"):
        os.makedirs("./datas")

    scrape_all_stocks(scrape)

    with open("./stocks.txt", "r") as f:
        for stock_name in f.readlines():
            stock_name = stock_name.strip()
            print("-> getting data from {}".format(stock_name))
            get_stock_data(driver=scrape, stock_name=stock_name)
            txt_to_csv(from_path="./datas/{}.txt".format(stock_name), to_path="./datas/{}.csv".format(stock_name))
            os.remove("./datas/{}.txt".format(stock_name))

    scrape.close()

if __name__ == "__main__":
    main()