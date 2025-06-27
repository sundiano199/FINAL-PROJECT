import unittest
from unittest.mock import MagicMock, patch


# Assuming your class is named `StudentRegistration` and the method is inside it
class TestFullStudentRegistration(unittest.TestCase):
    def setUp(self):
        # Create a dummy instance with the necessary attributes
        self.app = type('DummyApp', (), {})()
        self.app.reg_entries = {
            "Registration Number": MagicMock(),
            "Surname": MagicMock(),
            "Other Names": MagicMock(),
            "Sex": MagicMock(),
            "Preferred Course of Study": MagicMock(),
            "Date of Birth": MagicMock(),
            "Nationality": MagicMock(),
            "Session": MagicMock(),
            "Date of Registration": MagicMock(),
            "Year": MagicMock(),
        }
        self.app.photo_path = MagicMock()
        self.app.clear_entries = MagicMock()

        # Provide sample return values
        for key in self.app.reg_entries:
            self.app.reg_entries[key].get.return_value = f"Test {key}"
        self.app.reg_entries["Registration Number"].get.return_value = "REG123"
        self.app.photo_path.get.return_value = "path/to/photo.jpg"

        # Bind the method to the dummy instance
        from main import MainApp # replace with actual import
        self.app.full_student_registration = MainApp.full_student_registration.__get__(self.app)

    @patch('sqlite3.connect')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_full_registration_success(self, mock_showerror, mock_showinfo, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call the method
        self.app.full_student_registration()

        # Ensure INSERT was attempted
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # Ensure success message was shown
        mock_showinfo.assert_called_once_with("Success", "Student bio data saved successfully.")
        mock_showerror.assert_not_called()

        # Ensure form cleared
        self.app.clear_entries.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_missing_registration_number(self, mock_showerror):
        self.app.reg_entries["Registration Number"].get.return_value = ""
        self.app.full_student_registration()
        mock_showerror.assert_called_once_with("Missing Data", "Registration Number is required.")

