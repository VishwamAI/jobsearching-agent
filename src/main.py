import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Append the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.create_db_schema import Base, Candidate
from scripts.candidate_management_system import (
    add_candidate,
    get_candidate_by_email,
    update_candidate,
    delete_candidate,
    add_to_watchlist,
    remove_from_watchlist,
    schedule_interview,
    update_interview_status,
)
from scripts.redefine_job_levels import redefine_job_levels

DATABASE_URL = "sqlite:///../data/jobsearching_agent.db"


def initialize_database():
    if not os.path.exists("../data"):
        os.makedirs("../data")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


def main():
    initialize_database()

    # Example usage of candidate management functions
    print("Adding a new candidate...")
    candidate = add_candidate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        resume="path/to/resume.pdf",
    )
    if candidate:
        print(f"Candidate added: {candidate.first_name} {candidate.last_name}")

    print("Retrieving candidate by email...")
    candidate = get_candidate_by_email(email="john.doe@example.com")
    if candidate:
        print(f"Candidate retrieved: {candidate.first_name} {candidate.last_name}")

    print("Updating candidate information...")
    candidate = update_candidate(candidate_id=candidate.id, phone="0987654321")
    if candidate:
        print(
            f"Candidate updated: {candidate.first_name} {candidate.last_name}, "
            f"Phone: {candidate.phone}"
        )

    print("Deleting candidate...")
    candidate = delete_candidate(candidate_id=candidate.id)
    if candidate:
        print(f"Candidate deleted: {candidate.first_name} {candidate.last_name}")

    # Example usage of watchlist management functions
    print("Adding candidate to watchlist...")
    watchlist_entry = add_to_watchlist(candidate_id=candidate.id, job_id=1)
    if watchlist_entry:
        print(f"Candidate added to watchlist for job ID: {watchlist_entry.job_id}")

    print("Removing candidate from watchlist...")
    removed_watchlist_entry = remove_from_watchlist(candidate_id=candidate.id, job_id=1)
    if removed_watchlist_entry:
        print(f"Candidate removed from watchlist for job ID: {removed_watchlist_entry.job_id}")

    # Example usage of interview scheduling functions
    print("Scheduling an interview for candidate...")
    interview_schedule = schedule_interview(candidate_id=candidate.id, job_id=1, interview_date=datetime.now(), status="Scheduled")
    if interview_schedule:
        print(f"Interview scheduled for candidate ID: {interview_schedule.candidate_id} for job ID: {interview_schedule.job_id}")

    print("Updating interview status...")
    updated_interview = update_interview_status(interview_id=interview_schedule.id, status="Completed")
    if updated_interview:
        print(f"Interview status updated to: {updated_interview.status}")

    # Apply job level categorization
    print("Applying job level categorization...")
    input_csv = '../data/preprocessed_job_listings.csv'
    df = redefine_job_levels(input_csv)
    output_csv = '../data/preprocessed_job_listings_updated.csv'
    df.to_csv(output_csv, index=False)
    print(f"Updated job levels saved to {output_csv}")


if __name__ == "__main__":
    main()
