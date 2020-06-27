# ecommerce-product-price-comparison

### General Information
This simple tool enables the user to search for a specific item on the 3 popular eCommerce platforms for the purpose of:
* Comparing product price distributions between different eCommerce websites for a consumer point of view.
* Leverage on the market selling price of a product by knowing the average, minimum, maximum, 25th, 50th, up to 75th percentile pricing point for a seller point of view.

### Limitations:
* The default online retail sites to be searched are: Shopee, eBay and Lazada.  (PH websites)
* Search can only be done 1 product at a time.
* Can be slow due to Lazada processing is using Selenium webdriver. 

### Technology: 
Python 3.7.3

### Tools Used:
1. Shopee - Requests library
2. eBay - Requests and BeautifulSoup
3. Lazada - Selenium Webdriver

### Pre-requisites:
* Selenium Webdriver installed (the module uses Chrome version)
* Webdriver location: 'C:\Program Files (x86)\chromedriver.exe'
* Python installed

### Steps to run:
1. Execute the main version ecommerce.py
```
$ python ecommerce.py
```
2. Enter the item you want to search, ie. Herschel Little America backpack
```
$ Hola! Please enter an item you want to search: Herschel Little America 
```
3. Tool will begin its search.

### Sample output:
1. Statistics Table

![Alt text](https://github.com/charlievc/ecommerce-product-price-comparison/blob/master/img_sample/statTable.jpg)

2. Statistics Graph

![Alt text](https://github.com/charlievc/ecommerce-product-price-comparison/blob/master/img_sample/statPlot.jpg)

