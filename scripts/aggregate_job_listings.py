import os
import pandas as pd
from job_scraping import scrape_job_listings

def aggregate_job_listings(sources):
    """
    Aggregate job listings from multiple sources into a single DataFrame.

    Args:
        sources (list): A list of dictionaries containing source information.
                        Each dictionary should have the keys 'content', 'title_selector', 'description_selector', and 'is_url'.

    Returns:
        pd.DataFrame: A DataFrame containing aggregated job listings.
    """
    all_job_listings = []

    for source in sources:
        job_listings = scrape_job_listings(
            content=source['content'],
            title_selector=source['title_selector'],
            description_selector=source['description_selector'],
            is_url=source['is_url']
        )
        all_job_listings.extend(job_listings)

    # Convert the list of job listings to a DataFrame
    job_listings_df = pd.DataFrame(all_job_listings)

    return job_listings_df

if __name__ == "__main__":
    # Example sources for testing
    sources = [
        {
            'content': 'https://example.com/jobs',
            'title_selector': 'h2.job-title',
            'description_selector': 'div.job-description',
            'is_url': True
        },
        {
            'content': """
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
            """,
            'title_selector': 'h2.job-title',
            'description_selector': 'div.job-description',
            'is_url': False
        }
    ]

    job_listings_df = aggregate_job_listings(sources)
    print(job_listings_df)
