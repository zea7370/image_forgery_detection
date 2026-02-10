import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from feature_extractor import extract_features

data = []
labels = []

dataset_path = "dataset"

for label in ["original", "tampered"]:
    folder = os.path.join(dataset_path, label)
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        features = extract_features(path)
        data.append(features)
        labels.append(0 if label == "original" else 1)

df = pd.DataFrame(data, columns=["noise", "edges", "compression"])
df["label"] = labels

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")
