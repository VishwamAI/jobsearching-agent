# jobsearching-agent
[![Python application](https://github.com/VishwamAI/jobsearching-agent/actions/workflows/python-app.yml/badge.svg)](https://github.com/VishwamAI/jobsearching-agent/actions/workflows/python-app.yml)
## Overview

This repository contains the code for the jobsearching-agent, an advanced AI job searching agent that analyzes job listings from various portals to match job roles with users' skills and experience. The agent is designed to be free and legal, similar to "whitecarrot.io".

## Features

- **Job Searching**: The agent can search for job listings across various platforms using customizable search criteria.
- **Job Categorization**: The agent categorizes job listings based on predefined categories to help users find relevant jobs quickly.
- **Auto-Applying**: The agent can automatically apply to job listings that match the user's criteria. This feature includes:
  - **Resume Submission**: Automatically submits the user's resume to job listings.
  - **Cover Letter Customization**: Customizes cover letters based on the job description and user profile.
  - **Application Tracking**: Tracks the status of job applications and provides updates to the user.
  - **Error Handling**: Includes robust error handling to ensure that applications are submitted correctly and retries in case of failures.
  - For more details, see the "Advanced Features" section below.

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

## Using the Candidate Management System

The `candidate_management_system.py` script can be used to manage candidate data, including adding, retrieving, updating, and deleting candidates, as well as managing the watchlist and scheduling interviews. Follow these steps to use the script:

1. Add a new candidate:
   ```bash
   python scripts/candidate_management_system.py add_candidate "John" "Doe" "john.doe@example.com" "1234567890" "resume.pdf"
   ```

2. Retrieve a candidate by email:
   ```bash
   python scripts/candidate_management_system.py get_candidate_by_email "john.doe@example.com"
   ```

3. Update a candidate's information:
   ```bash
   python scripts/candidate_management_system.py update_candidate 1 phone="0987654321"
   ```

4. Delete a candidate:
   ```bash
   python scripts/candidate_management_system.py delete_candidate 1
   ```

5. Add a job to the watchlist:
   ```bash
   python scripts/candidate_management_system.py add_to_watchlist 1 1
   ```

6. Remove a job from the watchlist:
   ```bash
   python scripts/candidate_management_system.py remove_from_watchlist 1 1
   ```

7. Schedule an interview:
   ```bash
   python scripts/candidate_management_system.py schedule_interview 1 1 "2024-06-20 10:00:00" "Scheduled"
   ```

8. Update interview status:
   ```bash
   python scripts/candidate_management_system.py update_interview_status 1 "Completed"
   ```

## Advanced Features

### Virtual Interview Scheduling

The jobsearching-agent includes a feature to schedule and conduct virtual interviews. This feature integrates with video conferencing tools to facilitate seamless interview scheduling.

### Application Tracking System

The agent provides a dashboard to track the progress of job applications through various stages such as shortlisted, applied, CV sent, interviewing, and offer.

### Job Watchlist Management

Candidates can add jobs to a watchlist and manage their job search process effectively.

### Auto-Applying to Job Listings

The jobsearching-agent includes a feature to automatically apply to job listings across various online platforms. This feature has been enhanced with the following capabilities:

- **Resume Submission**: Automatically submits the user's resume to job listings that match the user's criteria.
- **Cover Letter Customization**: Customizes cover letters based on the job description and user profile, ensuring a personalized application for each job.
- **Application Tracking**: Tracks the status of job applications and provides updates to the user, including notifications for application status changes.
- **Error Handling**: Includes robust error handling to ensure that applications are submitted correctly and retries in case of failures.
- **Platform Integration**: Supports integration with multiple job platforms, allowing the agent to apply to jobs across the entire internet.
- **User Preferences**: Allows users to set preferences for job applications, such as job title, location, salary range, and more.
- **Logging and Reporting**: Provides detailed logs and reports of the auto-applying process, helping users to monitor and review their job applications.

These enhancements make the auto-applying feature more powerful and user-friendly, enabling users to efficiently apply to job listings and manage their job search process.

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
