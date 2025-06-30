import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load model & label encoder
model = joblib.load("admission_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# 2. Load dataset
df = pd.read_csv("sample_student_data.csv")

# 3. Map grades to numbers
grade_map = {
    "A1": 1, "B2": 2, "B3": 3,
    "C4": 4, "C5": 5, "C6": 6,
    "D7": 7, "E8": 8, "F9": 9
}
for col in ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric',
            'Civic Education', 'Geography', 'Economics', 'Government', 'Literature']:
    df[col] = df[col].map(grade_map)

# 4. Remove not admitted candidates
df = df[df["admitted_department"] != "-"]

# 5. Prepare features and target
features = [
    'UTME', 'Post-UTME',
    'English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric',
    'Geography', 'Economics', 'Literature'
]
X = df[features]
y_true = label_encoder.transform(df["admitted_department"])

# 6. Predict
y_pred = model.predict(X)

# 7. Evaluate
accuracy = accuracy_score(y_true, y_pred)
print(f"✅ Accuracy: {accuracy * 100:.2f} %\n")

print("🔍 Classification Report:")
print(classification_report(y_true, y_pred, target_names=label_encoder.classes_))

# 8. Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_,
            cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
