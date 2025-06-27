import unittest
from unittest.mock import MagicMock, patch

class TestSaveOlevelResults(unittest.TestCase):
    def setUp(self):
        # Create a dummy class with required fields
        self.app = type('DummyApp', (), {})()

        # Simulate a StringVar or Entry for reg_no
        self.app.selected_olevel_reg = MagicMock()
        self.app.olevel_subjects = [MagicMock() for _ in range(9)]
        self.app.olevel_grades = [MagicMock() for _ in range(9)]

        # Default mock values
        self.app.selected_olevel_reg.get.return_value = "REG456"
        for i in range(9):
            self.app.olevel_subjects[i].get.return_value = f"Subject{i+1}"
            self.app.olevel_grades[i].get.return_value = "A1"

        # Bind method under test
        from main import MainApp  # Replace with real module
        self.app.save_olevel_results = MainApp.save_olevel_results.__get__(self.app)

    @patch('sqlite3.connect')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_successful_save(self, mock_showerror, mock_showinfo, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        self.app.save_olevel_results()

        # Ensure DB insertion
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # Ensure success message is shown
        mock_showinfo.assert_called_once_with("Success", "O'Level results saved successfully!")
        mock_showerror.assert_not_called()

    @patch('tkinter.messagebox.showerror')
    def test_missing_reg_number(self, mock_showerror):
        self.app.selected_olevel_reg.get.return_value = ""
        self.app.save_olevel_results()
        mock_showerror.assert_called_once_with("Error", "Please select a registration number.")

    @patch('tkinter.messagebox.showerror')
    def test_missing_subject_or_grade(self, mock_showerror):
        self.app.olevel_subjects[3].get.return_value = ""  # Simulate missing subject
        self.app.olevel_grades[5].get.return_value = ""    # Simulate missing grade
        self.app.save_olevel_results()
        mock_showerror.assert_called_once_with("Input Error", "All 9 subjects and grades must be filled.")
