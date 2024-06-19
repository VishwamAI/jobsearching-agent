import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

            for result in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
                job_title = result.get_text()
                job_listings.append({'job_title': job_title})

            time.sleep(2)  # Sleep to avoid being blocked

        except requests.RequestException as e:
            logging.error(f"Error fetching URL: {url} - {e}")
            continue

    return job_listings

def save_to_csv(job_listings, filename='data/google_job_listings.csv'):
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)
    logging.info(f"Job listings saved to {filename}")

if __name__ == "__main__":
    query = "software engineer jobs"
    job_listings = google_job_search(query)
    save_to_csv(job_listings)
