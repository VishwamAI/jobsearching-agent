import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.create_db_schema import Base, Candidate
from scripts.candidate_management import (
    add_candidate,
    get_candidate_by_email,
    update_candidate,
    delete_candidate,
)

# Append the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


if __name__ == "__main__":
    main()
