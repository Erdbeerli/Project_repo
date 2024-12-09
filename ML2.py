import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import requests

# Fetch the first 20 plants with "herb" or "vegetable" tags
def fetch_first_20_plants():
    """
    Fetch the first 20 plants with tags 'herb' or 'vegetable' from OpenFarm API.
    """
    base_url = "https://openfarm.cc/api/v1/crops"
    all_plants = []  # List to store valid plants

    try:
        # Fetch all data from the first page (no advanced filtering supported by API)
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                for plant in data['data']:
                    attributes = plant.get('attributes', {})
                    tags = attributes.get("tags_array", [])

                    # Only include plants with 'herb' or 'vegetable' tags
                    if "herb" in tags or "vegetable" in tags:
                        all_plants.append({
                            "name": attributes.get("name", "Unknown Plant"),
                            "description": attributes.get("description", "No description available."),
                            "sun_requirements": attributes.get("sun_requirements", "Unknown"),
                            "spread": attributes.get("spread", "Unknown"),
                            "image_url": attributes.get("main_image_path", None)
                        })

                    if len(all_plants) >= 20:  # Stop when 20 plants are fetched
                        break
            else:
                st.error("No 'data' field found in the API response.")
        else:
            st.error(f"API request failed with status code {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    
    return all_plants

# Convert list of fetched plants to DataFrame
def convert_to_dataframe(plant_list):
    """
    Convert a list of plant dictionaries into a pandas DataFrame.
    """
    if not plant_list:
        st.warning("No plant data available to convert.")
        return pd.DataFrame()

    # Create DataFrame and ensure 'spread' is numeric
    df = pd.DataFrame(plant_list)
    df["spread"] = pd.to_numeric(df["spread"], errors="coerce").fillna(0)
    return df

# Initialize Machine Learning Model
def initialize_ml_model(df):
    """
    Initialize and train a RandomForestClassifier to recommend plants.
    """
    if df.empty:
        st.error("No data available for training.")
        return None, None

    try:
        # Filter out invalid rows
        df = df[df["sun_requirements"] != "Unknown"]
        df = df.dropna(subset=["spread"])

        # Encode 'sun_requirements' using LabelEncoder
        le_sun = LabelEncoder()
        df["sun_encoded"] = le_sun.fit_transform(df["sun_requirements"])

        # Prepare features and labels
        X = df[["sun_encoded", "spread"]]
        y = df["name"]

        # Train RandomForest model
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        st.success("Machine Learning Model trained successfully!")
        return model, le_sun
    except Exception as e:
        st.error(f"Error training the model: {e}")
        return None, None

# Analyze Image and Predict Plant
def analyze_image_and_predict(image, model, le_sun, plants_df):
    """
    Analyze an uploaded image's brightness and predict a suitable plant.
    """
    try:
        # Calculate average brightness
        avg_color = np.array(image).mean(axis=(0, 1))
        brightness = avg_color.mean()
        st.write(f"Image Brightness: {brightness:.2f}")

        # Determine light condition based on brightness
        if brightness > 180:
            light_condition = "full sun"
        elif brightness > 100:
            light_condition = "partial sun"
        else:
            light_condition = "shade"

        st.write(f"Detected Light Condition: {light_condition}")

        # Use the model for prediction
        if model is not None and le_sun is not None:
            if light_condition in le_sun.classes_:
                light_encoded = le_sun.transform([light_condition])[0]
                spread_mean = plants_df["spread"].mean()
                input_data = np.array([[light_encoded, spread_mean]])

                predicted_plant = model.predict(input_data)[0]
                st.subheader(f"🌱 Recommended Plant: {predicted_plant}")
            else:
                st.warning("Light condition not recognized for prediction.")
        else:
            st.error("Machine Learning model is not initialized.")
    except Exception as e:
        st.error(f"Error analyzing image: {e}")

# Main Streamlit App
def main():
    st.title("Plant Recommendation System 🌱")
    st.write("Fetch plants with 'herb' or 'vegetable' tags, train a model, and predict suitable plants.")

    # Button to fetch and display plants
    if st.button("Fetch and Display Plants"):
        st.info("Fetching plant data...")
        plants = fetch_first_20_plants()

        # Convert fetched plants to DataFrame
        plants_df = convert_to_dataframe(plants)

        if not plants_df.empty:
            st.success("Successfully fetched plant data!")
            st.write("### Plant Data:")
            st.dataframe(plants_df)  # Display the DataFrame

            # Initialize Machine Learning Model
            st.subheader("Training Machine Learning Model...")
            model, le_sun = initialize_ml_model(plants_df)

            if model and le_sun:
                st.success("Model is ready for predictions!")

                # Allow user to upload an image for analysis
                st.subheader("Upload an Image for Plant Recommendation:")
                uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
                if uploaded_image:
                    image = Image.open(uploaded_image)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    analyze_image_and_predict(image, model, le_sun, plants_df)
            else:
                st.error("Failed to train the model.")
        else:
            st.warning("No valid plant data fetched.")

if __name__ == "__main__":
    main()
