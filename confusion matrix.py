import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("sample_student_data.csv")

# Convert O'Level grades to numeric
grade_map = {
    "A1": 8, "B2": 7, "B3": 6,
    "C4": 5, "C5": 4, "C6": 3,
    "D7": 2, "E8": 1, "F9": 0
}
subjects = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']
for subject in subjects:
    df[subject] = df[subject].map(grade_map)

# Encode target
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['admitted_department'] = df['admitted_department'].astype(str)
df['department_encoded'] = le.fit_transform(df['admitted_department'])

# Features and target
X = df[['UTME', 'Post-UTME', 'English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']]
y = df['department_encoded']

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load trained model
model = joblib.load("admission_model.pkl")

# Make predictions on test set
y_pred = model.predict(X_test)

# Generate and display confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(xticks_rotation=45, cmap=plt.cm.Blues)
plt.title("Confusion Matrix for Admission Prediction")
plt.tight_layout()
plt.show()
