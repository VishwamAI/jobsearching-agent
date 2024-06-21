import pytest
from bs4 import BeautifulSoup
from job_scraping import scrape_job_listings

def test_scrape_job_listings():
    # Mock HTML data for testing
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
    title_selector = "h2.job-title"
    description_selector = "div.job-description"

    # Simulate the scraping process using the mock HTML data
    job_listings = scrape_job_listings(mock_html, title_selector, description_selector, is_url=False)

    # Print job listings for debugging
    print("Parsed job descriptions:", [desc.get_text() for desc in soup.select(description_selector)])
    print("Parsed job titles:", [title.get_text() for title in soup.select(title_selector)])
    print("Job listings HTML:", soup.prettify())
    print("Scraped job listings:", job_listings)

    # Expected results
    expected_job_listings = [
        {
            'title': 'Software Engineer',
            'description': 'Develop and maintain software applications.'
        },
        {
            'title': 'Data Scientist',
            'description': 'Analyze and interpret complex data sets.'
        }
    ]

    # Print expected job listings for debugging
    print("Expected job listings:", expected_job_listings)

    assert job_listings == expected_job_listings

def test_scrape_job_listings_with_error():
    # Mock HTML data with missing description for testing error handling
    mock_html = """
    <html>
    <body>
        <div class="job-listing">
            <h2 class="job-title">Software Engineer</h2>
            <div class="job-description">Develop and maintain software applications.</div>
        </div>
        <div class="job-listing">
            <h2 class="job-title">Data Scientist</h2>
        </div>
    </body>
    </html>
    """
    soup = BeautifulSoup(mock_html, 'html.parser')
    title_selector = "h2.job-title"
    description_selector = "div.job-description"

    # Simulate the scraping process using the mock HTML data
    job_listings = scrape_job_listings(mock_html, title_selector, description_selector, is_url=False)

    # Print job listings for debugging
    print("Parsed job descriptions:", [desc.get_text() for desc in soup.select(description_selector)])
    print("Parsed job titles:", [title.get_text() for title in soup.select(title_selector)])
    print("Job listings HTML:", soup.prettify())
    print("Scraped job listings with error:", job_listings)

    # Expected results
    expected_job_listings = [
        {
            'title': 'Software Engineer',
            'description': 'Develop and maintain software applications.'
        },
        {
            'title': 'Data Scientist',
            'description': 'No description provided.'
        }
    ]

    # Print expected job listings for debugging
    print("Expected job listings with error:", expected_job_listings)

    assert job_listings == expected_job_listings

if __name__ == "__main__":
    pytest.main()