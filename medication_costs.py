import pandas as pd
import re
import os

def clean_csv(input_file):
    try:
        # Remove quotation marks from the input file path
        input_file = input_file.strip('"')

        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(input_file)
        
        # Check if the DataFrame is empty
        if df.empty:
            print("Error: Input file is empty.")
            return

        # Step 1: Remove £ signs from 'Sum of AccountSales'
        df['Sum of AccountSales'] = df['Sum of AccountSales'].str.replace('£', '')

        # Step 2: Remove single or double spaces from 'paymentRefOperation'
        df['paymentRefOperation'] = df['paymentRefOperation'].astype(str).apply(lambda x: re.sub(r'\s+', ' ', x))

        # Step 3: Replace 'MedicationCosts' with 'Medication Costs' in all column headers
        df.columns = df.columns.str.replace('MedicationCosts', 'Medication Costs')

        # Step 4: Change date format in 'Date' to 'YYYY-MM-DD HH:MM:SS'
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

        # Step 5: Remove the bottom line that includes the total by deleting entire row
        df = df[df['pukReference'] != 'total']

        # Step 6: Convert all values in 'pukReference' column to uppercase and remove leading/trailing spaces
        df['pukReference'] = df['pukReference'].str.upper().str.strip()

        # Step 7: Drop the last row
        df.drop(df.tail(1).index, inplace=True)

        # Determine output file path
        output_file = os.path.splitext(input_file)[0] + '_cleaned.csv'

        # Write the modified DataFrame back to a CSV file
        df.to_csv(output_file, index=False)
        print(f"Cleaning completed. Output file saved as '{output_file}'.")

    except FileNotFoundError:
        print("Error: Input file not found.")
    except pd.errors.EmptyDataError:
        print("Error: Input file is empty.")
    except Exception as e:
        print(f"An error occurred during data cleaning: {e}")

if __name__ == "__main__":
    # Input file path as user input
    input_file = input("Enter the path of the input CSV file: ")

    clean_csv(input_file)
