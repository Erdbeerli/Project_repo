import streamlit as st
import requests

def filter_plants_by_gdd():
    """Displays plants based on user-selected Growing Days requirements."""

    st.title("Filter Plants by Growing Days Requirement")
    st.write("Match the slider to how many days you want to wait")

    # Growing days selection
    gdd = st.slider(label="How many growing days can you wait?", min_value=0, max_value=100)

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
            # Loop through each plant to filter by GDD requirement
            for plant in data['data']:
                attributes = plant.get('attributes', {})
                gdd_all = attributes.get('growing_degree_days', None)

                # Check if gdd_all has a valid value and matches the user's selected GDD
                if gdd_all is not None:
                    try:
                        # Convert gdd_all to an integer for comparison
                        gdd_all = int(gdd_all)
                        if gdd_all == gdd:
                            matching_plants.append(plant)
                    except ValueError:
                        # Skip if gdd_all is not a number
                        continue

                # Stop after finding 10 matching plants
                if len(matching_plants) >= 10:
                    break

        # Display the matching plants if any are found
        if matching_plants:
            for plant in matching_plants:
                attributes = plant['attributes']
                st.write(f"Plant: {attributes.get('name', 'Unknown')}")
        else:
            st.write("No plants found with the selected GDD. Please try a different option.")
    else:
        st.write("There was a big error")            

# Run the function
filter_plants_by_gdd()
