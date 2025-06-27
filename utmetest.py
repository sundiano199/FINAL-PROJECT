import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

class TestImportFullCandidateData(unittest.TestCase):
    def setUp(self):
        # Create a dummy MainApp-like object
        self.app = type('DummyApp', (), {})()
        self.app.load_registered_candidates_data = MagicMock()

        # Bind the method under test
        from main import MainApp  # Replace with actual module name
        self.app.import_full_candidate_data = MainApp.import_full_candidate_data.__get__(self.app)




    @patch('tkinter.filedialog.askopenfilename', return_value='fakefile.csv')
    @patch('pandas.read_csv', side_effect=Exception("File not found"))
    @patch('tkinter.messagebox.showerror')
    def test_invalid_csv_reading(self, mock_error, mock_read_csv, mock_askfile):
        self.app.import_full_candidate_data()
        mock_error.assert_called_once()
        self.assertIn("Could not read file", mock_error.call_args[0][1])

    @patch('tkinter.filedialog.askopenfilename', return_value='test.csv')
    @patch('pandas.read_csv')
    @patch('tkinter.messagebox.showerror')
    def test_missing_columns_in_csv(self, mock_error, mock_read_csv, mock_askfile):
        # Provide DataFrame missing some required columns
        mock_df = pd.DataFrame({"reg_no": ["001"]})
        mock_read_csv.return_value = mock_df

        self.app.import_full_candidate_data()
        mock_error.assert_called_once_with("Format Error", "CSV file must contain all required columns.")

    @patch('tkinter.filedialog.askopenfilename', return_value='test.csv')
    @patch('pandas.read_csv')
    @patch('tkinter.messagebox.showinfo')
    @patch('sqlite3.connect')
    def test_successful_import(self, mock_connect, mock_info, mock_read_csv, mock_askfile):
        # Create a valid DataFrame
        valid_data = {
            "reg_no": ["001"],
            "surname": ["John"],
            "othernames": ["Doe"],
            "sex": ["M"],
            "dob": ["2000-01-01"],
            "nationality": ["Nigerian"],
            "session": ["2024/2025"],
            "reg_date": ["2024-06-01"],
            "year": ["2024"],
            "preferred_course": ["Computer Science"],
            "subject1": ["Math"], "grade1": ["A1"],
            "subject2": ["Eng"], "grade2": ["B2"],
            "subject3": ["Bio"], "grade3": ["C4"],
            "subject4": ["Chem"], "grade4": ["B3"],
            "subject5": ["Phys"], "grade5": ["A1"],
            "subject6": ["Geo"], "grade6": ["C5"],
            "subject7": ["Econs"], "grade7": ["B2"],
            "subject8": ["Civic"], "grade8": ["B3"],
            "subject9": ["Lit"], "grade9": ["A1"],
            "utme_subject1": ["Math"], "utme_score1": [70],
            "utme_subject2": ["Eng"], "utme_score2": [65],
            "utme_subject3": ["Chem"], "utme_score3": [60],
            "utme_subject4": ["Bio"], "utme_score4": [55],
            "total_utme_score": [250],
            "post_utme_score": [75]
        }
        mock_df = pd.DataFrame(valid_data)
        mock_read_csv.return_value = mock_df

        # Mock DB connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        self.app.import_full_candidate_data()

        self.assertTrue(mock_cursor.execute.called)
        mock_info.assert_called_once_with("Import Complete", "1 candidate records successfully imported.")
        self.app.load_registered_candidates_data.assert_called_once()
