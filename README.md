# Lead Generation from LinkedIn Webscraping

Webscraping LinkedIn profiles in LinkedIn Sales Navigator for B2B marketing lead generation.
My target is movers (contacts who have recently changed jobs within the last 90 days) in the HR department.

Utilising the access to thousands of contacts on Sales Navigator in LinkedIn, I have created a webscraper built with Python and Selenium. 
With an automated browser, it will log into my account, loop through the selected industries that it is instructed to scrape, and go through each page of the result pages. Contacts data cannot be scraped unless the profile is scrolled within the viewport and displayed in the browser of end user (i.e. myself) - to tackle this, the webscraper uses an automated scrolling feature by emulating human browsing behaviour, including random sleep time. Scraped data is then saved into a CSV file.

Scraped data will then be compared against a separate CSV file containing data from a company's CRM database. 

If the name of the scraped contact does not match any of the names within the CRM, it will be classified as a 'new lead', and the script will return a list of email addresses of the employees, whose contact details are in the CRM, that are employed in the same company that the 'new lead' is currently working in. These new leads will then be placed into a spreadseet. 

If the name of the scraped contact matches any of the names on the CRM, it is assumed that they are the same person. The script then checks whether their contact details are 'up-to-date' by comparing their company names - the company name displayed in the CRM and the company name that is freshly scraped from LinkedIn. If they are the same, then the contact details are up-to-date. If they are not the same, the script will return the name of the new company and a list of email addresses of employees, whose contact details are in the CRM, working in that new company. These are all placed into a separate spreadsheet for easier identification.

Final script combining webscrape and CRM script: https://github.com/pymche/LinkedIn-LeadGen-Webscrape/blob/main/Final_script.py
