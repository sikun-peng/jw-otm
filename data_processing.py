import pandas as pd
import re

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
        if part.lower() in ["apt", "unit", "ste", "#"]:
            apt_match = re.search(r'\d+', rest_address_parts[i+1])  # Extract number from Apt/Unit string
            if apt_match:
                apt_number = apt_match.group()
            rest_address = ' '.join(rest_address_parts[:i])  # Remove Apt/Unit and its number from rest_address
            break
    
    street = rest_address.strip()
    
    return house_number, direction, street, apt_number

def preprocess_data(df):
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']
    df['Homestead'] = ""
    df['Ownername'] = ""
    return df

def aggregate_data(df):
    df['House #'], df['N/S/E/W'], df['Street'], df['Apt #'] = zip(*df['Physical Address'].apply(split_address))
    df['Phone'] = df['Phone'].replace('N/A', pd.NA)
    df = df.groupby(['House #', 'N/S/E/W', 'Street', 'Apt #', 'Physical City','Physical State', 'Physical ZIP', 'Latitude', 'Longitude']).agg({
        'Full Name': ', '.join,
        'Phone': lambda x: ', '.join(x.dropna()) if x.dropna().any() else pd.NA,
        'Homestead': lambda x: 'YES' if 'YES' in x.tolist() else 'NO',
        'Ownername': lambda x: 'YES' if 'YES' in x.tolist() else 'NO'
    }).reset_index()
    df = df.groupby(['House #', 'N/S/E/W', 'Street', 'Apt #', 'Physical City', 'Physical State', 'Physical ZIP', 'Latitude', 'Longitude']).agg({
        'Full Name': ', '.join, 'Phone': lambda x: ', '.join(x.dropna()) if x.dropna().any() else pd.NA, 'Homestead': 'first', 'Ownername': 'first'}).reset_index()
    # After the aggregation step
    df['Notes'] = df.apply(lambda row: 'homestead match' if row['Homestead'] == 'YES' else '', axis=1)
    #df['Notes'] = df.apply(lambda row: row['Notes'] + 'owner name match' if row['Ownername'] == 'YES' else '', axis=1)

    df = df[['Full Name', 'House #', 'N/S/E/W', 'Street', 'Physical City', 'Physical State', 'Physical ZIP', 'Apt #', 'Phone', 'Latitude', 'Longitude', 'Notes']]

    return df