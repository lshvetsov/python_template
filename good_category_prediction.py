import numpy as np
import nltk
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")


def train_rf(train_df, train_labels):
    # Instantiate a RandomForestClassifier
    rf_model = RandomForestClassifier(random_state=42)

    # Fit the model
    rf_model.fit(train_df, train_labels)

    return rf_model


def tokenize_text(text: str) -> list[str]:
    text = text.lower().strip()

    # Tokenize with regexp token with the pattern [A-z]+
    tokens = regexp_tokenize(text, "[A-z]+")

    # Remove stopwords
    stop_words = set(stopwords.words('english'))

    # Filter stopwords out of the text
    tokens = [token for token in tokens if token.lower() not in stop_words]

    return tokens


def lemmatize_text(tokens: list[str]) -> list[str]:
    # Instantiate WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize without POS tags for performance reasons
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens


def load_models():
    # Load w2v_model.pkl from the data directory
    w2v_model = pd.read_pickle("../data/w2v_model.pkl")

    # Load rf_model.pkl from the data directory
    rf_model = pd.read_pickle("../data/rf_model.pkl")

    # Load label_encoder.pkl from the data directory
    label_encoder = pd.read_pickle("../data/label_encoder.pkl")

    return w2v_model, rf_model, label_encoder


def predict_top3_categories(text_input, w2v_model, rf_model, label_encoder):
    # Tokenize and lemmatize text input
    input_tokens = lemmatize_text(tokenize_text(text_input))

    # Get mean of the embeddings vector
    input_embed = np.mean([w2v_model.wv[word] for word in input_tokens if word in w2v_model.wv]
                          or [np.zeros(300)], axis=0)

    # Convert embedding vectors to a DataFrame
    input_df = pd.DataFrame([input_embed])

    # Get the predicted probabilities of the rf_model with predict_proba
    predicted_proba = rf_model.predict_proba(input_df)

    # Get the top3 categories from their probability values
    top3_idx = np.argsort(predicted_proba, axis=1)[:, -3:]

    # Get predicted value classes and flatten
    top3_classes_encoded = rf_model.classes_[top3_idx]
    top3_classes_encoded_flat = top3_classes_encoded.flatten()

    # Perform inverse transformation to get the name of the classes and reshape
    top3_classes = label_encoder.inverse_transform(top3_classes_encoded_flat)
    top3_classes = top3_classes.reshape(top3_classes_encoded.shape)

    return top3_classes, predicted_proba, top3_idx


def main():
    st.title('Goods Category App')

    text_input = st.text_area('Enter Goods Description', 'Type Here...')

    button, space, clear = st.columns([1, 2, 1])

    with button:
        if st.button('Predict'):
            w2v_model, rf_model, label_encoder = load_models()
            top3_classes, predicted_proba, top3_idx = predict_top3_categories(text_input, w2v_model, rf_model,
                                                                              label_encoder)

            with space:
                st.write("Top 3 Predicted Categories:")
                for i, classes in enumerate(top3_classes):
                    for category, prob in zip(classes[::-1], predicted_proba[i, top3_idx[i]][::-1]):
                        st.write(f"{category} {prob * 100:.0f}")
    with clear:
        clear_button = st.button('Clear')

        if clear_button:
            st.empty()


# Entry point
if __name__ == "__main__":
    main()
