import requests
from bs4 import BeautifulSoup

def scrape_job_listings(content, title_selector, description_selector, is_url=True):
    """
    Scrape job listings from the given URL or HTML content and return a list of job details.

    Args:
        content (str): The URL of the job listings page to scrape or HTML content.
        title_selector (str): The CSS selector for job titles.
        description_selector (str): The CSS selector for job descriptions.
        is_url (bool): Flag indicating whether the content is a URL or HTML content.

    Returns:
        list: A list of dictionaries containing job details.
    """
    if is_url:
        try:
            response = requests.get(content)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            html_content = response.content
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return []
    else:
        html_content = content

    soup = BeautifulSoup(html_content, 'html.parser')

    job_listings = []

    # Extract job titles and descriptions from the page
    for job_listing in soup.select("div.job-listing"):
        try:
            title_element = job_listing.select_one(title_selector)
            description_element = job_listing.select_one(description_selector)
            title = title_element.text.strip() if title_element else "No title provided."
            description = description_element.text.strip() if description_element else "No description provided."
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
    title_selector = "h2.job-title"
    description_selector = "div.job-description"
    job_listings = scrape_job_listings(mock_html, title_selector, description_selector, is_url=False)

    for job in job_listings:
        print(f"Job Title: {job['title']}")
        print(f"Description: {job['description']}")
        print("-" * 40)
