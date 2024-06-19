import requests
from bs4 import BeautifulSoup

def scrape_job_listings(url):
    """
    Scrape job listings from the given URL and return a list of job details.

    Args:
        url (str): The URL of the job listings page to scrape.

    Returns:
        list: A list of dictionaries containing job details.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    job_listings = []

    # Example: Extract job titles and descriptions from the page
    for job_element in soup.find_all('div', class_='job-listing'):
        title = job_element.find('h2', class_='job-title').text.strip()
        description = job_element.find('div', class_='job-description').text.strip()

        job_listings.append({
            'title': title,
            'description': description
        })

    return job_listings

if __name__ == "__main__":
    url = "https://example.com/jobs"
    job_listings = scrape_job_listings(url)
    for job in job_listings:
        print(f"Job Title: {job['title']}")
        print(f"Description: {job['description']}")
        print("-" * 40)
