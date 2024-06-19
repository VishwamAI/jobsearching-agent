import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

def preprocess_input_data(input_data):
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])

    # Select relevant columns
    df = df[['job_title', 'jurisdictional_classification', 'negotiating_unit', 'agency_description']]

    # Combine relevant text columns into a single column for feature extraction
    df['combined_text'] = df['job_title'] + ' ' + df['jurisdictional_classification'] + ' ' + df['negotiating_unit'] + ' ' + df['agency_description']

    # Initialize the TF-IDF vectorizer
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')

    # Transform the combined text data
    X = vectorizer.transform(df['combined_text'])

    # Convert the TF-IDF matrix to a DataFrame
    feature_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

    # Convert all columns to numeric, coercing errors to NaN
    feature_df = feature_df.apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values in any column
    feature_df.dropna(inplace=True)

    return feature_df

def predict_job_level(input_data):
    # Load the trained model
    model = joblib.load('models/job_matching_model.pkl')

    # Preprocess the input data
    preprocessed_data = preprocess_input_data(input_data)

    # Make predictions
    job_level_pred = model.predict(preprocessed_data)

    # Decode the predicted job level if it was encoded
    le = LabelEncoder()
    le.classes_ = joblib.load('models/label_encoder_classes.pkl')
    job_level_pred = le.inverse_transform(job_level_pred)

    return job_level_pred[0]

if __name__ == "__main__":
    # Sample input data
    input_data = {
        'job_title': 'Software Engineer',
        'grade': 'G-12',
        'jurisdictional_classification': 'Competitive',
        'negotiating_unit': 'PS&T',
        'agency_description': 'Department of Technology'
    }

    # Predict job level
    predicted_job_level = predict_job_level(input_data)
    print(f"Predicted job level: {predicted_job_level}")
