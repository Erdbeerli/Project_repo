import streamlit as st
import requests

# Set up the Streamlit interface
st.title("OpenFarm Crop Information Finder")
st.write("Search for crop details using the OpenFarm API.")

# Input field for the crop name
crop_name = st.text_input("Enter Crop Name", "parsley")

# Button to trigger API call
if st.button("Search"):
    # Base URL for OpenFarm API
    base_url = "https://openfarm.cc/api/v1/crops"

    # Send a GET request to the API with the search term
    response = requests.get(f"{base_url}?filter={crop_name}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if any data is returned
        if 'data' in data and data['data']:
            # Extract details of the first matching crop
            crop = data['data'][0]
            attributes = crop['attributes']

            # Display crop details
            st.subheader("Crop Details")
            st.write(f"**Name:** {attributes.get('name')}")
            st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
            st.write(f"**Description:** {attributes.get('description')}")
            st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
            st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
            st.write(f"**Spread:** {attributes.get('spread')}")
            st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
            st.write(f"**Height:** {attributes.get('height')}")
            st.write(f"**Tags:** {attributes.get('tags_array')}")

            # Companion link if available
            companions_link = crop['relationships']['companions']['links'].get('related')
            if companions_link:
                st.write(f"[Companion Plants Link]({companions_link})")
        else:
            st.write("No matching crops found.")
    else:
        st.write(f"Request failed with status code: {response.status_code}")