import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_features(input_csv, output_csv):
    # Read the preprocessed CSV file
    df = pd.read_csv(input_csv)

    # Convert relevant columns to strings
    df['job_title'] = df['job_title'].astype(str)
    df['jurisdictional_classification'] = df['jurisdictional_classification'].astype(str)
    df['negotiating_unit'] = df['negotiating_unit'].astype(str)
    df['agency_description'] = df['agency_description'].astype(str)

    # Combine relevant text columns into a single column for feature extraction
    df['combined_text'] = df['job_title'] + ' ' + df['jurisdictional_classification'] + ' ' + df['negotiating_unit'] + ' ' + df['agency_description']

    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=1000)

    # Fit and transform the combined text data
    X = vectorizer.fit_transform(df['combined_text'])

    # Convert the TF-IDF matrix to a DataFrame
    feature_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

    # Add the grade and job level columns to the feature DataFrame
    feature_df['grade'] = df['grade']
    feature_df['job_level'] = df['job_level']

    # Save the feature DataFrame to a new CSV file
    feature_df.to_csv(output_csv, index=False)
    print(f"Features extracted and saved to {output_csv}")

if __name__ == "__main__":
    input_csv = '../data/preprocessed_job_listings.csv'
    output_csv = '../data/job_listings_features.csv'
    extract_features(input_csv, output_csv)
