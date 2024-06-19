import requests
from bs4 import BeautifulSoup

def scrape_job_listings(url, title_selector, description_selector):
    """
    Scrape job listings from the given URL and return a list of job details.

    Args:
        url (str): The URL of the job listings page to scrape.
        title_selector (str): The CSS selector for job titles.
        description_selector (str): The CSS selector for job descriptions.

    Returns:
        list: A list of dictionaries containing job details.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    job_listings = []

    # Extract job titles and descriptions from the page
    for job_element in soup.select(title_selector):
        try:
            title = job_element.text.strip()
            description = job_element.select_one(description_selector).text.strip()
        except AttributeError:
            print("Error parsing job element, skipping...")
            continue

        job_listings.append({
            'title': title,
            'description': description
        })

    return job_listings

if __name__ == "__main__":
    # Mock data for testing
    mock_html = """
    <html>
    <body>
        <div class="job-listing">
            <h2 class="job-title">Software Engineer</h2>
            <div class="job-description">Develop and maintain software applications.</div>
        </div>
        <div class="job-listing">
            <h2 class="job-title">Data Scientist</h2>
            <div class="job-description">Analyze and interpret complex data sets.</div>
        </div>
    </body>
    </html>
    """
    soup = BeautifulSoup(mock_html, 'html.parser')
    job_listings = []
    title_selector = "h2.job-title"
    description_selector = "div.job-description"
    for job_element in soup.select(title_selector):
        try:
            title = job_element.text.strip()
            description = job_element.select_one(description_selector).text.strip()
        except AttributeError:
            print("Error parsing job element, skipping...")
            continue

        job_listings.append({
            'title': title,
            'description': description
        })

    for job in job_listings:
        print(f"Job Title: {job['title']}")
        print(f"Description: {job['description']}")
        print("-" * 40)
