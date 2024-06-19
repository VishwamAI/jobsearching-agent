import requests
from bs4 import BeautifulSoup

def collect_job_listings(url, title_selector, description_selector, max_pages=5):
    """
    Collect job listings from the given URL and return a list of job details.

    Args:
        url (str): The URL of the job listings page to scrape.
        title_selector (str): The CSS selector for job titles.
        description_selector (str): The CSS selector for job descriptions.
        max_pages (int): The maximum number of pages to scrape.

    Returns:
        list: A list of dictionaries containing job details.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    job_listings = []
    for page in range(1, max_pages + 1):
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        for job_listing in soup.select("article"):
            try:
                title_element = job_listing.select_one(title_selector)
                description_element = job_listing.select_one(description_selector)
                title = title_element.text.strip() if title_element else "No title provided."
                description = description_element.text.strip() if description_element else "No description provided."
                print(f"Debug: Found job listing - Title: {title}, Description: {description}")
            except AttributeError:
                print("Error parsing job element, skipping...")
                continue

            job_listings.append({
                'title': title,
                'description': description
            })

    print(f"Debug: Final job listings - {job_listings}")
    return job_listings

if __name__ == "__main__":
    # Example usage
    url = "https://www.monster.com/jobs/search/?q=Software-Engineer&where=USA"
    title_selector = "h3 a"
    description_selector = "div"
    job_listings = collect_job_listings(url, title_selector, description_selector)
    print(job_listings)
