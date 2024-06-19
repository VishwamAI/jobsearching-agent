import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import os
import re

# Configure logging
logging.basicConfig(filename='job_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def google_job_search(query, num_pages=5):
    job_listings = []
    base_url = "https://www.google.com/search?q="

    for page in range(num_pages):
        start = page * 10
        url = f"{base_url}{query}&start={start}"
        logging.info(f"Fetching URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for result in soup.find_all('div', class_='BjJfJf PUpOsf'):
                job_title_elem = result.find('h3')
                company_name_elem = result.find('div', class_='vNEEBe')
                location_elem = result.find('div', class_='Qk80Jf')

                job_title = job_title_elem.get_text() if job_title_elem else 'N/A'
                company_name = company_name_elem.get_text() if company_name_elem else 'N/A'
                location = location_elem.get_text() if location_elem else 'N/A'

                job_listings.append({
                    'job_title': job_title,
                    'company_name': company_name,
                    'location': location,
                    'job_level': categorize_job_title(job_title)
                })

                if not job_title_elem:
                    logging.warning(f"Missing job title for result: {result}")
                if not company_name_elem:
                    logging.warning(f"Missing company name for result: {result}")
                if not location_elem:
                    logging.warning(f"Missing location for result: {result}")

            time.sleep(2)  # Sleep to avoid being blocked

        except requests.RequestException as e:
            logging.error(f"Error fetching URL: {url} - {e}")
            continue

    return job_listings

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

def save_to_csv(job_listings, filename='../data/google_job_listings.csv'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)
    logging.info(f"Job listings saved to {filename}")

if __name__ == "__main__":
    query = "software engineer jobs"
    job_listings = google_job_search(query)
    save_to_csv(job_listings)
