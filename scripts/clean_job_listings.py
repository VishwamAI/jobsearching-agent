import json
import os

def clean_job_listings(json_filename):
    with open(json_filename, 'r') as json_file:
        job_listings = json.load(json_file)

    # Filter out invalid job listings
    cleaned_job_listings = [
        job for job in job_listings
        if "More results" not in job['jobTitle'] and "Try again" not in job['jobTitle']
    ]

    # Save the cleaned job listings back to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(cleaned_job_listings, json_file, indent=4)

if __name__ == "__main__":
    json_filename = '../data/job_listings.json'
    clean_job_listings(json_filename)
