import pandas as pd
import random
import time
from data_processing import preprocess_data, aggregate_data, split_address
from web_scraping import homestead_check
from constants import A_TO_Z_CSV_PATH, ENABLE_HOMESTEAD_CHECK, ENABLE_VOTER_REGISTRATION_CHECK

def process_csv(a_to_z_csv_path = A_TO_Z_CSV_PATH,
        enable_homestead_check = ENABLE_HOMESTEAD_CHECK,
        enable_voter_registration_check = None,
        voter_registration_csv_path = None,
        enable_use_otm_file = None,
        otm_csv_path = None,
        output_path = "",
        output_file_name = "" ):
    print(f"a_to_z_csv_path:{a_to_z_csv_path}")
    print(f"enable_homestead_check:{enable_homestead_check}")
    print(f"enable_voter_registration_check:{enable_voter_registration_check}")
    print(f"voter_registration_csv_path:{voter_registration_csv_path}")
    print(f"enable_use_otm_file:{enable_use_otm_file}")

    output_file_path = output_path + "/" + output_file_name
    print(f"output_file_path:{output_file_path}")


    # Read the CSV file
    df = pd.read_csv(a_to_z_csv_path)

    # Preprocess data
    df = preprocess_data(df)

    # Perform homestead check
    if enable_homestead_check:
        df = homestead_check(df)
    else:
        print("Homestead check disabled, move on to data formatting")

    # Aggregate data
    df = aggregate_data(df)

    # Save output
    print(f"File saved in {output_file_path}")
    df.to_csv(output_file_path, index=False)
