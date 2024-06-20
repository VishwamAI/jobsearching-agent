import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(filename='/home/ubuntu/jobsearching-agent/logs/extract_job_elements.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_job_elements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    job_listings = []

    results = soup.select('div[jsname="Q4LuWd"]')

    for result in results:
        try:
            job_title_elem = result.select_one('div:nth-of-type(1)')
            job_title = job_title_elem.text.strip() if job_title_elem else 'N/A'

            company_name_elem = result.select_one('div:nth-of-type(2)')
            company_name = company_name_elem.text.strip() if company_name_elem else 'N/A'

            location_elem = result.select_one('div:nth-of-type(3)')
            location = location_elem.text.strip() if location_elem else 'N/A'

            url_elem = result.select_one('a')
            url = url_elem['href'] if url_elem else 'N/A'

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
                    'url': url
                })

        except Exception as e:
            logging.warning(f"Error processing result: {e}")

    return job_listings

if __name__ == "__main__":
    # Example usage
    url = "https://www.google.com/search?q=software+engineer+jobs"
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    if response.status_code == 200:
        html_content = response.content
        job_listings = extract_job_elements(html_content)
        logging.info(f"Extracted job listings: {job_listings}")
    else:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
