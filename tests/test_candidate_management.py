import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from create_db_schema import Base, Candidate
from candidate_management import add_candidate, get_candidate_by_email, update_candidate, delete_candidate

DATABASE_URL = 'sqlite:///../data/test_jobsearching_agent.db'

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
        self.session.commit()

    def test_add_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe@example.com", "1234567890", "resume.pdf")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")
        self.assertEqual(candidate.email, "john.doe@example.com")

    def test_get_candidate_by_email(self):
        add_candidate("John", "Doe", "john.doe@example.com", "1234567890", "resume.pdf")
        candidate = get_candidate_by_email("john.doe@example.com")
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.first_name, "John")
        self.assertEqual(candidate.last_name, "Doe")

    def test_update_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe@example.com", "1234567890", "resume.pdf")
        updated_candidate = update_candidate(candidate.id, phone="0987654321")
        self.assertIsNotNone(updated_candidate)
        self.assertEqual(updated_candidate.phone, "0987654321")

    def test_delete_candidate(self):
        candidate = add_candidate("John", "Doe", "john.doe@example.com", "1234567890", "resume.pdf")
        deleted_candidate = delete_candidate(candidate.id)
        self.assertIsNotNone(deleted_candidate)
        self.assertIsNone(get_candidate_by_email("john.doe@example.com"))

if __name__ == "__main__":
    unittest.main()
