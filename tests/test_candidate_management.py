import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

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

DATABASE_URL = "sqlite:///:memory:"


class TestCandidateManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.session.close()

    def setUp(self):
        self.session.query(Candidate).delete()
        self.session.query(Job).delete()
        self.session.query(Watchlist).delete()
        self.session.query(InterviewSchedule).delete()
        self.session.commit()

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
        unique_email = self.generate_unique_email("john.doe@example.com")
        candidate = add_candidate(
            "John", "Doe", unique_email,
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(candidate.email, unique_email)

    def test_get_candidate_by_email(self):
        unique_email = self.generate_unique_email("john.doe@example.com")
        add_candidate(
            "John", "Doe", unique_email,
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        candidate = get_candidate_by_email(unique_email, session=self.session)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(candidate.email, unique_email)

    def test_update_candidate(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        self.assertIsNotNone(candidate)
        new_phone = self.generate_unique_phone("0987654321")
        updated_candidate = update_candidate(candidate.id, phone=new_phone, session=self.session)
        self.assertIsNotNone(updated_candidate)
        self.assertEqual(updated_candidate.phone, new_phone)

    def test_delete_candidate(self):
        unique_email = self.generate_unique_email("john.doe@example.com")
        candidate = add_candidate(
            "John", "Doe", unique_email,
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        deleted_candidate = delete_candidate(candidate.id, session=self.session)
        self.assertIsNotNone(deleted_candidate)
        self.assertIsNone(get_candidate_by_email(unique_email, session=self.session))

    def test_add_to_watchlist(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        job = Job(
            title="Software Engineer",
            description="Develop software",
            location="Remote"
        )
        self.session.add(job)
        self.session.commit()
        watchlist_entry = add_to_watchlist(candidate.id, job.id, session=self.session)
        self.assertIsNotNone(watchlist_entry)
        self.assertEqual(watchlist_entry.candidate_id, candidate.id)
        self.assertEqual(watchlist_entry.job_id, job.id)

    def test_remove_from_watchlist(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        job = Job(
            title="Software Engineer",
            description="Develop software",
            location="Remote"
        )
        self.session.add(job)
        self.session.commit()
        add_to_watchlist(candidate.id, job.id, session=self.session)
        removed_watchlist_entry = remove_from_watchlist(candidate.id, job.id, session=self.session)
        self.assertIsNotNone(removed_watchlist_entry)
        self.assertEqual(removed_watchlist_entry.candidate_id, candidate.id)
        self.assertEqual(removed_watchlist_entry.job_id, job.id)

    def test_schedule_interview(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        job = Job(
            title="Software Engineer",
            description="Develop software",
            location="Remote"
        )
        self.session.add(job)
        self.session.commit()
        interview_schedule = schedule_interview(
            candidate.id, job.id, datetime.now(), "Scheduled", session=self.session
        )
        self.assertIsNotNone(interview_schedule)
        self.assertEqual(interview_schedule.candidate_id, candidate.id)
        self.assertEqual(interview_schedule.job_id, job.id)
        self.assertEqual(interview_schedule.status, "Scheduled")

    def test_update_interview_status(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            session=self.session
        )
        job = Job(
            title="Software Engineer",
            description="Develop software",
            location="Remote"
        )
        self.session.add(job)
        self.session.commit()
        interview_schedule = schedule_interview(
            candidate.id, job.id, datetime.now(), "Scheduled", session=self.session
        )
        updated_interview = update_interview_status(
            interview_schedule.id, "Completed", session=self.session
        )
        self.assertIsNotNone(updated_interview)
        self.assertEqual(updated_interview.status, "Completed")


if __name__ == "__main__":
    unittest.main()
