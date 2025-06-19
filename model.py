from sklearn.tree import DecisionTreeClassifier
import pickle

with open("admission_model.pkl_model.pkl", "rb") as f:
    model = pickle.load(f)

# View basic model info
print(model)
print("Features:", model.feature_names_in_ if hasattr(model, 'feature_names_in_') else "N/A")
print("Classes:", model.classes_ if hasattr(model, 'classes_') else "N/A")
