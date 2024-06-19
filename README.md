# jobsearching-agent

## Overview

This repository contains the code for the jobsearching-agent, an advanced AI job searching agent that analyzes job listings from various portals to match job roles with users' skills and experience. The agent is designed to be free and legal, similar to "whitecarrot.io".

## Features

- Web scraping
- Natural Language Processing (NLP)
- Summarization
- Model training and evaluation
- CI/CD workflows
- Virtual interview scheduling
- Application tracking system
- Job watchlist management

## How to Earn the Galaxy Brain Badge on GitHub

To encourage community engagement, you can earn the Galaxy Brain badge on GitHub by following these steps:

1. Answer at least 2 discussions.
2. You cannot mark your own answers to your own questions. They have to be marked by another user.
3. Discussions should be in a public repository.
4. Be aware of a current bug observed by some users whereby marking your own answers can prevent you from getting the badge instead.

For more details, refer to the [GitHub Community discussion](https://github.com/orgs/community/discussions/18293).

## Getting Started

To get started with the jobsearching-agent, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/VishwamAI/jobsearching-agent.git
   cd jobsearching-agent
   ```

2. Set up the virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the tests to ensure everything is set up correctly:
   ```bash
   pytest
   ```

## Using the Web Scraping Script

The `scrape_job_listings.py` script can be used to scrape job listings from a job board and save them to a CSV file. Follow these steps to use the script:

1. Update the `job_board_url` variable in the script with the URL of the job board you want to scrape.
2. Run the script:
   ```bash
   python scripts/scrape_job_listings.py
   ```
3. The scraped job listings will be saved to `data/job_listings.csv`.

## Advanced Features

### Virtual Interview Scheduling

The jobsearching-agent includes a feature to schedule and conduct virtual interviews. This feature integrates with video conferencing tools to facilitate seamless interview scheduling.

### Application Tracking System

The agent provides a dashboard to track the progress of job applications through various stages such as shortlisted, applied, CV sent, interviewing, and offer.

### Job Watchlist Management

Candidates can add jobs to a watchlist and manage their job search process effectively.

## Contributing

We welcome contributions to the jobsearching-agent project. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a clear message.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Note

This is a minor update to trigger the CI/CD pipeline.
