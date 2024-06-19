from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db_schema import Candidate, Job, Application, Base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = 'sqlite:///../data/jobsearching_agent.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def add_candidate(first_name, last_name, email, phone=None, resume=None):
    try:
        candidate = Candidate(first_name=first_name, last_name=last_name, email=email, phone=phone, resume=resume)
        session.add(candidate)
        session.commit()
        return candidate
    except SQLAlchemyError as e:
        session.rollback()
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
