import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_job_listings(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def preprocess_job_data(job_data):
    processed_data = []
    for job in job_data:
        job_title = job.get('title', '')
        job_description = job.get('description', '')
        job_requirements = job.get('requirements', '')
        job_qualifications = job.get('qualifications', '')

        processed_data.append({
            'title': job_title,
            'description': job_description,
            'requirements': job_requirements,
            'qualifications': job_qualifications
        })

    return pd.DataFrame(processed_data)

def main():
    api_url = "https://api.example.com/job_listings"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    job_data = fetch_job_listings(api_url, headers)
    if job_data:
        job_df = preprocess_job_data(job_data)
        job_df.to_csv('job_listings.csv', index=False)
        print("Job listings data saved to job_listings.csv")

if __name__ == "__main__":
    main()
