import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load your balanced dataset
df = pd.read_csv("sample_student_data.csv")

# Define features and target
features = [
    "UTME", "Post-UTME",
    "English", "Maths", "Physics", "Chemistry", "Biology", "Agric", "Geography", "Economics", "Literature"
]

# Convert grades to numeric scores (A1=6 to F9=0)
grade_map = {
    'A1': 6, 'B2': 5, 'B3': 4, 'C4': 3, 'C5': 2, 'C6': 1,
    'D7': 0, 'E8': 0, 'F9': 0
}
for col in features[2:]:
    df[col] = df[col].map(grade_map)

X = df[features]
y_raw = df["admitted_department"]

# Encode labels (admitted departments)
le = LabelEncoder()
y = le.fit_transform(y_raw)

# Save the label encoder for decoding later
joblib.dump(le, "label_encoder.pkl")

# Split dataset (stratified to preserve class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model with class_weight='balanced' to handle imbalance
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "admission_model.pkl")

# Predict on test set
y_pred = model.predict(X_test)

# Print accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Accuracy: {accuracy:.3f}\n")

# Decode labels for display
target_names = le.inverse_transform(sorted(set(y)))
print("📊 Classification Report:")
print(classification_report(
    y_test, y_pred, target_names=target_names, zero_division=0
))

# Optional: Plot Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=target_names, yticklabels=target_names, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
