import pandas as pd
import random
from collections import Counter
from faker import Faker

# Initialize Faker
fake = Faker()

# Course hierarchy and requirements
course_map = {
    "Computer Science": {"utme_min": 240, "post_utme_min": 75, "rank": 0},
    "Microbiology": {"utme_min": 230, "post_utme_min": 70, "rank": 1},
    "Biochemistry": {"utme_min": 225, "post_utme_min": 70, "rank": 2},
    "Physics": {"utme_min": 220, "post_utme_min": 68, "rank": 3},
    "Applied Physics": {"utme_min": 215, "post_utme_min": 66, "rank": 4},
    "Industrial Chemistry": {"utme_min": 210, "post_utme_min": 65, "rank": 5},
    "Mathematics and Statistics": {"utme_min": 205, "post_utme_min": 64, "rank": 6},
    "Animal and Environmental Biology": {"utme_min": 203, "post_utme_min": 60, "rank": 7},
    "Plant Science and Biotechnology": {"utme_min": 200, "post_utme_min": 60, "rank": 8}
}

grades = ['A1', 'B2', 'B3', 'C4', 'C5', 'C6']
fail_grades = ['D7', 'E8', 'F9']

# Function to generate a student with optional forced course
def generate_student(index, force_admit_course=None):
    name = fake.name()
    preferred_course = random.choice(list(course_map.keys()))
    utme = random.randint(180, 300)
    post_utme = random.randint(30, 100)

    def rand_grade(pass_only=False):
        return random.choice(grades) if pass_only else random.choice(grades + fail_grades)

    english = rand_grade()
    maths = rand_grade()
    physics = rand_grade()
    chemistry = rand_grade()
    biology = rand_grade()
    agric = rand_grade()
    civic_education = rand_grade()
    geography = rand_grade()
    economics = rand_grade()
    government = rand_grade()
    literature = rand_grade()

    def is_pass(g): return g in grades
    subject_passes = sum(is_pass(g) for g in [english, maths, physics, chemistry, biology, agric])
    has_english = is_pass(english)
    has_maths = is_pass(maths)

    def qualifies(course):
        req = course_map[course]
        return (
            utme >= req['utme_min'] and
            post_utme >= req['post_utme_min'] and
            has_english and has_maths and
            subject_passes >= 5
        )

    admitted = "-"

    if force_admit_course:
        while not qualifies(force_admit_course):
            utme = random.randint(180, 300)
            post_utme = random.randint(30, 100)
            english = rand_grade()
            maths = rand_grade()
            physics = rand_grade()
            chemistry = rand_grade()
            biology = rand_grade()
            agric = rand_grade()
            subject_passes = sum(is_pass(g) for g in [english, maths, physics, chemistry, biology, agric])
            has_english = is_pass(english)
            has_maths = is_pass(maths)
        admitted = force_admit_course
        preferred_course = force_admit_course
    else:
        if qualifies(preferred_course):
            admitted = preferred_course
        else:
            preferred_rank = course_map[preferred_course]['rank']
            eligible_courses = [
                course for course in course_map
                if course_map[course]['rank'] > preferred_rank and qualifies(course)
            ]
            if "Physics" in eligible_courses and "Applied Physics" in eligible_courses:
                admitted = random.choice(["Physics", "Applied Physics"])
            elif eligible_courses:
                admitted = eligible_courses[0]

    reg_no = f"REG2025_{index + 1:04d}"
    return [
        reg_no, name, preferred_course, utme, post_utme,
        english, maths, physics, chemistry, biology, agric,
        civic_education, geography, economics, government, literature,
        admitted
    ]

# =========================
# STEP 1: Load Original Data
# =========================
df = pd.read_csv("sample_student_data.csv")

# =========================
# STEP 2: Detect Underrepresented Courses
# =========================
min_required = 30
admit_counts = Counter(df['admitted_department'])
underrepresented = {
    course: count for course, count in admit_counts.items()
    if count < min_required and course != "-"
}

print("\n🔍 Underrepresented Courses:")
for course, count in underrepresented.items():
    print(f"{course}: {count} (needs {min_required - count} more)")

# =========================
# STEP 3: Generate More Students
# =========================
columns = [
    "Registration No", "Name", "Preferred Course", "UTME", "Post-UTME",
    "English", "Maths", "Physics", "Chemistry", "Biology", "Agric",
    "Civic Education", "Geography", "Economics", "Government", "Literature",
    "admitted_department"
]

new_rows = []
index_start = len(df)

for course, count in underrepresented.items():
    needed = min_required - count
    for i in range(needed):
        new_rows.append(generate_student(index_start + len(new_rows), force_admit_course=course))

df_new = pd.DataFrame(new_rows, columns=columns)
df_combined = pd.concat([df, df_new], ignore_index=True)

# =========================
# STEP 4: Save to New File
# =========================
df_combined.to_csv("university_admissions_balanced.csv", index=False, encoding='utf-8')
print("\n✅ New balanced dataset saved as 'university_admissions_balanced.csv'")
