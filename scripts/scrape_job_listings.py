import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def scrape_job_listings(url):
    job_listings = []
    page = 1

    while True:
        response = requests.get(url, params={'page': page})
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all('div', class_='job-listing')

        if not jobs:
            print(f"No more job listings found on page {page}.")
            break

        for job in jobs:
            try:
                job_title = job.find('h2', class_='job-title').text.strip()
                company = job.find('div', class_='company').text.strip()
                location = job.find('div', class_='location').text.strip()
                description = job.find('div', class_='description').text.strip()

                job_listings.append({
                    'job_title': job_title,
                    'company': company,
                    'location': location,
                    'description': description
                })
            except AttributeError as e:
                print(f"Error parsing job listing: {e}")
                continue

        print(f"Scraped {len(jobs)} job listings from page {page}.")
        page += 1
        time.sleep(1)  # Be polite and avoid overwhelming the server

    return job_listings

def save_job_listings(job_listings, output_file):
    df = pd.DataFrame(job_listings)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    job_board_url = 'https://example.com/jobs'
    output_file = os.path.join(os.path.dirname(__file__), '../data/job_listings.csv')

    job_listings = scrape_job_listings(job_board_url)
    save_job_listings(job_listings, output_file)
    print(f"Scraped {len(job_listings)} job listings and saved to {output_file}")
