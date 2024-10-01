import pandas as pd

# Load the Excel file
file_path = 'orig.xlsx'
df = pd.read_excel(file_path)

# Fill forward to handle merged cells or missing values
df.fillna(method='ffill', inplace=True)

# Save the cleaned data to a new CSV file
output_path = 'current_inventory.csv'
df.to_csv(output_path, index=False)
