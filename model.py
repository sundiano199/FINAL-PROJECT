import sqlite3

# Connect to your database
DB_NAME = "students.db"  # Replace with your actual DB file name
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Sample student scores (reg_no must match an existing student in the students table)
sample_scores = [
    ("REG001", 250, 72, "B3", "A1", "B2", "C4", "C5", "B3"),
    ("REG002", 198, 59, "C5", "C4", "C6", "D7", "C4", "C5"),
    ("REG003", 280, 80, "A1", "A1", "A1", "B2", "B3", "B3"),
    ("REG004", 210, 65, "B2", "B3", "B2", "C5", "C4", "C4"),
    ("REG005", 170, 50, "C6", "C6", "D7", "E8", "F9", "D7")
]

# Insert the sample data
for score in sample_scores:
    cursor.execute("""
        INSERT OR REPLACE INTO scores (
            reg_no, utme_score, post_utme_score,
            English, Maths, Physics, Chemistry, Biology, Agric
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, score)

conn.commit()
conn.close()

print("✅ Sample scores inserted successfully.")
