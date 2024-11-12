import streamlit as st
import requests

def filter_plants_by_sunlight():
    """Displays plants based on user-selected sunlight requirements."""

    st.title("Filter Plants by Sunlight Requirement")
    st.write("Choose a sunlight condition to find suitable plants.")

    # Sunlight selection options
    sun_options = {
        'Full Sun ☀️': 'Full Sun',
        'Partial Sun 🌤️': 'Partial Sun'
    }
    selected_sun_option = st.selectbox('How sunny is the place for your plant?', list(sun_options.keys()))

    # Base URL for OpenFarm API
    base_url = "https://openfarm.cc/api/v1/crops"

    # Send a GET request to the API to get all crops data
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        matching_plants = []

        # Verify if there is any data in the response
                if 'data' in data and isinstance(data['data'], list):
                # Loop through each plant to filter by sun requirement
                for plant in data['data']:
                attributes = plant.get('attributes', {})

                
                # Retrieve the sun requirement and check if it matches the selected option
                plant_sun_req = attributes.get('sun_requirements', '').lower()
                
                # Check if the plant's sun requirements match the selected option
                if sun_options[selected_sun_option].lower() in plant_sun_req:
                    matching_plants.append(attributes)

                # Stop after finding 5 matching plants
                if len(matching_plants) >= 5:
                    break

            # Display the matching plants
            if matching_plants:
                for attributes in matching_plants:
                    st.subheader(f"Plant: {attributes.get('name')}")
                    st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
                    st.write(f"**Description:** {attributes.get('description')}")
                    st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
                    st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
                    st.write(f"**Spread:** {attributes.get('spread')}")
                    st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
                    st.write(f"**Height:** {attributes.get('height')}")
                    st.write(f"**Tags:** {attributes.get('tags_array')}")

                    # Display plant image if available
                    main_image = attributes.get('main_image_path')
                    if main_image:
                        st.image(main_image, caption="Main Image", use_column_width=True)
                    st.write("---")  # Divider between plants
            else:
                st.write("No plants found with the selected sunlight requirement.")
        else:
            st.write("No plant data available from the API.")
    else:
        st.write(f"Request failed with status code: {response.status_code}")

# Run the function
filter_plants_by_sunlight()
