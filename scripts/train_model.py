import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model(input_csv, model_output):
    # Read the feature CSV file
    df = pd.read_csv(input_csv, low_memory=False)

    # Separate features and target variable
    X = df.drop(columns=['job_level'])
    y = df['job_level']

    # Convert all columns to numeric, coercing errors to NaN
    X = X.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values in any column
    X.dropna(inplace=True)
    y = y[X.index]  # Ensure target variable matches the filtered features

    # Encode the target variable if it contains categorical data
    if y.dtype == 'object':
        le = LabelEncoder()
        y = le.fit_transform(y)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

    # Save the trained model to a file
    joblib.dump(model, model_output)
    print(f"Trained model saved to {model_output}")

if __name__ == "__main__":
    input_csv = '../data/job_listings_features_encoded.csv'
    model_output = '../models/job_matching_model.pkl'
    train_model(input_csv, model_output)
