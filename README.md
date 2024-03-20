# jw-otm


# OTM Territory Update Process

This guide outlines the steps involved in updating the territory in OTM (Order Management System). The process includes:

- [Search & Download Contacts In The Territory](#search--download-contacts-in-the-territory)
- [Formatting CSV File](#formatting-csv-file)
- [Remove Old Address](#remove-old-address)
- [Import New Address](#import-new-address)
- [Auto Assign Addresses](#auto-assign-addresses)
- [Check Duplicates](#check-duplicates)

## Search & Download Contacts In The Territory

We utilize the AtoZ database as our "source of truth" to find Mandarin speakers in the local community. Access to AtoZ Database can be obtained through certain local libraries, such as the Austin Public Library. You can apply for a library card for free if you live within the Austin city limit, or apply for an e-card with a fee if you reside outside the city limit.

Once registered, access AtoZ Database and utilize its advanced search options to find people or businesses in a particular category, using filters such as zip code and name. Commonly used last names in Mandarin are used for the name filter.

Instructions for accessing and downloading data from AtoZ Database are detailed within the document.

## Formatting CSV File

CSV files downloaded from AtoZ Database may require formatting. Two methods are outlined for this:

### Method 1: Manual Formatting (For Non-Python Users)

- Combine CSV files if necessary.
- Merge first names and last names with addresses.
- Insert new fields for "Full Name" and "Address Count".
- Sort entries based on address count.
- Manually merge duplicate addresses.
- Split full addresses into subsets.
- Replace 'N/A' phone numbers.
- Check and save the CSV file.

### Method 2: Using Python

Python scripts are provided to automate the formatting process. Instructions for combining CSV files and formatting using Python are outlined.

## Remove Old Address

Scan notes for all unconfirmed addresses and uncheck if notes are important or DNC.

## Import New Address

No specific instructions provided in this document. Likely involves uploading the formatted CSV file into OTM.

## Auto Assign Addresses

Details regarding auto-assigning addresses are not provided in this document.

## Check Duplicates

Process for checking duplicates within the territory is not elaborated in this document.

---

This README provides an overview of the territory update process in OTM. For detailed instructions on each step, refer to the respective sections above.