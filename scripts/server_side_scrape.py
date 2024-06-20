import requests
from lxml import html
import pandas as pd
import os
import logging
import json

# Configure logging
logging.basicConfig(filename='/home/ubuntu/jobsearching-agent/logs/job_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def server_side_scrape(query, num_pages=5):
    job_listings = []
    base_url = "https://www.google.com/search?q="

    for page in range(num_pages):
        start = page * 10
        url = f"{base_url}{query}&start={start}"
        logging.info(f"Fetching URL: {url}")

        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            if response.status_code != 200:
                logging.error(f"Failed to retrieve page {page}. Status code: {response.status_code}")
                break

            html_content = response.content
            logging.info(f"HTML content: {html_content[:5000]}")  # Log the first 5000 characters of the HTML content
            tree = html.fromstring(html_content)
            results = tree.xpath('//div[@jsname="Q4LuWd"]')

            for result in results:
                try:
                    job_title_elem = result.xpath('.//*[contains(@class, "BjJfJf") or contains(@class, "whuFyc") or contains(@class, "uLAgob") or contains(@class, "uVxte") or contains(@class, "qQ1Cnf")]')
                    job_title = job_title_elem[0].text.strip() if job_title_elem else 'N/A'

                    company_name_elem = result.xpath('.//*[contains(@class, "mWcf0e") or contains(@class, "eDGqNd") or contains(@class, "k62gjb") or contains(@class, "vNEEBe")]')
                    company_name = company_name_elem[0].text.strip() if company_name_elem else 'N/A'

                    location_elem = result.xpath('.//*[contains(@class, "JMgW3") or contains(@class, "ruhZ8e") or contains(@class, "Qk80Jf")]')
                    location = location_elem[0].text.strip() if location_elem else 'N/A'

                    url_elem = result.xpath('.//a')
                    url = url_elem[0].get('href') if url_elem else 'N/A'

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
    job_listings = server_side_scrape(query)
    save_to_json(job_listings)
    save_json_to_csv('../data/job_listings.json', '../data/google_job_listings.csv')
