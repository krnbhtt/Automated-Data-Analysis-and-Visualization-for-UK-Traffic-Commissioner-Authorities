import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import pandas as pd
import os

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
#plt.show()
