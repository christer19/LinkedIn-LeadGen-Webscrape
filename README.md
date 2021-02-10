# Lead Generation from LinkedIn Webscraping

Webscraping LinkedIn profiles in LinkedIn Sales Navigator for B2B marketing lead generation.
My target is movers (contacts who have recently changed jobs within the last 90 days) in the HR department.

Utilising the access to thousands of contacts on Sales Navigator in LinkedIn, I have created a webscraper built with Python and Selenium. 
With an automated browser, it will log into my account, loop through the selected industries that it is instructed to scrape, and go through each page of the result pages. Contacts data cannot be scraped unless the profile is scrolled within the viewport and displayed in the browser of end user (i.e. myself) - to tackle this, the webscraper uses an automated scrolling feature by emulating human browsing behaviour, including random sleep time. 

After the data is scraped and saved into a CSV file, it will then be opened in another python script, where the scraped data will be cleansed, and compared with the existing contacts from the database that I have obtained from a CRM system.
