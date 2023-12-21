import os
from dotenv import load_dotenv
from scrapper import StockChartsScrapper
from cleaner import to_csv

load_dotenv()

stock_name = "INTC"

urls = {
    "login": "https://stockcharts.com/login/index.php",
    "get_stock": "https://stockcharts.com/h-hd/?"
}

xpaths = {
    "username": """//*[@id="form_UserID"]""",
    "password": """//*[@id="form_UserPassword"]""",
    "submit": """//*[@id="loginform"]/fieldset/button""",
    "data_path": """//*[@id="historical-data-body"]/div/pre"""
}

credential = {
    "username": os.getenv("user"),
    "password": os.getenv("password")
}

def login(driver: StockChartsScrapper) -> None:
    driver.go_url(url=urls["login"])
    driver.fill_input(xpath=xpaths["username"], value=credential["username"])
    driver.fill_input(xpath=xpaths["password"], value=credential["password"])
    driver.click_btn(xpath=xpaths["submit"])

def main():
    scrape = StockChartsScrapper()
    login(driver=scrape)
    scrape.go_url(url=urls["get_stock"] + stock_name)

    data = scrape.get_data(xpath=xpaths["data_path"])

    if not os.path.exists("./datas"):
        os.makedirs("./datas")
    
    with open("./datas/{}.txt".format(stock_name), "w") as f:
        f.write(data)
    
    to_csv(from_path="./datas/{}.txt".format(stock_name), to_path="./datas/{}.csv".format(stock_name))

    os.remove("./datas/{}.txt".format(stock_name))
    

    scrape.close()

if __name__ == "__main__":
    main()