import numpy as np
import pandas as pd
from selenium import webdriver


"""
This module is used to retrieve broker's detailed information from brokercheck.finra.org
"""

#set up scrape and javascript 
url='http://brokercheck.finra.org/Individual/Summary/4509743' #url

driver = webdriver.Firefox() #open firefox
driver.get(url)

driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click() #click on accept
driver.find_element_by_id("plus").click() #click on expand


# get the disclosure details and save in dictionary
table={}
disclosure_date=[]
disclosure_type=[]
for i in driver.find_elements_by_xpath('//div[@class="discfirstcolumn TextBold"]'):
    disclosure_date.append(i.text)
for i in driver.find_elements_by_xpath('//div[@class="discsecondcolumn TextBold"]'):
    disclosure_type.append(i.text)
        
    

for i in zip(driver.find_elements_by_xpath('//div[@class="disclosureInnerTable"]'),\
               driver.find_elements_by_xpath('//div[@class="disclosureValue"]')):
   table[i[0].text]=i[1].text

driver.close()

print table
