import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2

try:
    # Load the trained model
    model = tf.keras.models.load_model("digit_recognition_model.keras")
    st.write("Model loaded successfully!")
except Exception as e:
    st.write(f"Error loading model: {e}")
    model = None

# Sidebar elements for customization
st.sidebar.header("Canvas Options")
stroke_width = st.sidebar.slider("Stroke width: ", 10, 35, 15)
stroke_color = "#FFFFFF"
bg_color = "#000000"
bg_image = st.sidebar.file_uploader("Background image (optional):", type=["png", "jpg"])
drawing_mode = "freedraw"
realtime_update = True

# Create columns for side-by-side layout
col1, col2 = st.columns(2)

with col1:
    # Canvas for drawing
    st.markdown("### Draw a digit on the canvas")
    canvas_result = st_canvas(
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=280,
        width=280,
        drawing_mode=drawing_mode,
        display_toolbar=True,
        key="full_app",
    )

with col2:
    # Process and display the image
    if canvas_result.image_data is not None:
        # Convert the image to the format expected by the model
        image = canvas_result.image_data.astype('uint8')

        # Convert the image to grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Create a mask to capture the drawn area
        _, thresh = cv2.threshold(image_gray, 1, 255, cv2.THRESH_BINARY)

        # Find contours to get the bounding box of the drawn area
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Get the largest contour which should be the drawn area
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Crop the drawn area
            cropped_image = image_gray[y:y+h, x:x+w]

            # Resize the cropped image to 28x28 pixels
            image_resized = cv2.resize(cropped_image, (28, 28))

            # Normalize the image
            image_normalized = image_resized.astype('float32') / 255

            # Reshape the image to fit the model input
            image_reshaped = image_normalized.reshape(1, 28, 28, 1)

            # Display the processed image
            st.markdown("### Processed Image")
            st.image(image_resized, width=250)

            if model:
                # Make prediction
                prediction = model.predict(image_reshaped)
                predicted_digit = np.argmax(prediction, axis=1)

                # Display the prediction
                st.markdown(f"### Predicted Digit: **{predicted_digit[0]}**")
            else:
                st.markdown("### Model not loaded. Please check the error above.")
        else:
            st.markdown("### No drawing detected. Please draw a digit on the canvas.")
    else:
        st.markdown("### No drawing detected. Please draw a digit on the canvas.")
