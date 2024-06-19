import pandas as pd
import re

def redefine_job_levels(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv, low_memory=False)

    # Define the mapping for job levels
    job_level_mapping = {
        'G-1': 'Entry-level',
        'G-2': 'Entry-level',
        'G-3': 'Entry-level',
        'G-4': 'Entry-level',
        'G-5': 'Entry-level',
        'G-6': 'Mid-level',
        'G-7': 'Mid-level',
        'G-8': 'Mid-level',
        'G-9': 'Mid-level',
        'G-10': 'Mid-level',
        'G-11': 'Advanced-level',
        'G-12': 'Advanced-level',
        'G-13': 'Advanced-level',
        'G-14': 'Advanced-level',
        'G-15': 'Advanced-level'
    }

    # Apply the mapping to the 'job_level' column
    df['job_level'] = df['grade'].map(job_level_mapping)

    # Dynamic categorization based on job title keywords
    def categorize_job_title(title):
        title = title.lower()
        if re.search(r'\b(intern|junior|entry|assistant|trainee)\b', title):
            return 'Entry-level'
        elif re.search(r'\b(mid|senior|lead|manager|specialist)\b', title):
            return 'Mid-level'
        elif re.search(r'\b(director|vp|vice president|chief|head|principal)\b', title):
            return 'Advanced-level'
        else:
            return 'Unknown'

    # Apply dynamic categorization to job titles
    df['dynamic_job_level'] = df['job_title'].apply(categorize_job_title)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Updated job levels saved to {output_csv}")

if __name__ == "__main__":
    input_csv = './data/preprocessed_job_listings.csv'
    output_csv = './data/preprocessed_job_listings_updated.csv'
    redefine_job_levels(input_csv, output_csv)
