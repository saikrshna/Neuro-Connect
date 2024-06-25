import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
import time
import serial

# Load the CSV files
csv_files = ["recorded_data1.csv","recorded_data2.csv"]

# Read CSV files into DataFrame and concatenate them
dfs = [pd.read_csv(file) for file in csv_files]
data = pd.concat(dfs, ignore_index=True)

# Prepare features (X) and labels (y)
X = data[['channel1', 'channel2']]
y = data['state']  # Assuming 'state' column contains the label

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

joblib.dump(clf, 'random_forest_model.pkl')
