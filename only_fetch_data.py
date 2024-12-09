import streamlit as st
import requests

def fetch_plant_data():
    """
    Fetch the first 20 plants with 'vegetable' or 'herb' tags from OpenFarm API.
    Returns a list of valid plants.
    """
    url = "https://openfarm.cc/api/v1/crops"
    machine_plants = []  # List to store valid plants

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if 'data' in data and data['data']:
                for plant in data['data']:
                    attributes = plant.get('attributes', {})
                    tags = attributes.get("tags_array", [])

                    # Include plants if they have "vegetable" or "herb" tags
                    if any(tag in ["vegetable", "herb"] for tag in tags):
                        machine_plants.append({
                            "name": attributes.get("name", "Unknown"),
                            "description": attributes.get("description", "No description available"),
                            "sun_requirements": attributes.get("sun_requirements", "unknown"),
                            "spread": attributes.get("spread", "unknown"),
                            "image_url": attributes.get("main_image_path", None)
                        })

                    # Stop after collecting 20 valid plants
                    if len(machine_plants) == 20:
                        break
            else:
                st.warning("No data found in the API response.")

        else:
            st.error(f"API request failed with status code {response.status_code}")

    except Exception as e:
        st.error(f"An error occurred while fetching plant data: {e}")

    # Return fetched plants or fallback data
    if not machine_plants:
        st.warning("No valid plants found. Using fallback data.")
        return [
            {"name": "Tomato", "description": "A red fruit often mistaken as a vegetable.", "sun_requirements": "full sun", "spread": 50, "image_url": None},
            {"name": "Basil", "description": "A fragrant herb used in Italian cuisine.", "sun_requirements": "partial sun", "spread": 30, "image_url": None},
            {"name": "Lettuce", "description": "A leafy green vegetable.", "sun_requirements": "partial sun", "spread": 40, "image_url": None}
        ]
    return machine_plants

def display_plants(plants):
    """
    Display the fetched plants with details.
    """
    st.write("### First 20 Plants with Tags 'Vegetable' or 'Herb'")
    if plants:
        for plant in plants:
            st.write(f"**Name:** {plant['name']}")
            st.write(f"**Description:** {plant['description']}")
            st.write(f"**Sun Requirements:** {plant['sun_requirements']}")
            st.write(f"**Spread:** {plant['spread']}")
            if plant['image_url']:
                st.image(plant['image_url'], caption=plant['name'], use_column_width=True)
            st.write("---")
    else:
        st.write("No plants with 'vegetable' or 'herb' tags were found.")

# Streamlit UI
st.title("🌱 First 20 Vegetables and Herbs from OpenFarm API")

if st.button("Fetch First 20 Plants"):
    st.write("Fetching the first 20 plants with 'vegetable' or 'herb' tags...")
    first_20_plants = fetch_plant_data()
    display_plants(first_20_plants)
