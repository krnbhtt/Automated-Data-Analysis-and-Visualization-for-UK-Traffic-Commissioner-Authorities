import pandas as pd

data = pd.read_csv('Data\concatenated_data.csv')

# Cleanse data by removing duplicates
df_cleaned = data.drop_duplicates()

# Split the data into datasets for each license and each registered company
license_dataset = df_cleaned[['LicenceNumber', 'LicenceType',
                              'NumberOfVehiclesAuthorised', 'NumberOfTrailersAuthorised',
                              'VehiclesSpecified', 'TrailersSpecified',
                              'LicenceStatus', 'ContinuationDate']]

company_dataset = df_cleaned[['GeographicRegion', 'OperatorName', 'OperatorType', 'CorrespondenceAddress','OCAddress',
                              'OCAddress','TransportManager', 'DirectorOrPartner', 'CompanyRegNumber']]

# Save the datasets to CSV files in the Colab environment
license_dataset.to_csv("data/license_dataset.csv", index=False)
company_dataset.to_csv("data/company_dataset.csv", index=False)

print("License dataset and company dataset saved.")
