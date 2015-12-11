import numpy as np
import pandas as pd


url='http://brokercheck.finra.org/Individual/Summary/4509743'

#==============================================================================
# #
#==============================================================================
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time


driver = webdriver.Firefox()
driver.get(url)

driver.find_element_by_id("ctl00_phContent_TermsAndCondUC_BtnAccept").click()
driver.find_element_by_id("plus").click()

time.sleep(2)

# get the disclosure details
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