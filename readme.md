# Handwritten Digit Recognition App

This is a simple Streamlit application for recognizing handwritten digits using a pre-trained TensorFlow model. Users can draw a digit on a canvas, and the app will predict the digit using the loaded model.

## Features

- **Draw a Digit**: Use the canvas to draw a digit between 0 and 9.
- **Model Prediction**: After drawing, the app predicts the digit and displays the result.
- **Customizable Canvas**: Adjust stroke width, color, and add a background image if desired.
- **Processed Image Display**: View the processed and resized version of your drawn digit.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Aditya190803/Handwritten-Digit-Recognition.git
   cd Handwritten-Digit-Recognition
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have a trained model saved as `digit_recognition_model.keras` in the same directory as the app script.
2. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

3. Open the app in your web browser. Draw a digit on the canvas on the left side, and the app will display the processed image and predicted digit on the right side.



