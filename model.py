import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# ✅ Step 1: Load dataset
df = pd.read_csv("sample_student_data.csv")  # Ensure this file exists in the same directory

# ✅ Step 2: Convert O'Level grades to numeric
grade_map = {
    "A1": 8, "B2": 7, "B3": 6,
    "C4": 5, "C5": 4, "C6": 3,
    "D7": 2, "E8": 1, "F9": 0
}
subjects = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']
for subject in subjects:
    df[subject] = df[subject].map(grade_map)

# ✅ Step 3: Encode the admitted department (target)
le = LabelEncoder()
df['admitted_department'] = df['admitted_department'].astype(str)
df['department_encoded'] = le.fit_transform(df['admitted_department'])

# ✅ Step 4: Define features (X) and target (y)
X = df[['UTME', 'Post-UTME', 'English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']]
y = df['department_encoded']

# ✅ Step 5: Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Step 6: Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Step 7: Evaluate the model
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))
print("\n✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ✅ Step 8: Save the model and label encoder
joblib.dump(model, "admission_model.pkl")
joblib.dump(le, "label_encoder.pkl")
print("\n✅ Model and label encoder saved.")
