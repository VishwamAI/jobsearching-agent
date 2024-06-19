import pandas as pd

def preprocess_job_listings(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Select relevant columns
    df = df[['Title Name', 'Grade', 'Jurisdictional Classification', 'Negotiating Unit', 'Job Level', 'Agency Description']]

    # Rename columns for clarity
    df.rename(columns={
        'Title Name': 'job_title',
        'Grade': 'grade',
        'Jurisdictional Classification': 'jurisdictional_classification',
        'Negotiating Unit': 'negotiating_unit',
        'Job Level': 'job_level',
        'Agency Description': 'agency_description'
    }, inplace=True)

    # Save the preprocessed data to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Preprocessed data saved to {output_csv}")

if __name__ == "__main__":
    input_csv = '../data/title_and_salary_listing.csv'
    output_csv = '../data/preprocessed_job_listings.csv'
    preprocess_job_listings(input_csv, output_csv)
