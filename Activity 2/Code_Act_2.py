import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# Load housing dataset
data = pd.read_csv("housing.csv")

print("First few rows of the data:")
print(data.head())

print("\nSummary statistics (like average, min, max):")
print(data.describe())

print("\nColumn names in the dataset:")
print(data.columns)

# Identify target column
target_column = "median_house_value"

# Handle categorical column 'ocean_proximity' using one-hot encoding
data_encoded = pd.get_dummies(data, columns=["ocean_proximity"], drop_first=True)

# Handle missing values by filling with column mean
data_encoded = data_encoded.fillna(data_encoded.mean(numeric_only=True))

# Features (X) and Label (y)
X = data_encoded.drop(target_column, axis=1)
y = data_encoded[target_column]

print("\nFeature names (inputs):")
print(list(X.columns))

print("\nTarget (output - house value):")
print(target_column)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate using RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nRoot Mean Squared Error (how far predictions are on average): {rmse:.2f}")

# Show some predictions
results = pd.DataFrame({
    "Actual": y_test[:10].values,
    "Predicted": y_pred[:10]
})
print("\nSample predictions (first 10 houses):")
print(results)
