import pandas as pd

# Load the CSV and Excel files using relative paths
americas_data = pd.read_csv('data/americas.csv')
emea_data = pd.read_csv('data/emea.csv')
forecast_data = pd.read_csv('data/forecast.csv')
asia_data = pd.read_excel('data/asia.xlsx')

# Display the first few rows of each DataFrame
print("Americas Data:")
print(americas_data.head())

print("\nEMEA Data:")
print(emea_data.head())

print("\nAsia Data:")
print(asia_data.head())

print("\nForecast Data:")
print(forecast_data.head())

# Check for missing values and data types
print("Americas Data Info:")
print(americas_data.info())

print("\nEMEA Data Info:")
print(emea_data.info())

print("\nAsia Data Info:")
print(asia_data.info())

print("\nForecast Data Info:")
print(forecast_data.info())

# Drop 'Unnamed: 0' columns from each dataset if they exist
americas_data = americas_data.drop(columns=['Unnamed: 0'], errors='ignore')
emea_data = emea_data.drop(columns=['Unnamed: 0'], errors='ignore')
asia_data = asia_data.drop(columns=['Unnamed: 0'], errors='ignore')
forecast_data = forecast_data.drop(columns=['Unnamed: 0'], errors='ignore')

# Calculate the percentage of missing values in 'MATERIAL_NBR' for each DataFrame
americas_missing = americas_data['MATERIAL_NBR'].isnull().mean() * 100
emea_missing = emea_data['MATERIAL_NBR'].isnull().mean() * 100
asia_missing = asia_data['MATERIAL_NBR'].isnull().mean() * 100

print(f"Missing 'MATERIAL_NBR' in Americas: {americas_missing:.2f}%")
print(f"Missing 'MATERIAL_NBR' in EMEA: {emea_missing:.2f}%")
print(f"Missing 'MATERIAL_NBR' in Asia: {asia_missing:.2f}%")

# Standardize column names for MATERIAL_NBR across datasets
americas_data.rename(columns={'MATERIAL_NBR': 'MATERIAL_NUMBER'}, inplace=True)
emea_data.rename(columns={'MATERIAL_NBR': 'MATERIAL_NUMBER'}, inplace=True)
asia_data.rename(columns={'MATERIAL_NBR': 'MATERIAL_NUMBER'}, inplace=True)

# For Forecast data, make sure it's already consistent
forecast_data.rename(columns={'MATERIAL_NUMBER': 'MATERIAL_NUMBER'}, inplace=True)

# Inspect the unique values in the 'PERIOD' column for each dataset
print("Unique PERIOD values in Americas Data:")
print(americas_data['PERIOD'].unique())

print("\nUnique PERIOD values in EMEA Data:")
print(emea_data['PERIOD'].unique())

print("\nUnique PERIOD values in Asia Data:")
print(asia_data['PERIOD'].unique())

# Function to standardize 'PERIOD' format
def standardize_period_format(df, region):
    if region == 'Americas':
        # For Americas Data, add '.12' to represent December (end of the year)
        df['PERIOD'] = df['PERIOD'].astype(str) + '.12'
    else:
        # Standardize to 'yyyy.mm' format for EMEA and Asia
        df['PERIOD'] = df['PERIOD'].apply(lambda x: f"{int(str(x).split('.')[0]):04d}.{int(str(x).split('.')[1]):02d}" if '.' in str(x) else f"{int(x):04d}.01")
    return df

# Apply the function to each dataset with the correct region
americas_data = standardize_period_format(americas_data, 'Americas')
emea_data = standardize_period_format(emea_data, 'EMEA')
asia_data = standardize_period_format(asia_data, 'Asia')

# Create a 'YEAR' column by extracting the year from the 'PERIOD' column
americas_data['YEAR'] = americas_data['PERIOD'].str[:4].astype(int)
emea_data['YEAR'] = emea_data['PERIOD'].str[:4].astype(int)
asia_data['YEAR'] = asia_data['PERIOD'].str[:4].astype(int)

# Inspect unique values in COMMERCIAL_COUNTRY_NAME
print("Unique country names in Americas Data:")
print(americas_data['COMMERCIAL_COUNTRY_NAME'].unique())

print("\nUnique country names in EMEA Data:")
print(emea_data['COMMERCIAL_COUNTRY_NAME'].unique())

print("\nUnique country names in Asia Data:")
print(asia_data['COMMERCIAL_COUNTRY_NAME'].unique())

# Country name mapping to standardize country names
country_name_mapping = {
    'Canadá': 'Canada',
    'México': 'Mexico',
    'Brasil': 'Brazil',
    'UK': 'United Kingdom',
    'U.S.A': 'United States',
    'Estados Unidos': 'United States',
    'España': 'Spain',
    # Add more mappings as needed based on your data
}

# Apply the mapping to standardize the country names in all datasets
americas_data['COMMERCIAL_COUNTRY_NAME'] = americas_data['COMMERCIAL_COUNTRY_NAME'].replace(country_name_mapping)
emea_data['COMMERCIAL_COUNTRY_NAME'] = emea_data['COMMERCIAL_COUNTRY_NAME'].replace(country_name_mapping)
asia_data['COMMERCIAL_COUNTRY_NAME'] = asia_data['COMMERCIAL_COUNTRY_NAME'].replace(country_name_mapping)

# Verify the standardization
print("Standardized country names in Americas Data:")
print(americas_data['COMMERCIAL_COUNTRY_NAME'].unique())

# Combine sales data from different regions
combined_sales = pd.concat([americas_data, emea_data, asia_data], axis=0, ignore_index=True)

# Merge combined_sales with forecast_data on 'MATERIAL_NUMBER', 'YEAR', 'COMMERCIAL_COUNTRY_NAME', and 'COMMERCIAL_SEGMENT'
final_data = pd.merge(combined_sales, forecast_data,
                      left_on=['MATERIAL_NUMBER', 'YEAR', 'COMMERCIAL_COUNTRY_NAME'],
                      right_on=['MATERIAL_NUMBER', 'YEAR', 'CMRCL_CNTRY_DSC'],
                      how='inner')

# Display the first few rows of the merged DataFrame
print("Combined Sales and Forecast Data:")
print(final_data.head())

# Check for missing values in the merged DataFrame
missing_values = final_data.isnull().sum()

# Display columns with missing values
print("Columns with missing values:")
print(missing_values[missing_values > 0])

# Display a summary of missing values
print(f"\nTotal missing values in merged data: {missing_values.sum()}")
