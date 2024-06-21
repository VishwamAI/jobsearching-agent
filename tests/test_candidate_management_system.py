import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.create_db_schema import Base, Candidate, Watchlist, InterviewSchedule, Job, Application
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

DATABASE_URL = 'sqlite:///../data/test_jobsearching_agent.db'

class TestCandidateManagementSystem(unittest.TestCase):
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
        self.session.query(Watchlist).delete()
        self.session.query(InterviewSchedule).delete()
        self.session.query(Job).delete()
        self.session.query(Application).delete()
        self.session.commit()

    def test_add_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe_unique@example.com", "1234567899", "resume.pdf")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(candidate.email, "john.doe_unique@example.com")

    def test_get_candidate_by_email(self):
        add_candidate("John", "Doe", "john.doe2@example.com", "1234567891", "resume.pdf")
        candidate = get_candidate_by_email("john.doe2@example.com")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")

    def test_update_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe3@example.com", "1234567892", "resume.pdf")
        updated_candidate = update_candidate(candidate.id, phone="0987654321")
        self.assertIsNotNone(updated_candidate)
        self.assertEqual(updated_candidate.phone, "0987654321")

    def test_delete_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe4@example.com", "1234567893", "resume.pdf")
        deleted_candidate = delete_candidate(candidate.id)
        self.assertIsNotNone(deleted_candidate)
        self.assertIsNone(get_candidate_by_email("john.doe4@example.com"))

    def test_add_to_watchlist(self):
        candidate = add_candidate("John", "Doe", "john.doe5@example.com", "1234567894", "resume.pdf")
        watchlist_entry = add_to_watchlist(candidate.id, 1)
        self.assertIsNotNone(watchlist_entry)
        self.assertEqual(watchlist_entry.candidate_id, candidate.id)
        self.assertEqual(watchlist_entry.job_id, 1)

    def test_remove_from_watchlist(self):
        candidate = add_candidate("John", "Doe", "john.doe6@example.com", "1234567895", "resume.pdf")
        add_to_watchlist(candidate.id, 1)
        removed_watchlist_entry = remove_from_watchlist(candidate.id, 1)
        self.assertIsNotNone(removed_watchlist_entry)
        self.assertIsNone(self.session.query(Watchlist).filter_by(candidate_id=candidate.id, job_id=1).first())

    def test_schedule_interview(self):
        candidate = add_candidate("John", "Doe", "john.doe7@example.com", "1234567896", "resume.pdf")
        interview_schedule = schedule_interview(candidate.id, 1, datetime.now(), "Scheduled")
        self.assertIsNotNone(interview_schedule)
        self.assertEqual(interview_schedule.candidate_id, candidate.id)
        self.assertEqual(interview_schedule.job_id, 1)
        self.assertEqual(interview_schedule.status, "Scheduled")

    def test_update_interview_status(self):
        candidate = add_candidate("John", "Doe", "john.doe8@example.com", "1234567897", "resume.pdf")
        interview_schedule = schedule_interview(candidate.id, 1, datetime.now(), "Scheduled")
        updated_interview = update_interview_status(interview_schedule.id, "Completed")
        self.assertIsNotNone(updated_interview)
        self.assertEqual(updated_interview.status, "Completed")

    def test_auto_apply_to_jobs(self):
        candidate = add_candidate("John", "Doe", "john.doe9@example.com", "1234567898", "resume.pdf")
        job1 = Job(id=1, title='Software Engineer', company='Company A', location='Location A', description='Job Description A')
        job2 = Job(id=2, title='Data Scientist', company='Company B', location='Location B', description='Job Description B')
        self.session.add(job1)
        self.session.add(job2)
        self.session.commit()
        job_listings = [
            {'id': 1, 'title': 'Software Engineer'},
            {'id': 2, 'title': 'Data Scientist'}
        ]
        result = auto_apply_to_jobs(candidate.id, job_listings)
        self.assertTrue(result)
        applications = self.session.query(Application).filter_by(candidate_id=candidate.id).all()
        self.assertEqual(len(applications), 2)
        for application in applications:
            self.assertEqual(application.status, 'Submitted')

if __name__ == "__main__":
    unittest.main()
