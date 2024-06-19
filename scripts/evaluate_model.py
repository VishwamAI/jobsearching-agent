import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

def evaluate_model(model_path, test_csv):
    # Load the trained model
    model = joblib.load(model_path)

    # Read the test CSV file
    df = pd.read_csv(test_csv, low_memory=False)

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

    # Make predictions on the test set
    y_pred = model.predict(X)

    # Evaluate the model
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted')
    recall = recall_score(y, y_pred, average='weighted')
    f1 = f1_score(y, y_pred, average='weighted')

    print(f"Model accuracy: {accuracy}")
    print(f"Model precision: {precision}")
    print(f"Model recall: {recall}")
    print(f"Model F1 score: {f1}")

if __name__ == "__main__":
    model_path = '../models/job_matching_model.pkl'
    test_csv = '../data/job_listings_features_encoded.csv'
    evaluate_model(model_path, test_csv)
