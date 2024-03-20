#https://voter-registration-maps-traviscountytx.hub.arcgis.com/pages/c24b019674604e1eb46fdf169a20b112
#https://www.wilcotx.gov/220/Public-Information-Request

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import random

def check_homestead_williamson(street_name, first_name, last_name, current_row, total_rows):
    base_url = "https://tax.wilco.org/Proxy-WilliamsonTax/Search/Properties/"
    params = {
        "f": street_name,
        "ty": "2023",
        "pvty": "2023",
        "pn": "1",
        "st": "9",
        "so": "1",
        "pt": "RP;PP;MH;NR",
        "take": "20",
        "skip": "0",
        "page": "1",
        "pageSize": "20"
    }

    agent_list = [  # User-Agent list remains unchanged
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
       "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
       # Add more User-Agents as needed
    ]

    headers = {'User-Agent': random.choice(agent_list)}

    proxy_list = [
        'http://ekbhyghn:3j7epm34sgrf@38.154.227.167:5868',
        'http://ekbhyghn:3j7epm34sgrf@185.199.229.156:7492',
        'http://ekbhyghn:3j7epm34sgrf@185.199.228.220:7300',
        'http://ekbhyghn:3j7epm34sgrf@185.199.231.45:8382',
        'http://ekbhyghn:3j7epm34sgrf@188.74.210.207:6286',
        'http://ekbhyghn:3j7epm34sgrf@188.74.183.10:8279',
        'http://ekbhyghn:3j7epm34sgrf@188.74.210.21:6100',
        'http://ekbhyghn:3j7epm34sgrf@45.155.68.129:8133',
        'http://ekbhyghn:3j7epm34sgrf@154.95.36.199:6893',
        'http://ekbhyghn:3j7epm34sgrf@45.94.47.66:8110'
    ]

    try:
        proxy = {'http': random.choice(proxy_list)}
        response = requests.get(base_url, params=params, headers=headers, proxies=proxy)
        if response.status_code != 200:
            return False, False

        data = response.json()

        if not data["ResultList"]:
            print(f"Row {current_row}/{total_rows}: Property not found: {street_name}")
            return False, False

        property_quick_ref_id = data["ResultList"][0]["PropertyQuickRefID"]
        party_quick_ref_id = data["ResultList"][0]["PartyQuickRefID"]

        details_url = f"https://tax.wilco.org/Property-Detail/PropertyQuickRefID/{property_quick_ref_id}/PartyQuickRefID/{party_quick_ref_id}#"

        response = requests.get(details_url, headers=headers, proxies=proxy)
        if response.status_code != 200:
            return False, False

        soup = BeautifulSoup(response.content, 'html.parser')
        exemptions = soup.find('td', text='Exemptions')
        owner_name = soup.find('td', text='Owner Name')
        
        if exemptions and owner_name:
            exemptions_text = exemptions.find_next_sibling('td').text.strip()
            owner_name_text = owner_name.find_next_sibling('td').text.strip()
            
            homestead_found = False
            ownername_found = False

            if "Homestead" in exemptions_text and "Exemption" in exemptions_text and "Active" in exemptions_text:
                homestead_found = True
            if first_name.lower() in owner_name_text.lower() and last_name.lower() in owner_name_text.lower():
                ownername_found = True

            print(f"Row {current_row}/{total_rows}: Homestead found: {homestead_found}, Ownername found: {ownername_found}")
            return homestead_found & ownername_found, ownername_found

        print(f"Row {current_row}/{total_rows}: Property not found.")
        return False, False

    except Exception as e:
        print(f"Error occurred: {e}")
        return False, False

# Read the CSV file
df = pd.read_csv('/Users/sikun.peng/Downloads/territory/2024/78613s.csv')

df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
df['Homestead'] = ""
df['Ownername'] = ""

WILLIAMSON_ZIP = [
    '78613',
    '78626',
    '78628',
    '78633',
    '78641',
    '78642',
    '78660',
    '78664',
    '78665',
    '78681',
    '78717'
]

for index, row in df.iterrows():
    zip_code = str(row['Physical ZIP'])
    if zip_code in WILLIAMSON_ZIP:
        address = row['Physical Address'] + ', ' + row['Physical City'] + ', ' + str(row['Physical ZIP'])
        homestead_value, ownername_value = check_homestead_williamson(address, row['First Name'], row['Last Name'], index + 1, len(df))
        if homestead_value:
            df.at[index, 'Homestead'] = 'YES'
        if ownername_value:
            df.at[index, 'Ownername'] = 'YES'
    else:
        print(f"Row {index + 1}/{len(df)}: Skipped - Not in Williamson County")
    time.sleep(random.uniform(0.5, 2))

# Function to split the address into subsets
def split_address(address):
    parts = address.split(',')
    house_number = parts[0].split()[0]
    
    direction = ''
    rest_address = ' '.join(parts[0].split()[1:])
    direction_match = re.search(r'\b[NSEW]\b', rest_address)  # Match single letter N/S/E/W
    if direction_match:
        direction = direction_match.group()
        rest_address = rest_address.replace(direction, '')  # Remove direction from rest_address
    direction = direction.strip()
    
    apt_number = ''
    rest_address_parts = rest_address.split()
    for i, part in enumerate(rest_address_parts):
        if 'Apt' in part or 'Unit' or 'Suite' in part:
            apt_match = re.search(r'\d+', rest_address_parts[i+1])  # Extract number from Apt/Unit string
            if apt_match:
                apt_number = apt_match.group()
            rest_address = ' '.join(rest_address_parts[:i] + rest_address_parts[i+2:])  # Remove Apt/Unit and its number from rest_address
            break
    
    street = rest_address.strip()
    
    return house_number, direction, street, apt_number

df['House #'], df['N/S/E/W'], df['Street'], df['Apt #'] = zip(*df['Physical Address'].apply(split_address))

df['Phone'] = df['Phone'].replace('N/A', pd.NA)

df = df.groupby(['House #', 'N/S/E/W', 'Street', 'Apt #', 'Physical City', 'Physical State', 'Physical ZIP', 'Latitude', 'Longitude']).agg({
    'Full Name': ', '.join,
    'Phone': lambda x: ', '.join(x.dropna()) if x.dropna().any() else pd.NA,
    'Homestead': lambda x: 'YES' if 'YES' in x.tolist() else 'NO',
    'Ownername': lambda x: 'YES' if 'YES' in x.tolist() else 'NO'
}).reset_index()

df = df.groupby(['House #', 'N/S/E/W', 'Street', 'Apt #', 'Physical City', 'Physical State', 'Physical ZIP', 'Latitude', 'Longitude']).agg({'Full Name': ', '.join, 'Phone': lambda x: ', '.join(x.dropna()) if x.dropna().any() else pd.NA, 'Homestead': 'first', 'Ownername': 'first'}).reset_index()

# After the aggregation step
df['Notes'] = df.apply(lambda row: row['Full Name'] + ' (homestead match)' if row['Homestead'] == 'YES' else '', axis=1)
df['Notes'] = df.apply(lambda row: row['Full Name'] + ' (owner name match)' if row['Ownername'] == 'YES' else '', axis=1)

df = df[['Full Name', 'House #', 'N/S/E/W', 'Street', 'Physical City', 'Physical State', 'Physical ZIP', 'Apt #', 'Phone', 'Latitude', 'Longitude', 'Notes']]


df.to_csv('output.csv', index=False)
