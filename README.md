# StockChartsScrapper
this script get stock data and store in csv format file using Selenium with ChromeWebdriver

## Quick Start

First install all dependencies by this script:
```console
$ python -m pip install -r requirements.txt
```


Then create .env file and put your [StockCharts](https://stockcharts.com/) account credential like this:
```txt
user=<USERNAME>
password=<PASSWORD>
```


And run main.py script to start the scrapping process:
```console
$ python main.py
```


When everything is done you should get all stock data in ./datas
