import pandas as pd

# Define the path to the features file
features_file = '../data/job_listings_features.csv'
cleaned_features_file = '../data/job_listings_features_cleaned.csv'

# Define a function to clean the data
def clean_data(file_path):
    # Initialize an empty dataframe to hold the cleaned data
    cleaned_df = pd.DataFrame()

    # Load the data in chunks
    for chunk in pd.read_csv(file_path, chunksize=5000, low_memory=False):
        # Convert only numeric columns to numeric, coercing errors to NaN
        numeric_columns = chunk.select_dtypes(include=['number']).columns
        chunk[numeric_columns] = chunk[numeric_columns].apply(pd.to_numeric, errors='coerce')
        # Identify and handle non-numeric columns
        for column in chunk.columns:
            if chunk[column].dtype == 'object':
                # Convert non-numeric columns to numeric, coercing errors to NaN
                chunk[column] = pd.to_numeric(chunk[column], errors='coerce')
        # Drop rows with NaN values in numeric columns
        chunk.dropna(subset=numeric_columns, inplace=True)
        # Append the cleaned chunk to the cleaned dataframe
        cleaned_df = pd.concat([cleaned_df, chunk], ignore_index=True)

    # Save the cleaned data to a new CSV file
    cleaned_df.to_csv(cleaned_features_file, index=False)
    return cleaned_features_file

# Run the cleaning function
if __name__ == "__main__":
    cleaned_file_path = clean_data(features_file)
    print(f"Cleaned data saved to {cleaned_file_path}")
