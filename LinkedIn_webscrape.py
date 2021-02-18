from bs4 import BeautifulSoup
import requests
import selenium
import time
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

ID = os.environ.get('linkedin_username')
PW = os.environ.get('linkedin_pw')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.linkedin.com/sales/login")

contacts = []

# Log In
iframe = driver.find_element_by_tag_name("iframe")
driver.switch_to.frame(iframe)

time.sleep(2)

username = driver.find_element_by_xpath("//input[@id='username']")
username.send_keys(ID)

password = driver.find_element_by_xpath("//input[@id='password']")
password.send_keys(PW)

login = driver.find_element_by_class_name("login__form_action_container")
login.click()

# Navigate to site

# Looping through each industry

industries ={
    "Internet": 6,
    "Research": 70,
    "Telecommunications": 8,
    "Government Administration": 75,
    "Education Management": 69,
    "Utilities": 59,
    "Human Resources": 137,
    "Hospital & Healthcare": 14,
    "Financial Services": 43,
    "Higher Education": 68,
    "Retail": 27,
    "IT and Services": 96,
    "Oil & Energy": 57,
    "Construction": 48,
    "Automotive": 53,
    "Insurance": 42,
    "Pharmaceuticals": 15,
    "Food Production": 23,
    "Food & Beverages": 34,
    "Facilities Services": 122,
    "Banking": 41,
    "Legal Services": 10,
    "Staffing and Recruitment": 104
}

total_pages = 1

def var_URL(industry, page=1):
    industry = str(industry)
    page = str(page)
    url = 'https://www.linkedin.com/sales/search/people?companySize=E%2CF%2CG%2CH%2CI&doFetchHeroCard=false&functionIncluded=12&geoIncluded=101165590&industryIncluded=' + industry + '&logHistory=true&page=' + page + '&rsLogId=626686577&searchSessionId=aHJOnIBpTq%2BsfziTKdMYfA%3D%3D&spotlight=RECENT_POSITION_CHANGE'
    return url

def find_last_page():
    last_page = driver.find_elements_by_xpath("//ol[@class='search-results__pagination-list']/li")
    last_page = str(last_page[-1].text)
    if '…' in last_page:
        last_page = last_page.split()
        last_page = int(last_page[1])
    elif '…' not in last_page:
        last_page = int(float(last_page))
    return last_page


# Loop through each industry, scrape data from each page

try:

    for industry, industry_code in industries.items():

        url = var_URL(industry_code)

        driver.get(url)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results__pagination"))
        )

        time.sleep(2)

        current_page = 1
        lastpage = find_last_page()

        print('industry:', industry)
        print('total pages:', lastpage)

        while current_page <= lastpage:

            url2 = var_URL(industry_code, current_page)
            driver.get(url2)
            print('current page:', current_page)

            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results__result-item"))
            ) 

            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.1);")
            time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.2);")
            if current_page%8 == 0:
                time.sleep(np.random.randint(3, 6))
            else:
                time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.3);")
            time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.45);")
            if current_page%5 == 0:
                time.sleep(np.random.randint(30, 90))
            else:
                time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.6);")
            time.sleep(np.random.uniform(1.5, 2))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.75);")
            time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.9);")
            time.sleep(np.random.uniform(0.5, 1))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            html = driver.find_elements_by_class_name('horizontal-person-entity-lockup-4')

            for info in html:
                info = info.text
                info = info.split('\n')
                info.append(industry)
                contacts.append(info)

            if current_page%3 == 0 or current_page == lastpage+1:
                time.sleep(np.random.randint(10, 20))
            elif total_pages%10 == 0:
                time.sleep(np.random.randint(90, 120))

            current_page += 1
            total_pages += 1
        
except:
    driver.quit()
finally:
    driver.quit()


# write data into a list to be exported to CSV file

extract = []

for line in contacts:
    exclude = ['Premium Member Badge', 'Viewed']
    exclude2 = 'is online' 
    exclude3 = 'was last active'
    line = [x for x in line if x not in exclude and exclude2 not in x and exclude3 not in x]
    extract.extend([[line[0], line[1], line[-1], line[-2]]])


# write to csv file

with open('scraped_newhr.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['LinkedIn Name', 'Title_Company', 'Industry', 'Location'])
    for line in extract:
        csv_writer.writerow(line)
