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

We are using AtoZ database as “source of truth” to find mandarin speakers in the local community.

Some local libraries, such as, Austin Public Library, offer free access to AtoZ Database https://library.austintexas.gov/virtual/atozdatabases

https://library.austintexas.gov/mylibrarycard
You can apply a library card for free if you live within Austin city limit or apply an ecard with a fee for those do not reside in the city limit.
![Image](https://drive.google.com/uc?id=1KW_udYMSmOpb1Lc-mzvUkjpJRaOz0s3i)



Then we will be prompted to the page below
![Image](https://drive.google.com/uc?id=16gaNGdvTGvp6yYkdptHmvgPM4BZ8U14E)

We mainly use two filter in this case, zip code and name

Zip code can allow one or multiple values, but you might want to click “Update Count” and get a reasonable number of address (You can export a maximum of 1000 address at a time).


For name field, we are focusing on using the most commonly used last names in mandarin

Liang,Yu,Cao,Meng,Cui,Xiong,Kang,Tan,Dai,Xiao,Cai,Wang,Mao,Zheng,Shi,Kong,Qiu,Hong,He,Zhong,Wu,Yang,Qin,Shao,Hu,Xia,Lai,Gao,Du,Liu,Niu,Dong,Huang,Jin,Zeng,Lu,Bai,Guo,Hao,Fan,Ren,Chang,Gong,Feng,Xue,Fang,Liao,Deng,Han,Hou,Luo,Xie,Duan,Cheng,Shen,Song,Ye,Sun,Chen,Yuan,Li,Lin,Pan,Zou,Yin,Zhang,Jiang,Fu,Peng,Yao,Zhu,Su,Jia,Tian,Ding,Zhao,Lei,Gu,Ma,Tang,Wan,Xu,Qian,Yan,Zhou,Wei

You can click the dropdown to view 100 records per page, and select maximum of 1000 entries by clicking 10 pages.
![Image](https://drive.google.com/uc?id=15eX-BN3vF7hcRxsA0h357q0nzaxGSv_y)


![Image](https://drive.google.com/uc?id=1KosDSd5Ad5dZQi8LqXaGUWwHG3STNuvE)



The csv format with Custom detail should include
- First Name
- Last Name
- Physical Address
- Physical City
- Physical State
- Physical ZIP
- Phone
- Latitude
- Longitude

![Image](https://drive.google.com/uc?id=1Pn_Qog6Af_QWytBZUM1kWWWZzHuTfKf7)


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