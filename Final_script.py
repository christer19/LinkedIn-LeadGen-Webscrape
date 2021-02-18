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
import pandas as pd

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






# Compare scraped contacts from LinkedIn with database from CRM


# Load scraped contacts

leads_df = pd.read_csv('scraped_newhr.csv')

# clean data in scraped contacts

def name_clean(x):
    x = x.split(' ')
    x = [name for name in x if name not in x[2:]]
    x = ' '.join(x)
    return x

leads_df['Cleaned Name'] = leads_df['LinkedIn Name'].apply(name_clean)
leads_df[['First Name', 'Last Name']] = leads_df['Cleaned Name'].str.split(' ', expand = True)
leads_df[['Title', 'Company']] = leads_df['Title_Company'].str.split(' at ', expand = True).drop(columns=2)
leads_df.drop('Title_Company', axis = 1, inplace=True)
leads_df = leads_df[['First Name', 'Last Name', 'LinkedIn Name', 'Title', 'Company', 'Industry', 'Location']]

leads_df.to_csv(r'scraped_newhr_cleaned.csv', index = False)


# Load CRM database CSV file

crm_df = pd.read_csv('Leads_001.csv')

crm_df[['First Name', 'Last Name', 'Full Name', 'Title', 'Company', 'Email', 'Phone', 'Industry', 'Lead Status', 'Record Id', 'Lead Owner Id']]


# Save full names and company names in CRM to lists for later use

# Save full name
full_name = []
for name in crm_df['Full Name']:
    full_name.append(name)

# Drop contacts with empty company
crm_df = crm_df.dropna(axis='index', subset=['Company'], how='any').reset_index(drop=True)

# Save companies
company = [comp for comp in crm_df['Company']]

# for storing data temporarily, then append to multiple csv files at the same time using context manager
data_tobe_exported = {
    
    'existing_leads.csv': [],
    'new_leads.csv': []
    
}


# If company exists in current database, return email of our CRM leads from same company
# (for reference to contruct email for our new contact who is in this company)

def company_email(x):
    
    # check if company exists in CRM
    
    for crm in range(0, len(company)):
        if x in company[crm]:
            company_email_match = 1
            
            break

        # If company does not exist in current database
        elif x not in company[crm]:
            company_email_match = 0
            
            
    # Return sample emails of that company
    
    filt = crm_df['Company'] == company[crm]
    email_ref = crm_df[filt][['Full Name', 'Email']]
    email_ref = email_ref.to_dict('split')
    email_ref = email_ref['data'][:3]
        
    if company_email_match == 1:
            return email_ref
        
    elif company_email_match == 0:
            email_ref = f'{x} does not currently exist in our CRM'
            return email_ref
        

def record_id_clean(a):
    id = crm_df[a]['Record Id'].values
    id = ', '.join([str(id[z]) for z in range(0, len(id))])
    return id
        
    
# Check if scraped contact is in our CRM, and if it is in CRM, whether their info is up to date (same company?)
    
def company_match(y, x):
    name_filt = crm_df['Full Name'] == y
    fullname_company = crm_df[name_filt]['Company']
    
    fullname_and_company = []
    for company in fullname_company:
        fullname_and_company.append(company)
    
    fullname_company = ', '.join(fullname_and_company)
    
    Scraped_company = x
    
    matchy = 0
    
    if Scraped_company.lower() in fullname_company.lower() or fullname_company.lower() in Scraped_company.lower():
        matchy = 1
    elif Scraped_company.lower() not in fullname_company.lower() or fullname_company.lower() not in Scraped_company.lower():
        matchy = 0
        
    if matchy == 1:
            uptodate = 'Y'
            crmcompany = fullname_company
            linkedincompany = Scraped_company
            email_ref = None
            record_id = record_id_clean(name_filt)
            return uptodate,crmcompany,linkedincompany,email_ref,record_id
    elif matchy == 0:
            uptodate = 'N'
            crmcompany = fullname_company
            linkedincompany = Scraped_company
            email_ref = company_email(Scraped_company)
            record_id = record_id_clean(name_filt)
            return uptodate,crmcompany,linkedincompany,email_ref,record_id


# read scraped data and temporarily store them into the dictionary to be written into CSV files later

with open('scraped_newhr_cleaned.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    
    for lead in csv_reader:
        
        print(lead)

        # loading scraped contacts
        
        FullName = lead[2]
        FirstName = lead[0]
        LastName = lead[1]
        CompanyName = lead[4]
        Title = lead[3]
        Industry = lead[5]
        Location = lead[6]
        Email = None
        LeadSource = 'LinkedIn Profile'
        LeadStatus = None
                
        # If scraped full name is not in CRM, check whether their company exists in our database
        # If it does, return email samples of their employees for us to construct new email of this new contact
        
        if FullName not in full_name:
 
            email_ref = company_email(CompanyName)
    
            csv_data_newlead = [[FullName, FirstName, LastName, CompanyName, Email, email_ref, Title, Industry, Location, LeadSource, LeadStatus]]
                
            data_tobe_exported['new_leads.csv'].extend(csv_data_newlead)
                
        # If new name is in CRM, check whether the contact's info is up to date
        # i.e. CRM company matches company name scraped from LinkedIn
        
        elif FullName in full_name:

            uptodate,crmcompany,linkedincompany,email_ref,record_id = company_match(FullName, CompanyName)
            
            csv_data_existing = [[record_id, FullName, FirstName, LastName, uptodate, crmcompany, linkedincompany, Email, email_ref, Title, Industry, Location, LeadSource, LeadStatus]]

            data_tobe_exported['existing_leads.csv'].extend(csv_data_existing)


# append stored data in dictionary to multiple csv files

for eachfilename, eachlist in data_tobe_exported.items():
    with open(eachfilename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        
        if eachfilename == 'new_leads.csv':
            writer.writerow(['Full Name', 'First', 'Last', 'Company', 'Email', 'Company Email Sample', 'Title', 'Industry', 'Location', 'Lead Source', 'Lead Status'])

        elif eachfilename == 'existing_leads.csv':
            writer.writerow(['Record ID', 'Full Name', 'First', 'Last', 'Up-to-date?', 'Old Company in CRM', 'Updated Company LinkedIn', 'Email', 'Company Email Sample', 'Title', 'Industry', 'Location', 'Lead Source', 'Lead Status'])

        for line in eachlist:
            writer.writerow(line)
