from sklearn.datasets import load_iris
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

iris = load_iris(as_frame=True)
df = iris.frame

print("First few rows of the data:")
print(df.head())

print("\nSummary statistics (like average, min, max):")
print(df.describe())

print("\nFeature names (inputs):")
print(iris.feature_names)

print("\nTarget classes (outputs - flower types):")
print(iris.target_names)

X = df[iris.feature_names]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nAccuracy (how often it's right):")
print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix (shows correct vs wrong predictions):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report (precision, recall, f1-score):")
print(classification_report(y_test, y_pred, target_names=iris.target_names))