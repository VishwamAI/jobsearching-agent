import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.create_db_schema import (
    Base, Candidate, Watchlist, InterviewSchedule, Job, Application
)
from scripts.candidate_management_system import (
    add_candidate,
    get_candidate_by_email,
    update_candidate,
    delete_candidate,
    add_to_watchlist,
    remove_from_watchlist,
    schedule_interview,
    update_interview_status,
    auto_apply_to_jobs
)

import uuid


def generate_unique_email(base_email):
    unique_id = uuid.uuid4().hex[:6]
    return f"{base_email.split('@')[0]}_{unique_id}@{base_email.split('@')[1]}"


def generate_unique_phone(base_phone):
    unique_id = uuid.uuid4().hex[:10]
    unique_phone = f"{base_phone[:4]}{unique_id}"
    return unique_phone


DATABASE_URL = (
    'sqlite:////home/ubuntu/jobsearching-agent/data/test_jobsearching_agent.db'
)


class TestCandidateManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(DATABASE_URL)
        print(f"Using DATABASE_URL: {DATABASE_URL}")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test class.")
        Base.metadata.drop_all(cls.engine)
        cls.session.close()
        print("Database tables dropped and session closed.")

    def setUp(self):
        print("Setting up the test case.")
        self.session.query(Candidate).delete()
        self.session.query(Watchlist).delete()
        self.session.query(InterviewSchedule).delete()
        self.session.query(Job).delete()
        self.session.query(Application).delete()
        self.session.commit()
        print("Database tables cleared.")
        remaining_candidates = self.session.query(Candidate).all()
        print(f"Remaining candidates after setup: {remaining_candidates}")
        remaining_watchlists = self.session.query(Watchlist).all()
        print(f"Remaining watchlists after setup: {remaining_watchlists}")
        remaining_interviews = self.session.query(InterviewSchedule).all()
        print(f"Remaining interviews after setup: {remaining_interviews}")
        remaining_jobs = self.session.query(Job).all()
        print(f"Remaining jobs after setup: {remaining_jobs}")
        remaining_applications = self.session.query(Application).all()
        print(f"Remaining applications after setup: {remaining_applications}")

    def test_add_candidate(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe@example.com"),
            generate_unique_phone("1234567890"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(
            candidate.email.split('@')[0].startswith("john.doe"), True
        )

    def test_get_candidate_by_email(self):
        email = generate_unique_email("john.doe2@example.com")
        add_candidate(
            "John", "Doe", email, generate_unique_phone("1234567891"),
            "resume.pdf"
        )
        self.session.commit()
        candidate = get_candidate_by_email(email)
        print(f"Candidate retrieved: {candidate}")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")

    def test_update_candidate(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe3@example.com"),
            generate_unique_phone("1234567892"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        updated_phone = generate_unique_phone("0987654321")
        updated_candidate = update_candidate(
            candidate.id, phone=updated_phone
        )
        self.assertIsNotNone(updated_candidate)
        self.assertEqual(updated_candidate.phone, updated_phone)

    def test_delete_candidate(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe4@example.com"),
            generate_unique_phone("1234567893"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        deleted_candidate = delete_candidate(candidate.id)
        self.assertIsNotNone(deleted_candidate)
        self.assertIsNone(get_candidate_by_email("john.doe4@example.com"))

    def test_add_to_watchlist(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe5@example.com"),
            generate_unique_phone("1234567894"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        watchlist_entry = add_to_watchlist(candidate.id, 1)
        self.assertIsNotNone(watchlist_entry)
        self.assertEqual(watchlist_entry.candidate_id, candidate.id)
        self.assertEqual(watchlist_entry.job_id, 1)

    def test_remove_from_watchlist(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe6@example.com"),
            generate_unique_phone("1234567895"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        add_to_watchlist(candidate.id, 1)
        removed_watchlist_entry = remove_from_watchlist(candidate.id, 1)
        self.assertIsNotNone(removed_watchlist_entry)
        self.assertIsNone(
            self.session.query(Watchlist).filter_by(
                candidate_id=candidate.id, job_id=1
            ).first()
        )

    def test_schedule_interview(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe7@example.com"),
            generate_unique_phone("1234567896"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        interview_schedule = schedule_interview(
            candidate.id, 1, datetime.now(), "Scheduled"
        )
        self.assertIsNotNone(interview_schedule)
        self.assertEqual(interview_schedule.candidate_id, candidate.id)
        self.assertEqual(interview_schedule.job_id, 1)
        self.assertEqual(interview_schedule.status, "Scheduled")

    def test_update_interview_status(self):
        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe8@example.com"),
            generate_unique_phone("1234567897"), "resume.pdf"
        )
        print(f"Candidate added: {candidate}")
        interview_schedule = schedule_interview(
            candidate.id, 1, datetime.now(), "Scheduled"
        )
        updated_interview = update_interview_status(
            interview_schedule.id, "Completed"
        )
        self.assertIsNotNone(updated_interview)
        self.assertEqual(updated_interview.status, "Completed")

    def test_auto_apply_to_jobs(self):
        print(f"Session ID before adding candidate: {id(self.session)}")
        print("Candidates before adding new candidate:")
        candidates_before = self.session.query(Candidate).all()
        for candidate in candidates_before:
            print(candidate)

        candidate = add_candidate(
            "John", "Doe", generate_unique_email("john.doe9@example.com"),
            generate_unique_phone("1234567898"), "resume.pdf"
        )
        self.session.flush()
        self.assertIsNotNone(
            candidate, "Candidate was not added successfully."
        )
        self.assertIsNotNone(
            candidate.id, "Candidate ID is None after addition."
        )
        print(f"Candidate added: {candidate}")
        print(f"Candidate ID: {candidate.id}")
        print(f"Session ID after adding candidate: {id(self.session)}")

        print("Candidates after adding new candidate:")
        candidates_after = self.session.query(Candidate).all()
        for candidate in candidates_after:
            print(candidate)

        job1 = Job(
            id=1, title='Software Engineer', description='Job Description A',
            location='Location A'
        )
        job2 = Job(
            id=2, title='Data Scientist', description='Job Description B',
            location='Location B'
        )
        self.session.add(job1)
        self.session.add(job2)
        self.session.commit()
        print(f"Job 1 ID: {job1.id}, Job 2 ID: {job2.id}")
        job_listings = [
            {'id': 1, 'title': 'Software Engineer'},
            {'id': 2, 'title': 'Data Scientist'}
        ]
        print(
            f"Session ID before calling auto_apply_to_jobs: {id(self.session)}"
        )
        result = auto_apply_to_jobs(candidate.id, job_listings, self.session)
        self.assertTrue(result)

        # Query the applications using the same session
        applications = self.session.query(Application).filter_by(
            candidate_id=candidate.id
        ).all()
        self.assertEqual(len(applications), 2)
        for application in applications:
            self.assertEqual(application.status, 'Submitted')


if __name__ == "__main__":
    unittest.main()
