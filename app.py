import streamlit as st
from model_utils import predict_with_nutrition
from PIL import Image
import tempfile
import os

st.title("🍽️ Food Nutrition Estimator")
st.write("Upload a food image to predict its class and estimated nutrition values.")

uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save temp image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.read())
        image_path = tmp_file.name

    image = Image.open(image_path)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analyzing..."):
        result = predict_with_nutrition(image_path)

    st.success("✅ Prediction Complete!")

    st.write("### 🍴 Detected Food:", result['food'])
    st.write("**Estimated Volume (ml):**", result['volume_ml'])
    st.write("**Estimated Weight (g):**", result['weight_grams'])

    st.write("### 🧾 Nutrition Info:")
    for key, value in result['nutrition'].items():
        st.write(f"**{key}:** {round(value, 2) if isinstance(value, (int, float)) else value}")

    os.remove(image_path)
