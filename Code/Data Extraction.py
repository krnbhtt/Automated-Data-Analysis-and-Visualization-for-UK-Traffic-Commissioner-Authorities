import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# URL of the webpage containing the CSV file links
webpage_url = "https://www.data.gov.uk/dataset/2a67d1ee-8f1b-43a3-8bc6-e8772d162a3c/traffic-commissioners-goods-and-public-service-vehicle-operator-licence-records"

# Create a directory to store downloaded files
if not os.path.exists("data"):
    os.makedirs("data")

# Download webpage content
response = requests.get(webpage_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all links within the webpage
all_links = soup.find_all("a", href=True)

# Filter links to find CSV file links
csv_links = [link["href"] for link in all_links if link["href"].endswith(".csv")]

# List to store cleaned DataFrames
cleaned_dfs = []

# Download CSV files, clean data, and store DataFrames
for csv_link in csv_links:
    full_csv_link = urljoin(webpage_url, csv_link).replace(" ", "%20")  # Ensure proper URL formatting
    df = pd.read_csv(full_csv_link)

    # Cleaning duplicates
    # df = df[['LicenceNumber', 'LicenceType', 'OperatorName', 'OperatorType',
    #          'CorrespondenceAddress', 'OCAddress', 'TransportManager',
    #          'NumberOfVehiclesAuthorised', 'NumberOfTrailersAuthorised',
    #          'VehiclesSpecified', 'TrailersSpecified', 'DirectorOrPartner',
    #          'LicenceStatus', 'ContinuationDate', 'CompanyRegNumber', 'ContinuationDate']]
    
    df = df.drop_duplicates()

    # Perform data cleansing on each DataFrame
    df['NumberOfTrailersAuthorised'] = df['NumberOfTrailersAuthorised'].fillna(0)
    
    # Add more data cleansing steps here needed
    df['DirectorOrPartner'].fillna('Name (not available)', inplace=True)
    df['DirectorOrPartner'] = df['DirectorOrPartner'].replace('(director)', 'Name(director)')

   #Change the date format from DD/MM/YYYY to YYYY/MM/DD hh/mm
    if len(df['ContinuationDate'].str.split("/")[0]) == 3:  # Assuming ContinuationDate is in DD/MM/YYYY format
        df['ContinuationDate'] = pd.to_datetime(df['ContinuationDate'], format='%d/%m/%Y')
        df['ContinuationDate'] = df['ContinuationDate'].dt.strftime('%Y-%m-%d %H:%M')  
    
    cleaned_dfs.append(df)

# Concatenate cleaned DataFrames
final_df = pd.concat(cleaned_dfs, ignore_index=True)

# Save concatenated DataFrame to a new CSV file
final_csv_path = os.path.join("Data", "concatenated_data.csv")
final_df.to_csv(final_csv_path, index=False)

print("Concatenated data saved to concatenated_data.csv")
