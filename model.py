import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load the dataset
df = pd.read_csv("sample_student_data.csv")

# 2. Map O'Level grades to numeric scores
grade_map = {
    "A1": 8, "B2": 7, "B3": 6,
    "C4": 5, "C5": 4, "C6": 3,
    "D7": 2, "E8": 1, "F9": 0
}
subjects = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']
for subject in subjects:
    df[subject] = df[subject].map(grade_map)

# 3. Features and target
features = ['UTME', 'Post-UTME'] + subjects
X = df[features]
y = df['admitted_department']

# 4. Encode department names
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 5. Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# 6. Save the model and encoder
joblib.dump(model, 'admission_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Model training complete and saved successfully.")
