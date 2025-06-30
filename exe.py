import subprocess

subprocess.call([
    "pyinstaller",
    "--onefile",
    "--windowed",
    "main.py",
    "--add-data", "students.db;.",
    "--add-data", "admission_model.pkl;.",
    "--add-data", "label_encoder.pkl;.",
    "--add-data", "sample_student_data.csv;."
])
