import csv
import random
from faker import Faker

fake = Faker('en_GB')

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
course_hierarchy = list(course_map.keys())

pass_grades = ['A1', 'B2', 'B3', 'C4', 'C5', 'C6']
fail_grades = ['D7', 'E8', 'F9']
all_grades = pass_grades + fail_grades

def is_pass(grade):
    return grade in pass_grades

def generate_student(index, category):
    preferred = random.choice(course_hierarchy)
    name = fake.name()
    reg_no = f"REG2025_{index + 1:04d}"

    english = random.choice(pass_grades)
    maths = random.choice(pass_grades)
    sciences = [random.choice(all_grades) for _ in range(4)]
    others = [random.choice(all_grades) for _ in range(5)]

    # Valid science pass count
    science_passes = sum(1 for g in sciences if is_pass(g))

    # Base scores
    utme = random.randint(180, 300)
    post_utme = random.randint(50, 100)

    admitted = "-"

    if category == "match":
        # Ensure scores and grades meet preferred course requirements
        req = course_map[preferred]
        utme = random.randint(req["utme_min"], req["utme_min"] + 30)
        post_utme = random.randint(req["post_utme_min"], req["post_utme_min"] + 15)
        sciences = [random.choice(pass_grades) for _ in range(3)] + [random.choice(all_grades)]
        english = random.choice(pass_grades)
        maths = random.choice(pass_grades)
        admitted = preferred

    elif category == "fallback":
        # Pick a high preferred course
        preferred = random.choice(course_hierarchy[:5])  # Top 5
        req = course_map[preferred]

        # Fail to meet preferred requirements
        utme = random.randint(180, req["utme_min"] - 1)
        post_utme = random.randint(50, req["post_utme_min"] - 1)

        # Check for fallback lower courses
        for course in course_hierarchy[course_map[preferred]['rank'] + 1:]:
            r = course_map[course]
            if utme >= r["utme_min"] and post_utme >= r["post_utme_min"]:
                admitted = course
                break

        english = random.choice(pass_grades)
        maths = random.choice(pass_grades)
        sciences = [random.choice(pass_grades) for _ in range(2)] + [random.choice(all_grades) for _ in range(2)]

    elif category == "rejected":
        # Make them fail English, Math, or all science
        fail_type = random.choice(["english", "math", "science"])
        if fail_type == "english":
            english = random.choice(fail_grades)
        elif fail_type == "math":
            maths = random.choice(fail_grades)
        else:
            sciences = [random.choice(fail_grades) for _ in range(4)]

        utme = random.randint(120, 180)
        post_utme = random.randint(30, 55)

    return [
        reg_no, name, preferred, utme, post_utme,
        english, maths, *sciences,
        *others,
        admitted
    ]

# Generate dataset
students = []
index = 0

for _ in range(200):  # 20% perfect match
    students.append(generate_student(index, "match"))
    index += 1

for _ in range(600):  # 60% fallback admitted
    students.append(generate_student(index, "fallback"))
    index += 1

for _ in range(200):  # 20% rejected
    students.append(generate_student(index, "rejected"))
    index += 1

# Shuffle for realism
random.shuffle(students)

# Save to CSV
header = [
    "Registration No", "Name", "Preferred Course", "UTME", "Post-UTME",
    "English", "Maths", "Physics", "Chemistry", "Biology", "Agric",
    "Civic Education", "Geography", "Economics", "Government", "Literature",
    "admitted_department"
]

with open("admission_dataset_final.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(students)

print("✅ Final dataset generated: 'admission_dataset_final.csv'")
