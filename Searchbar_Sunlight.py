import streamlit as st
import requests

# Set up the Streamlit interface
st.title("OpenFarm Crop Information Finder")
st.write("Search for crop details from OpenFarm, and filter by sunlight requirements.")

# Input field for crop name
crop_name = st.text_input("Enter Crop Name", "parsley")

# Dropdown for selecting sunlight requirement filter
sun_requirement = st.selectbox(
    "Select Your Available Sunlight Requirement",
    ("Any", "Full Sun", "Partial Sun", "Shade")
)

# Button to trigger the API call
if st.button("Search"):
    # Base URL for OpenFarm API
    base_url = "https://openfarm.cc/api/v1/crops"
    
    # Send a GET request to the API with the search term
    response = requests.get(f"{base_url}?filter={crop_name}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Debugging: Print the entire response to check the structure
        # st.write(data)  # Uncomment this line if you want to see the response structure

        # Check if there are results
        if 'data' in data and data['data']:
            found_crops = False  # Flag to track if any crops match the filter

            # Loop through the crops to filter by sunlight requirement
            for crop in data['data']:
                attributes = crop['attributes']
                
                # Safely get the sun requirements and handle potential None values
                crop_sun_req = attributes.get('sun_requirements')
                if isinstance(crop_sun_req, str):
                    crop_sun_req = crop_sun_req.lower()  # Call .lower() if it's a string
                else:
                    crop_sun_req = ''  # Default to an empty string if None

                # Check if the crop's sunlight requirement matches the user's selection
                if (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req):
                    
                    # If a crop matches the filter, display its details
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

                    found_crops = True

            if not found_crops:
                st.write("No crops match the specified sunlight requirement.")
        else:
            st.write("No matching crops found.")
    else:
        st.write(f"Request failed with status code: {response.status_code}")