import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import os
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(filename='job_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def google_job_search(query, num_pages=5):
    job_listings = []
    base_url = "https://www.google.com/search?q="

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for page in range(num_pages):
        start = page * 10
        url = f"{base_url}{query}&start={start}"
        logging.info(f"Fetching URL: {url}")

        try:
            driver.get(url)
            time.sleep(5)  # Wait for the page to load

            results = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Jobs list"] div[tabindex="-1"]')
            for result in results:
                try:
                    job_title_elem = result.find_element(By.CSS_SELECTOR, 'h2 span')
                    company_name_elem = result.find_element(By.CSS_SELECTOR, 'div[data-attrid="title"]')
                    location_elem = result.find_element(By.CSS_SELECTOR, 'div[data-attrid="subtitle"]')
                    url_elem = result.find_element(By.CSS_SELECTOR, 'a')

                    job_title = job_title_elem.text if job_title_elem else 'N/A'
                    company_name = company_name_elem.text if company_name_elem else 'N/A'
                    location = location_elem.text if location_elem else 'N/A'
                    url = url_elem.get_attribute('href') if url_elem else 'N/A'

                    # Log the extracted elements
                    logging.info(f"Extracted job title: {job_title}")
                    logging.info(f"Extracted company name: {company_name}")
                    logging.info(f"Extracted location: {location}")
                    logging.info(f"Extracted URL: {url}")

                    # Exclude irrelevant elements
                    if job_title != 'N/A' and company_name != 'N/A' and location != 'N/A' and url.startswith("http") and "More results" not in job_title and "Try again" not in job_title:
                        job_listings.append({
                            'job_title': job_title,
                            'company_name': company_name,
                            'location': location,
                            'url': url,
                            'job_level': categorize_job_title(job_title)
                        })

                except Exception as e:
                    logging.warning(f"Error processing result: {e}")

            time.sleep(2)  # Sleep to avoid being blocked

        except Exception as e:
            logging.error(f"Error fetching URL: {url} - {e}")
            continue

    driver.quit()
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
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        existing_df = pd.read_csv(filename)
        new_df = pd.DataFrame(job_listings)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(filename, index=False)
    else:
        df = pd.DataFrame(job_listings)
        df.to_csv(filename, index=False)
    logging.info(f"Job listings saved to {filename}")

def save_to_json(job_listings, filename='../data/job_listings.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            existing_data = json.load(json_file)
        existing_data.extend(job_listings)
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
    else:
        with open(filename, 'w') as json_file:
            json.dump(job_listings, json_file, indent=4)
    logging.info(f"Job listings saved to {filename}")

def save_json_to_csv(json_filename, csv_filename):
    with open(json_filename, 'r') as json_file:
        job_listings = json.load(json_file)
    save_to_csv(job_listings, csv_filename)

if __name__ == "__main__":
    query = "software engineer jobs"
    job_listings = google_job_search(query)
    save_to_json(job_listings)
    save_json_to_csv('../data/job_listings.json', '../data/google_job_listings.csv')
