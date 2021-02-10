import pandas as pd
import csv

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
