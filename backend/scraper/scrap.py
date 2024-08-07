from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from datetime import datetime

current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
formatted_date = current_date.strftime('%Y/%m/%d')

# function that scraps data on ebay, accepts a search key, scrap 
# and return a list of the results 
def scrap_per_key(search_value: str):
    data_to_save = []
    driver = webdriver.Chrome()
    driver.get(f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={search_value}&_sacat=0")
    driver.implicitly_wait(2)
    
    data = driver.find_elements(By.CLASS_NAME, 's-item')
    for i, da in enumerate(data):
        try:
            title = da.find_element(By.CLASS_NAME, 's-item__title').text 
            price = da.find_element(By.CLASS_NAME, 's-item__price').text
            link = da.find_element(By.CLASS_NAME, 's-item__link').get_attribute('href')
            data_to_save.append({'title': title, 'price': price, 'link': link, 'date': formatted_date})
            
        except Exception as e:
            print(f'an error occurred for the search value {search_value}: {e}')
            
    driver.quit()
    print(f'scraping completed')
    return data_to_save

# example usage/ demo run 
#scrap_per_key('electric guitar')