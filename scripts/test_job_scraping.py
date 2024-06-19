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
    job_listings = scrape_job_listings(mock_html, title_selector, description_selector)

    # Print job listings for debugging
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
    job_listings = scrape_job_listings(mock_html, title_selector, description_selector)

    # Print job listings for debugging
    print("Scraped job listings with error:", job_listings)

    # Expected results
    expected_job_listings = [
        {
            'title': 'Software Engineer',
            'description': 'Develop and maintain software applications.'
        }
    ]

    assert job_listings == expected_job_listings

if __name__ == "__main__":
    pytest.main()
