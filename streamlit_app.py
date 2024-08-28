import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns

# Load the trained model
model = joblib.load('/disease_detection/storage/my_model')

input_features = [
  'Usia',
  'sistolik',
  'diastolik',
  'gula_darah',
  'kolesterol',
  'asam_urat',
  'bmi',
  'otot_skeletal',
  'lemak_tubuh',
  'lemak_viscera',
  'resting_metabolisme',
  'usia_sel',
  'subcutan_fat',
  'Merokok',
  'aktifitas'
]

def main():
  st.title('Data Prediction App')

  with st.form(key='prediction_form'):
    inputs = {}
    for feature in input_features:
      inputs[feature] = st.text_input(f'Enter {feature}')

    submit_button = st.form_submit_button(label='Predict')

    if submit_button:
      # Convert inputs to a DataFrame
      input_data = pd.DataFrame([inputs])

      # Perform prediction
      predictions = model.predict(input_data)

      # Display results
      st.write("Predictions:", predictions)

      # Optionally, show accuracy score and other metrics
      if hasattr(model, 'score') and hasattr(model, 'predict'):
        # Generate some example true values (for demonstration)
        # In practice, you should use your test set for accurate results
        true_values = np.array([0])  # Placeholder for true values

        # Compute and display accuracy
        accuracy = accuracy_score(true_values, predictions)
        st.write(f"Accuracy Score: {accuracy:.2f}")

        # Compute and display classification report
        report = classification_report(true_values, predictions, output_dict=True)
        st.write("Classification Report:")
        st.text(classification_report(true_values, predictions))

        # Compute and display confusion matrix
        conf_matrix = confusion_matrix(true_values, predictions)
        fig, ax = plt.subplots()
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title('Confusion Matrix')
        st.pyplot(fig)