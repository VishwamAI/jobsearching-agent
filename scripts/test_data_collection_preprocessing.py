import unittest
import pandas as pd
from unittest.mock import patch, Mock
from scripts.data_collection_preprocessing import fetch_job_listings, preprocess_job_data

class TestDataCollectionPreprocessing(unittest.TestCase):

    @patch('scripts.data_collection_preprocessing.requests.get')
    def test_fetch_job_listings_success(self, mock_get):
        mock_response = Mock()
        expected_data = {'jobs': [{'title': 'Software Engineer', 'description': 'Develop software', 'requirements': 'Python', 'qualifications': 'BSc in Computer Science'}]}
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        api_url = "https://api.example.com/job_listings"
        headers = {"User-Agent": "Mozilla/5.0"}
        result = fetch_job_listings(api_url, headers)
        self.assertEqual(result, expected_data)

    @patch('scripts.data_collection_preprocessing.requests.get')
    def test_fetch_job_listings_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api_url = "https://api.example.com/job_listings"
        headers = {"User-Agent": "Mozilla/5.0"}
        result = fetch_job_listings(api_url, headers)
        self.assertIsNone(result)

    def test_preprocess_job_data(self):
        job_data = [
            {'title': 'Software Engineer', 'description': 'Develop software', 'requirements': 'Python', 'qualifications': 'BSc in Computer Science'},
            {'title': 'Data Scientist', 'description': 'Analyze data', 'requirements': 'Python, R', 'qualifications': 'MSc in Data Science'}
        ]
        expected_df = pd.DataFrame([
            {'title': 'Software Engineer', 'description': 'Develop software', 'requirements': 'Python', 'qualifications': 'BSc in Computer Science'},
            {'title': 'Data Scientist', 'description': 'Analyze data', 'requirements': 'Python, R', 'qualifications': 'MSc in Data Science'}
        ])
        result_df = preprocess_job_data(job_data)
        pd.testing.assert_frame_equal(result_df, expected_df)

if __name__ == '__main__':
    unittest.main()
