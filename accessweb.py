#!/usr/bin/env python
# coding: utf-8

# In[75]:


import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *

class Website(object): # Abstract Class
    # Constructor
    def __init__(self,item):
        self.item = item
    
    # Methods
    def setURL(self,url):
        self.url = url
        
    def setDriver(self):
        print('CHROME DRIVER SESSION START **')
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=chrome_options)
        driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe') 
        driver.get(self.url)
        return driver  
    
    def exitDriver(self,driver):
        print('CHROME DRIVER SESSION END **')
        driver.close()
    
    
class Lazada(Website):
    def __init__(self,item): 
        super().__init__(item)
        self.url = 'https://www.lazada.com.ph/'
        self.df = pd.DataFrame()
        self.ls_title = []
        self.ls_price = []
    
    def startSearch(self,driver):
        print('WEBDRIVER SEARCH INITIATED FOR LAZADA **')
        search = driver.find_element_by_id('q')
        search.send_keys(self.item) 
        search.send_keys(Keys.RETURN)
        time.sleep(3)
        
    def scrapeCurrPage(self,driver):
        item_titles = WebDriverWait(driver,50).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'c16H9d')))
        time.sleep(1)
        item_prices = WebDriverWait(driver,50).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'c3gUW0')))
        time.sleep(1)
        print(len(item_titles),'titles in current page')
        print(len(item_prices),'prices in current page')
        for title in item_titles:
            self.ls_title.append(title.text)
        for price in item_prices:
            self.ls_price.append(price.text)
        print('Total Title count:',len(self.ls_title))
        print('Total Price count:',len(self.ls_price))        
        
    def nextPage(self,driver):
        while True:
            print('Finalizing . . .')
            time.sleep(5)
            next_page = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH,'//li[@title="Next Page"]')))
            if next_page.get_attribute('aria-disabled') == "true":
                print('<< You have reached the end of the search result. >>')
                break
            else:
                next_page.click()
                print('Next page clicked! Loading . . .')
                time.sleep(5)
                self.scrapeCurrPage(driver)        
    
    def createDf(self):
        self.df=pd.DataFrame(zip(self.ls_title,self.ls_price),columns=['itemName','itemPrice'])
        self.df['webPage'] = 'Lazada'
        self.df['itemPrice']=self.df['itemPrice'].str.replace('₱','')
        self.df['itemPrice']=self.df['itemPrice'].str.replace(',','').astype(float)
        return self.df     
    
    def letsAutomateThis(newObj):
        """ Automatic Scraping """
        driver = newObj.setDriver()
        newObj.startSearch(driver)
        newObj.scrapeCurrPage(driver)
        newObj.nextPage(driver)
        newObj.exitDriver(driver)
        df = newObj.createDf()
        return df

    
class Shopee(Website):
    def __init__(self,item): # Constructor
        super().__init__(item)
        self.url = 'https://www.shopee.ph/'
        self.df = pd.DataFrame()
        self.ls_title = []
        self.ls_price = []
    
    def fetchHTML(self):
        headers = {
         'User-Agent': 'Chrome',
         'Referer': '{}search?keyword={}'.format(self.url,self.item)
        }
        url = 'https://www.shopee.ph/api/v2/search_items/?by=relevancy&keyword={}&limit=100&newest=0&order=desc&page_type=search'.format(self.item)
        print('REQUEST INITIATED FOR SHOPEE **')
        req = requests.get(url,headers=headers).json()        
        return req
    
    def scrapePage(self,req):
        for item in req['items']:
            self.ls_title.append(item['name'])
            self.ls_price.append(item['price']/100000)

    def createDf(self):
        self.df=pd.DataFrame(zip(self.ls_title,self.ls_price),columns=['itemName','itemPrice'])
        self.df['webPage'] = 'Shopee'
        return self.df              
            
    def letsAutomateThis(newObj):
        """ Automatic Scraping """
        req = newObj.fetchHTML()
        newObj.scrapePage(req)
        df = newObj.createDf()
        return df
    

class Ebay(Website):
    def __init__(self,item):
        super().__init__(item)
        self.url = 'https://www.ebay.ph/'
        self.df = pd.DataFrame()
        self.ls_title = []
        self.ls_price = []
    
    def fetchHTML(self):
        """ Fetch the HTML markup """
        headers = { # define a user agent to avoid detection of http request
            'User-Agent':'Chrome'
        }
        print('REQUEST INITIATED FOR EBAY **')
        for i in range(1,11):
            print('Page',i)
            url = 'https://www.ebay.ph/sch/i.html?_from=R40&_nkw={}&_pgn={}'.format(self.item,str(i))
            req = requests.get(url,headers=headers)
            self.scrapePage(req)
    
    def scrapePage(self,req):
        soup = BeautifulSoup(req.text,'lxml')
        results = soup.find_all('div',attrs={'id':'Results'})
        for i in results:
            for title in i.find_all('div',attrs={'class':'gvtitle'}):
                self.ls_title.append(title.text)
            for price in i.find_all('div',attrs={'class':'gvprices'}):
                currPrice = price.find('span',attrs={'class':'bold'})
                self.ls_price.append(currPrice.text)
        
    def createDf(self):
        self.df=pd.DataFrame(zip(self.ls_title,self.ls_price),columns=['itemName','itemPrice'])
        self.df['webPage'] = 'Ebay'
        self.df['itemName']=self.df['itemName'].str.replace('\n','')
        self.df['itemPrice']=self.df['itemPrice'].str.replace('PHP','')
        self.df['itemPrice']=self.df['itemPrice'].str.replace('\n','')
        self.df['itemPrice']=self.df['itemPrice'].str.replace(',','').astype(float)          
        return self.df         
    
    def letsAutomateThis(newObj):
        """ Automatic Scraping """
        newObj.fetchHTML()
        df = newObj.createDf()
        return df


# In[2]:


class Amazon(Website):
    def __init__(self,item):
        super().__init__(item)
        self.url = 'https://www.amazon.com/philippines/s?k=philippines&language=en_US&currency=PHP'
        self.df = pd.DataFrame()
        self.ls_title = []
        self.ls_price = []
    
    def fetchHTML(self):
        """ Fetch the HTML markup """
        headers = { # define a user agent to avoid detection of http request
            'User-Agent':'Chrome'
        }
        url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'.format(self.item)
        print('REQUEST INITIATED FOR AMAZON **')
        req = requests.get(url,headers=headers)
        return req


# In[ ]:


#x = Amazon('pen')


# In[ ]:


#x.url


# In[ ]:


#resp = x.fetchHTML()


# In[ ]:


#resp.text


# In[ ]:


#soup


# In[ ]:


#resp.session().close()

