from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.create_db_schema import Candidate, Job, Application, Base, Watchlist, InterviewSchedule
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

DATABASE_URL = 'sqlite:///../data/jobsearching_agent.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def add_candidate(first_name, last_name, email, phone=None, resume=None):
    try:
        candidate = Candidate(first_name=first_name, last_name=last_name, email=email, phone=phone, resume=resume)
        session.add(candidate)
        session.flush()
        session.commit()
        return candidate
    except SQLAlchemyError as e:
        session.rollback()
        if "UNIQUE constraint failed: candidates.email" in str(e):
            print(f"Error adding candidate: Email {email} already exists.")
        elif "UNIQUE constraint failed: candidates.phone" in str(e):
            print(f"Error adding candidate: Phone {phone} already exists.")
        else:
            print(f"Error adding candidate: {e}")
        return None

def get_candidate_by_email(email):
    try:
        return session.query(Candidate).filter_by(email=email).first()
    except SQLAlchemyError as e:
        print(f"Error retrieving candidate: {e}")
        return None

def update_candidate(candidate_id, **kwargs):
    try:
        candidate = session.query(Candidate).filter_by(id=candidate_id).first()
        if candidate:
            for key, value in kwargs.items():
                setattr(candidate, key, value)
            session.commit()
        return candidate
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating candidate: {e}")
        return None

def delete_candidate(candidate_id):
    try:
        candidate = session.query(Candidate).filter_by(id=candidate_id).first()
        if candidate:
            session.delete(candidate)
            session.commit()
        return candidate
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting candidate: {e}")
        return None

def add_to_watchlist(candidate_id, job_id):
    try:
        watchlist_entry = Watchlist(candidate_id=candidate_id, job_id=job_id, added_date=datetime.now())
        session.add(watchlist_entry)
        session.commit()
        return watchlist_entry
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding to watchlist: {e}")
        return None

def remove_from_watchlist(candidate_id, job_id):
    try:
        watchlist_entry = session.query(Watchlist).filter_by(candidate_id=candidate_id, job_id=job_id).first()
        if watchlist_entry:
            session.delete(watchlist_entry)
            session.commit()
        return watchlist_entry
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error removing from watchlist: {e}")
        return None

def schedule_interview(candidate_id, job_id, interview_date, status):
    try:
        interview_schedule = InterviewSchedule(candidate_id=candidate_id, job_id=job_id, interview_date=interview_date, status=status)
        session.add(interview_schedule)
        session.commit()
        return interview_schedule
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error scheduling interview: {e}")
        return None

def update_interview_status(interview_id, status):
    try:
        interview_schedule = session.query(InterviewSchedule).filter_by(id=interview_id).first()
        if interview_schedule:
            interview_schedule.status = status
            session.commit()
        return interview_schedule
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating interview status: {e}")
        return None

def auto_apply_to_jobs(candidate_id, job_listings, session):
    try:
        print(f"Querying candidate with ID: {candidate_id}")
        candidate = session.query(Candidate).filter_by(id=candidate_id).first()
        if not candidate:
            print(f"Candidate with ID {candidate_id} not found.")
            return None
        print(f"Candidate found: {candidate}")

        for job in job_listings:
            job_id = job.get('id')
            if not job_id:
                print(f"Job ID not found for job: {job}")
                continue
            print(f"Processing job ID: {job_id}")

            application = Application(
                candidate_id=candidate_id,
                job_id=job_id,
                application_date=datetime.now(),
                status='Pending'
            )
            session.add(application)
            print(f"Application created for job ID {job_id} with status 'Pending', Application ID: {application.id}")

            # Simulate application submission process
            # This is where you would add code to fill out and submit the application form
            # For now, we'll just print a message
            print(f"Applied to job ID {job_id} for candidate ID {candidate_id}")

            # Update application status to 'Submitted'
            application.status = 'Submitted'

        session.flush()  # Ensure all objects are persisted and IDs are generated
        for application in session.query(Application).filter_by(candidate_id=candidate_id).all():
            print(f"Application ID after flush: {application.id}, Job ID: {application.job_id}, Status: {application.status}")
        session.commit()
        print(f"Application status updated to 'Submitted' for all jobs")

        # Log the state of the database after commit
        committed_applications = session.query(Application).filter_by(candidate_id=candidate_id).all()
        for application in committed_applications:
            print(f"Committed Application ID: {application.id}, Job ID: {application.job_id}, Status: {application.status}")

        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during auto-application process: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    new_candidate = add_candidate("John", "Doe", "john.doe@example.com", "1234567890", "resume.pdf")
    if new_candidate:
        print(f"Added candidate: {new_candidate.first_name} {new_candidate.last_name}")

    candidate = get_candidate_by_email("john.doe@example.com")
    if candidate:
        print(f"Retrieved candidate: {candidate.first_name} {candidate.last_name}")

    updated_candidate = update_candidate(candidate.id, phone="0987654321")
    if updated_candidate:
        print(f"Updated candidate phone: {updated_candidate.phone}")

    deleted_candidate = delete_candidate(candidate.id)
    if deleted_candidate:
        print(f"Deleted candidate: {candidate.first_name} {candidate.last_name}")

    # Example usage of watchlist and interview scheduling
    watchlist_entry = add_to_watchlist(candidate.id, 1)
    if watchlist_entry:
        print(f"Added to watchlist: Candidate ID {watchlist_entry.candidate_id}, Job ID {watchlist_entry.job_id}")

    removed_watchlist_entry = remove_from_watchlist(candidate.id, 1)
    if removed_watchlist_entry:
        print(f"Removed from watchlist: Candidate ID {removed_watchlist_entry.candidate_id}, Job ID {removed_watchlist_entry.job_id}")

    interview_schedule = schedule_interview(candidate.id, 1, datetime.now(), "Scheduled")
    if interview_schedule:
        print(f"Scheduled interview: Candidate ID {interview_schedule.candidate_id}, Job ID {interview_schedule.job_id}, Status {interview_schedule.status}")

    updated_interview = update_interview_status(interview_schedule.id, "Completed")
    if updated_interview:
        print(f"Updated interview status: Interview ID {updated_interview.id}, Status {updated_interview.status}")
