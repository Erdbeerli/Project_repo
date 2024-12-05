import streamlit as st
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import requests
import pandas as pd

# Fetch Plant Data
def fetch_plant_data():
    url = "https://openfarm.cc/api/v1/crops"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                # Filter: Only plants with the tag `vegetable` or `herb`
                filtered_plants = [
                    {
                        "plant_name": plant['attributes'].get("name", "Unknown"),
                        "sun_requirements": plant['attributes'].get("sun_requirements", "unknown"),
                        "spread": plant['attributes'].get("spread", "unknown"),
                        "description": plant['attributes'].get("description", "No description available")
                    }
                    for plant in data['data']
                    if "tags_array" in plant['attributes'] and
                    any(tag in ["vegetable", "herb"] for tag in plant['attributes'].get("tags_array", []))
                ]
            else:
                # If 'data' is missing or empty
                filtered_plants = []
        else:
            # If the API response fails
            filtered_plants = []
            st.error(f"Failed to fetch data from OpenFarm API. Status code: {response.status_code}")
    except Exception as e:
        # If any exception occurs
        filtered_plants = []
        st.error(f"Error fetching plant data: {e}")

    # Check if filtered_plants is empty, use fallback data
    if not filtered_plants:
        st.warning("Using fallback plant data.")
        return pd.DataFrame({
            "plant_name": ["Tomato", "Basil", "Lettuce"],
            "sun_requirements": ["full sun", "partial sun", "partial sun"],
            "spread": [50, 30, 40],
            "description": [
                "A delicious red fruit often mistaken as a vegetable.",
                "A fragrant herb used in Italian cuisine.",
                "A leafy green vegetable."
            ]
        })

    # Convert to DataFrame
    df = pd.DataFrame(filtered_plants)

    # Ensure required columns are present
    required_columns = {"plant_name", "sun_requirements", "spread"}
    if not required_columns.issubset(df.columns):
        st.error("API data is missing required columns. Using fallback data.")
        return pd.DataFrame({
            "plant_name": ["Tomato", "Basil", "Lettuce"],
            "sun_requirements": ["full sun", "partial sun", "partial sun"],
            "spread": [50, 30, 40],
            "description": [
                "A delicious red fruit often mistaken as a vegetable.",
                "A fragrant herb used in Italian cuisine.",
                "A leafy green vegetable."
            ]
        })

    return df

# Debugging and Validation
def debug_dataframe(df):
    """Debug and validate the DataFrame for potential issues."""
    st.write("Checking the fetched plant data:")
    st.write(df.head())  # Display the first few rows of the DataFrame

    if df.empty:
        st.error("The plant data DataFrame is empty. Ensure the API is working or provide fallback data.")
    else:
        # Validate columns
        missing_columns = [col for col in ["plant_name", "sun_requirements", "spread"] if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns in the DataFrame: {missing_columns}")
        else:
            st.success("Plant data fetched and validated successfully.")


# Initialize ML Model
def initialize_ml_model(df):
    if df.empty:
        st.error("No data available for training.")
        return None, None

    try:
        # Debug and filter invalid data
        st.write("Filtering invalid data from the DataFrame...")
        st.write(f"Original DataFrame shape: {df.shape}")
        
        # Filter entries with "unknown" sunlight requirements or spread
        df = df[df["sun_requirements"] != "unknown"]
        df["spread"] = pd.to_numeric(df["spread"], errors="coerce")  # Convert spread to numeric
        df = df.dropna(subset=["spread"])  # Drop rows with NaN values in spread
        st.write(f"Filtered DataFrame shape: {df.shape}")

        # Encode sunlight requirements
        le_sun = LabelEncoder()
        df["sun_encoded"] = le_sun.fit_transform(df["sun_requirements"])
        st.write("Label encoding for sunlight requirements applied.")
        st.write(df[["sun_requirements", "sun_encoded"]].drop_duplicates())  # Show encoding

        # Prepare features and labels
        X = df[["sun_encoded", "spread"]]
        y = df["plant_name"]

        # Train the model
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        st.success("Machine learning model trained successfully.")
        return model, le_sun
    except Exception as e:
        st.error(f"Error initializing the ML model: {e}")
        return None, None


# Analyze Uploaded Images
def analyze_image(image):
    try:
        width, height = image.size
        avg_color = np.array(image).mean(axis=(0, 1))
        brightness = avg_color.mean()
        if brightness > 180:
            light_condition = "full sun"
        elif brightness > 100:
            light_condition = "partial sun"
        else:
            light_condition = "shade"
        space = 150 if width > 1000 else (50 if width > 500 else 20)
        return light_condition, space
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return None, None


# Image-Based ML
def image_based_ml(model, le_sun):
    st.title("Image-Based Plant Recommendation")
    uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            light_condition, space = analyze_image(image)
            st.write(f"Detected Light Condition: {light_condition}")
            st.write(f"Detected Space: {space} cm")
            if model is not None and le_sun is not None:
                if light_condition in le_sun.classes_:
                    light_encoded = le_sun.transform([light_condition])[0]
                    input_data = np.array([[light_encoded, space]])
                    predicted_plant = model.predict(input_data)[0]
                    st.subheader(f"🌱 Recommended Plant: {predicted_plant}")
                else:
                    st.warning("Light condition not recognized.")
            else:
                st.error("Model is not initialized.")
        except Exception as e:
            st.error(f"Error processing image: {e}")


# Main
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Photo-Based ML"])
    if page == "Photo-Based ML":
        image_based_ml(model, le_sun)


# Run App
plants_df = fetch_plant_data()
debug_dataframe(plants_df)  # Add DataFrame debugging
model, le_sun = initialize_ml_model(plants_df)
main()
