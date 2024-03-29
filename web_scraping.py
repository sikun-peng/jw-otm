import requests
import random
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from constant import USER_AGENT_NUM, WILLIAMSON_COUNTY_ZIP, WILLIAMSON_COUNTY_BASE_URL, TRAVIS_COUNTY_ZIP, PROXY_LIST

def generate_user_agent(k):
    agent_list = []
    # Create an instance of the UserAgent class
    ua = UserAgent()

    # Generate and output k random user-agent strings
    for _ in range(k):
        agent_list.append(ua.random)
    return agent_list


def check_homestead_williamson(street_name, first_name, last_name, current_row, total_rows):
    base_url = WILLIAMSON_COUNTY_BASE_URL + "/Proxy-WilliamsonTax//Search/Properties/"
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


    agent_list = generate_user_agent(USER_AGENT_NUM)

    headers = {'User-Agent': random.choice(agent_list)}

    try:
        proxy = {'http': random.choice(PROXY_LIST)}
        response = requests.get(base_url, params=params, headers=headers, proxies=proxy)
        print(headers)
        print(proxy)
        if response.status_code != 200:
            print(f"status_code: {response.status_code} - {response.json()}")
            return False, False

        data = response.json()

        if not data["ResultList"]:
            print(f"Row {current_row}/{total_rows}: Property not found: {street_name}")
            return False, False

        property_quick_ref_id = data["ResultList"][0]["PropertyQuickRefID"]
        party_quick_ref_id = data["ResultList"][0]["PartyQuickRefID"]

        details_url = f"{WILLIAMSON_COUNTY_BASE_URL}/Property-Detail/PropertyQuickRefID/{property_quick_ref_id}/PartyQuickRefID/{party_quick_ref_id}#"

        response = requests.get(details_url, headers=headers, proxies=proxy)
        if response.status_code != 200:
            print(f"status_code: {response.status_code} - {response.json()}")
            return False, False

        soup = BeautifulSoup(response.content, 'html.parser')
        exemptions = soup.find('td', string='Exemptions')
        owner_name = soup.find('td', string='Owner Name')
        
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

def homestead_check(df):
    for index, row in df.iterrows():
        zip_code = str(row['Physical ZIP'])
        if zip_code in WILLIAMSON_COUNTY_ZIP:
            address = row['Physical Address'] + ', ' + row['Physical City'] + ', ' + str(row['Physical ZIP'])
            homestead_value, ownername_value = check_homestead_williamson(address, row['First Name'], row['Last Name'], index + 1, len(df))
            if homestead_value:
                df.at[index, 'Homestead'] = 'YES'
            if ownername_value:
                df.at[index, 'Ownername'] = 'YES'
        else:
            print(f"Row {index + 1}/{len(df)}: Skipped - Not in Williamson County")
        time.sleep(random.uniform(5, 10))
    return df