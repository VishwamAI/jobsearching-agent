import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
import os

from scripts.create_db_schema import (
    Base, Candidate, Job, Watchlist, InterviewSchedule
)
from scripts.candidate_management import (
    add_candidate,
    get_candidate_by_email,
    update_candidate,
    delete_candidate,
    add_to_watchlist,
    remove_from_watchlist,
    schedule_interview,
    update_interview_status,
)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")


class TestCandidateManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f"Using DATABASE_URL in tests: {DATABASE_URL}")
        print("Inode number of database file at test setup:")
        os.system(f"ls -i {DATABASE_URL.split('///')[-1]}")
        print("Absolute path of database file at test setup:")
        os.system(f"readlink -f {DATABASE_URL.split('///')[-1]}")
        print("Contents of DATABASE_URL environment variable:")
        os.system("echo $DATABASE_URL")
        print("Checking if database file exists and is accessible:")
        os.system(f"ls -la {DATABASE_URL.split('///')[-1]}")
        cls.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Diagnostic print statements
        from sqlalchemy import inspect
        inspector = inspect(cls.engine)
        tables = inspector.get_table_names()
        print(f"Tables in the database at test setup: {tables}")

        if not inspector.has_table('candidates'):
            raise RuntimeError(
                "Candidates table was not created successfully."
            )

        # Additional diagnostics
        print(f"Database URL: {DATABASE_URL}")
        from sqlalchemy.sql import text

        with cls.engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            tables = result.fetchall()
            print("Tables in the database after setup:", tables)
            # Print the contents of the candidates table
            result = connection.execute(text("SELECT * FROM candidates;"))
            candidates = result.fetchall()
            print("Contents of the candidates table after setup:", candidates)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test class.")
        Base.metadata.drop_all(cls.engine)
        cls.session.close()
        print("Database tables dropped and session closed.")

    def setUp(self):
        self.session.query(Candidate).delete()
        self.session.query(Job).delete()
        self.session.query(Watchlist).delete()
        self.session.query(InterviewSchedule).delete()
        self.session.commit()
        # Diagnostic print to check session status and table accessibility
        print("Session status:")
        with self.engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            tables = result.fetchall()
            print("Tables in the database before test:", tables)
            result = connection.execute(text("SELECT * FROM candidates;"))
            candidates = result.fetchall()
            print("Contents of the candidates table before test:")
            print(candidates)

    def generate_unique_phone(self, base_phone):
        unique_id = uuid.uuid4().hex[:10]
        unique_phone = f"{base_phone[:4]}{unique_id}"
        print(f"Generated unique phone: {unique_phone}")
        return unique_phone

    def generate_unique_email(self, base_email):
        unique_id = uuid.uuid4().hex[:6]
        unique_email = (
            f"{base_email.split('@')[0]}{unique_id}@{base_email.split('@')[1]}"
        )
        print(f"Generated unique email: {unique_email}")
        return unique_email

    def test_add_candidate(self):
        try:
            unique_email = self.generate_unique_email("john.doe@example.com")
            candidate = add_candidate(
                "John", "Doe", unique_email,
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            self.assertIsNotNone(candidate)
            self.assertEqual(candidate.first_name, "John")
            self.assertEqual(candidate.last_name, "Doe")
            self.assertEqual(candidate.email, unique_email)
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_add_candidate: {e}")
            raise

    def test_get_candidate_by_email(self):
        try:
            unique_email = self.generate_unique_email("john.doe@example.com")
            add_candidate(
                "John", "Doe", unique_email,
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            candidate = get_candidate_by_email(unique_email)
            self.assertIsNotNone(candidate)
            self.assertEqual(candidate.first_name, "John")
            self.assertEqual(candidate.last_name, "Doe")
            self.assertEqual(candidate.email, unique_email)
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_get_candidate_by_email: {e}")
            raise

    def test_update_candidate(self):
        try:
            candidate = add_candidate(
                "John", "Doe", self.generate_unique_email("john.doe@example.com"),
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            self.assertIsNotNone(candidate)
            new_phone = self.generate_unique_phone("0987654321")
            updated_candidate = update_candidate(candidate.id, phone=new_phone)
            self.assertIsNotNone(updated_candidate)
            self.assertEqual(updated_candidate.phone, new_phone)
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_update_candidate: {e}")
            raise

    def test_delete_candidate(self):
        try:
            unique_email = self.generate_unique_email("john.doe@example.com")
            candidate = add_candidate(
                "John", "Doe", unique_email,
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            deleted_candidate = delete_candidate(candidate.id)
            self.assertIsNotNone(deleted_candidate)
            self.assertIsNone(get_candidate_by_email(unique_email))
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_delete_candidate: {e}")
            raise

    def test_add_to_watchlist(self):
        try:
            candidate = add_candidate(
                "John", "Doe", self.generate_unique_email("john.doe@example.com"),
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            job = Job(
                title="Software Engineer",
                description="Develop software",
                location="Remote"
            )
            self.session.add(job)
            self.session.commit()
            watchlist_entry = add_to_watchlist(candidate.id, job.id)
            self.assertIsNotNone(watchlist_entry)
            self.assertEqual(watchlist_entry.candidate_id, candidate.id)
            self.assertEqual(watchlist_entry.job_id, job.id)
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_add_to_watchlist: {e}")
            raise

    def test_remove_from_watchlist(self):
        try:
            candidate = add_candidate(
                "John", "Doe", self.generate_unique_email("john.doe@example.com"),
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            job = Job(
                title="Software Engineer",
                description="Develop software",
                location="Remote"
            )
            self.session.add(job)
            self.session.commit()
            add_to_watchlist(candidate.id, job.id)
            removed_watchlist_entry = remove_from_watchlist(candidate.id, job.id)
            self.assertIsNotNone(removed_watchlist_entry)
            self.assertEqual(removed_watchlist_entry.candidate_id, candidate.id)
            self.assertEqual(removed_watchlist_entry.job_id, job.id)
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_remove_from_watchlist: {e}")
            raise

    def test_schedule_interview(self):
        try:
            candidate = add_candidate(
                "John", "Doe", self.generate_unique_email("john.doe@example.com"),
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            job = Job(
                title="Software Engineer",
                description="Develop software",
                location="Remote"
            )
            self.session.add(job)
            self.session.commit()
            interview_schedule = schedule_interview(
                candidate.id, job.id, datetime.now(), "Scheduled"
            )
            self.assertIsNotNone(interview_schedule)
            self.assertEqual(interview_schedule.candidate_id, candidate.id)
            self.assertEqual(interview_schedule.job_id, job.id)
            self.assertEqual(interview_schedule.status, "Scheduled")
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_schedule_interview: {e}")
            raise

    def test_update_interview_status(self):
        try:
            candidate = add_candidate(
                "John", "Doe", self.generate_unique_email("john.doe@example.com"),
                self.generate_unique_phone("1234567890"), "resume.pdf"
            )
            job = Job(
                title="Software Engineer",
                description="Develop software",
                location="Remote"
            )
            self.session.add(job)
            self.session.commit()
            interview_schedule = schedule_interview(
                candidate.id, job.id, datetime.now(), "Scheduled"
            )
            updated_interview = update_interview_status(
                interview_schedule.id, "Completed"
            )
            self.assertIsNotNone(updated_interview)
            self.assertEqual(updated_interview.status, "Completed")
        except Exception as e:
            self.session.rollback()
            print(f"Error in test_update_interview_status: {e}")
            raise


if __name__ == "__main__":
    unittest.main()
