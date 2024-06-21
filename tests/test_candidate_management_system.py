import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.create_db_schema import (
    Base, Candidate, Job, Application
)
from scripts.candidate_management_system import (
    add_candidate,
    schedule_interview,
    update_interview_status,
    auto_apply_to_jobs
)
from datetime import datetime
import uuid

DATABASE_URL = "sqlite:///:memory:"

# Adding a comment to trigger CI/CD workflow
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

    def generate_unique_email(self, base_email):
        unique_id = uuid.uuid4().hex[:6]
        return f"{base_email.split('@')[0]}_{unique_id}@" \
               f"{base_email.split('@')[1]}"

    def generate_unique_phone(self, base_phone):
        unique_id = uuid.uuid4().hex[:10]
        unique_phone = f"{base_phone[:4]}{unique_id}"
        return unique_phone

    def test_add_candidate(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe@example.com"),
            self.generate_unique_phone("1234567890"), "resume.pdf",
            self.session
        )
        print(f"Candidate added: {candidate}")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(
            candidate.email.split('@')[0].startswith("john.doe"), True
        )

    def test_update_interview_status(self):
        candidate = add_candidate(
            "John", "Doe", self.generate_unique_email("john.doe8@example.com"),
            self.generate_unique_phone("1234567897"), "resume.pdf",
            self.session
        )
        print(f"Candidate added: {candidate}")
        interview_schedule = schedule_interview(
            candidate.id, 1, datetime.now(), "Scheduled", self.session
        )
        updated_interview = update_interview_status(
            interview_schedule.id, "Completed", self.session
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
            "John", "Doe", self.generate_unique_email("john.doe9@example.com"),
            self.generate_unique_phone("1234567898"), "resume.pdf",
            self.session
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
