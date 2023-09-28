# Importing required libraries
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import csv
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

        ###################################### Data_Extraction - Start ################################

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
    
    # Perform data cleansing on each DataFrame
    df['NumberOfTrailersAuthorised'] = df['NumberOfTrailersAuthorised'].fillna(0)
    
    # Add more data cleansing steps here if needed
    df['DirectorOrPartner'].fillna('Name (not available)', inplace=True)
    df['DirectorOrPartner'] = df['DirectorOrPartner'].replace('(director)', 'Name(director)')

    # Change the date format from DD/MM/YYYY to YYYY/MM/DD hh/mm
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

        ###################################### Data_Extraction - END ######################################

        ###################################### MYSQL_Connection - Start ###################################

# Open the CSV file
with open('Data/concatenated_data.csv', 'r', encoding='utf-8') as csvfile:

    # Create a reader object
    reader = csv.reader(csvfile, delimiter=',')

    # Skip header
    next(reader, None)

    # Iterate over the rows in the CSV file
    for row in reader:

        # Create a connection to the MySQL database
        conn = mysql.connector.connect(host="localhost", port='3306', user="root", password='Karan@786', database='levo_transport')
        cursor = conn.cursor()

        # Storing the values of cell into the local variables
        geographic_region = row[0].strip()
        licence_number = row[1].strip()
        licence_type = row[2].strip()
        operator_name = row[3].strip()
        operator_type = row[4].strip()
        correspondence_address = row[5].strip()
        OCAddress = row[6].strip()
        transport_manager = row[7].strip()
        number_of_vehicles_authorised = row[8].strip()
        number_of_trailers_authorised = row[9].strip()
        vehicles_specified = row[10].strip()
        trailers_specified = row[11].strip()
        director_or_partner = row[12].strip()
        license_status = row[13].strip()
        continuation_date = row[14].strip()
        company_reg_number = row[15].strip()

        ###################################### geographicregionmaster ###################################
        # Check if the value exists in the geographicregionmaster table
        cursor.execute('SELECT ID FROM geographicregionmaster WHERE Name = %s', (geographic_region,))
        result = cursor.fetchone()

        # If the value does not exist, insert it into the table & get the latest inserted primary key.
        if result is None:
            cursor.execute('INSERT INTO geographicregionmaster (Name) VALUES (%s)', (geographic_region,))
            conn.commit()
            geographic_region = cursor.lastrowid
           
        else:
            geographic_region = result[0]
        ###################################### geographicregionmaster - ENDS ############################
   
        ###################################### licence_type_master ######################################
        cursor.execute('SELECT ID FROM licence_type_master WHERE Name = %s', (licence_type,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO licence_type_master (Name) VALUES (%s)', (licence_type,))
            conn.commit()
            licence_type = cursor.lastrowid
            
        else:
            licence_type = result[0]
        ###################################### licence_type_master - ENDS ###############################

        ###################################### licence_status_master ####################################
        cursor.execute('SELECT ID FROM license_status_master WHERE Name = %s', (license_status,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO license_status_master (Name) VALUES (%s)', (license_status,))
            conn.commit()
            license_status = cursor.lastrowid
        else:
            license_status = result[0]
        
        ###################################### license_status_master - ENDS #############################

        ###################################### operatormaster ###########################################
        cursor.execute('SELECT ID FROM operatormaster WHERE Name = %s', (operator_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO operatormaster (Name, Operator_Type, Correspodence_Address, OCAddress, Company_Reg_No) VALUES (%s, %s, %s, %s, %s)', (operator_name, operator_type, correspondence_address, OCAddress, company_reg_number,))
            conn.commit()
            operator_name = cursor.lastrowid
        else:
            operator_name = result[0]
        ###################################### operatormaster - ENDS ####################################

        ###################################### operator_user ############################################
        if director_or_partner:
            parts = director_or_partner.split("(", 1)
            name_part = parts[0].strip()
            role_part = parts[1].rstrip(")").strip()

        cursor.execute('SELECT ID FROM operator_user WHERE Name = %s AND Role = %s AND FK_Operator_Master = %s', (name_part, role_part, operator_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO operator_user (Name, Role, FK_Operator_Master) VALUES (%s, %s, %s)', (name_part, role_part, operator_name,))
            conn.commit()
            name_part = cursor.lastrowid
        else:
            name_part = result[0]
        ###################################### operator_user - ENDS #####################################
   
        ###################################### licence_details ##########################################
        cursor.execute('INSERT INTO licence_details (licence_number, Transport_Manager, Number_Of_Vehicles_Authorised, Number_Of_Trailers_Authorised, Vehicles_Specified, Trailers_Specified, Continuation_Date, FK_Geographic_Region, FK_Licence_Type, FK_License_Status, FK_Operator_User, FK_Operator_Master) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (licence_number, transport_manager, number_of_vehicles_authorised, number_of_trailers_authorised, vehicles_specified, trailers_specified, continuation_date, geographic_region, licence_type, license_status, name_part, operator_name,))
        conn.commit()
        ###################################### licence_details - ENDS ###################################

        # Close the cursor object
        cursor.close()

        # Close the connection to the MySQL database
        conn.close()

        ###################################### MYSQL_Connection - END ###################################
        ###################################### Data_Visulisation - Start ################################

data = pd.read_csv('Data\concatenated_data.csv')

# Cleanse data by removing duplicates
df_cleaned = data.drop_duplicates()

# Split the data into datasets for each license and each registered company
license_dataset = df_cleaned[['LicenceNumber', 'LicenceType', 'OperatorName', 'OperatorType',
                              'CorrespondenceAddress', 'OCAddress', 'TransportManager',
                              'NumberOfVehiclesAuthorised', 'NumberOfTrailersAuthorised',
                              'VehiclesSpecified', 'TrailersSpecified', 'DirectorOrPartner',
                              'LicenceStatus', 'ContinuationDate', 'CompanyRegNumber']]

company_dataset = df_cleaned[['OperatorName', 'CorrespondenceAddress', 'OCAddress',
                              'TransportManager', 'CompanyRegNumber']].drop_duplicates()

# Save the datasets to CSV files in the Colab environment
license_dataset.to_csv("data/license_dataset.csv", index=False)
company_dataset.to_csv("data/company_dataset.csv", index=False)

print("License dataset and company dataset saved.")


        ###################################### Data_Visulisation - Start #################################

data_visulisation = "Data_Visulisation"

licence = pd.read_csv('data/license_dataset.csv')

# Data
visual_data = licence['VehiclesSpecified']

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(visual_data, bins=300, edgecolor='black', alpha=0.7)

# Customize the plot
plt.title("Histogram of Vehicles Specified")
plt.xlabel("Number of Vehicles Specified")
plt.ylabel("Frequency")

# Save the plot as an image (e.g., PNG)
plt.savefig(os.path.join(data_visulisation, "Histogram of Vehicles Specified.png"))

# Show the plot
#plt.show()

# Plotting LicenceType (Categorical - Stacked Bar Plot)
plt.figure(figsize=(10, 6))
sns.countplot(data=licence, x='LicenceType', hue='OperatorType')
plt.xticks(rotation=45)
plt.xlabel('Licence Type')
plt.ylabel('Count')
plt.title('Licence Type Distribution by Operator Type')
plt.tight_layout()
plt.legend(title='Operator Type')
plt.savefig(os.path.join(data_visulisation, "Licence Type Distribution by Operator Type-Stacked_Barplot.png"))

# Plotting LicenceType (Categorical - Pie Chart)
plt.figure(figsize=(8, 8))
licence_type_counts = licence['LicenceType'].value_counts()
plt.pie(licence_type_counts, labels=licence_type_counts.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Licence Type Distribution')
plt.tight_layout()
plt.savefig(os.path.join(data_visulisation, "Licence Type Distribution-Pie_Chart.png"))

# Plotting VehiclesSpecified (Continuous - Box Plot)
plt.figure(figsize=(8, 6))
sns.boxplot(data=licence, y='VehiclesSpecified')
plt.ylabel('Vehicles Specified')
plt.title('Vehicles Specified Distribution')
plt.tight_layout()
plt.savefig(os.path.join(data_visulisation, "Vehicles Specified Distribution-Box_Plot.png"))

# Assuming 'licence' is your DataFrame
# Select relevant columns
data = licence[['NumberOfVehiclesAuthorised', 'VehiclesSpecified']]

# Drop rows with missing data
data.dropna(inplace=True)

# Prepare data for regression
X = data[['NumberOfVehiclesAuthorised']]
y = data['VehiclesSpecified']

# Create linear regression model
model = LinearRegression()
model.fit(X, y)

# Predicted values
y_pred = model.predict(X)

# Plot the data and regression line
plt.figure(figsize=(10, 6))
sns.scatterplot(x='NumberOfVehiclesAuthorised', y='VehiclesSpecified', data=data, label='Data')
plt.plot(X, y_pred, color='red', label='Linear Regression')
plt.xlabel('Number of Vehicles Authorised')
plt.ylabel('Vehicles Specified')
plt.title('Linear Regression: Vehicles Specified vs Number of Vehicles Authorised')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(data_visulisation, "Linear Regression Vehicles Specified vs Number of Vehicles Authorised.png"))
plt.show()

        ###################################### Data_Visulisation - End ###################################