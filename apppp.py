#habe in diesem Dokument nochmals versucht an der Filterfunktion zu arbeiten...
#habe es nicht geschafft nach den tags zu filtern
#dieses Dokument braucht sehr lange für die Ausgabe und funktioniert nicht richtig
#wer wird weiter an der Filter-Funktion arbeiten? 


import streamlit as st
import requests

# Define crop categories
VEGETABLES = [
    "Potato", "Lettuce", "Tomato", "Zucchini", "Cucumber", "Spinach", "Radish", 
    "Kale", "Broccoli", "Cauliflower", "Peas", "Beans", "Onion", "Garlic", 
    "Leek", "Swiss Chard", "Beetroot", "Pumpkin", "Brussels Sprouts", "Celery", 
    "Parsley", "Dill", "Basil", "Cabbage", "Sweet Corn", "Turnip", "Parsnip", 
    "Eggplant", "Pepper"
]

HERBS = [
    "Basil", "Parsley", "Thyme", "Oregano", "Rosemary", "Chives", "Sage", 
    "Mint", "Cilantro", "Dill", "Fennel", "Lavender", "Tarragon", "Lemon Balm", 
    "Marjoram", "Chamomile", "Bay Laurel", "Sorrel", "Lovage", "Cress"
]

def filter_function():
    st.title("Crop Finder")
    st.write("Search for a type of crop and add your specifications.")

    # Predefined options
    category = st.radio("Choose a category:", ["Vegetables", "Herbs", "Both"])

    # Dynamically select the search terms based on the chosen category
    if category == "Vegetables":
        search_terms = VEGETABLES
    elif category == "Herbs":
        search_terms = HERBS
    else:  # Both
        search_terms = VEGETABLES + HERBS

    # Additional filters
    sun_requirement = st.selectbox("How sunny is your place?", ("Any", "Full Sun", "Partial Sun", "Shade"))
    
    spacing_avail = st.selectbox('How much space do you have?', ['A lot', 'A little bit', 'Not much'])
    spacing_ranges = {
        'A lot': lambda spacing: spacing >= 100,
        'A little bit': lambda spacing: 50 < spacing < 100,
        'Not much': lambda spacing: spacing <= 50,
    }

    gdd_avail = st.selectbox('How long do you want to wait?', ['I have time', 'About a semester', 'Less than 2 months'])
    gdd_ranges = {
        'I have time': lambda gdd: gdd >= 365,
        'About a semester': lambda gdd: 90 <= gdd < 365,
        'Less than 2 months': lambda gdd: gdd < 60,
    }

    if st.button("Search"):
        base_url = "https://openfarm.cc/api/v1/crops"
        found_crops = []

        try:
            for crop_name in search_terms:
                response = requests.get(f"{base_url}?filter={crop_name}")
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and data['data']:
                        for crop in data['data']:
                            attributes = crop['attributes']
                            if crop_matches_criteria(
                                attributes, sun_requirement, spacing_ranges[spacing_avail], gdd_ranges[gdd_avail]
                            ):
                                found_crops.append(attributes)
                else:
                    st.write(f"API request failed with status: {response.status_code}")

            # Display results
            if found_crops:
                for crop in found_crops:
                    display_crop_details(crop)
            else:
                st.write("No crops match your specifications.")
        except Exception as e:
            st.write(f"Error: {e}")

def crop_matches_criteria(attributes, sun_requirement, spacing_check, gdd_check):
    # Ensure no critical attribute is None
    if (
        attributes.get('sun_requirements') is None or
        attributes.get('row_spacing') is None or
        attributes.get('growing_degree_days') is None
    ):
        return False
    
    crop_sun_req = attributes.get('sun_requirements', '').lower()
    crop_spacing = int(attributes.get('row_spacing', 0))
    growing_deg_days = int(attributes.get('growing_degree_days', 0))
    
    return (
        (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req) and
        spacing_check(crop_spacing) and
        gdd_check(growing_deg_days)
    )

def display_crop_details(attributes):
    """
    Display crop details, excluding any attributes with a `None` value.
    """
    st.write(f"**Name:** {attributes.get('name')}")
    
    # Check and display each attribute only if it has a value
    description = attributes.get('description')
    if description:
        st.write(f"**Description:** {description}")
    
    sun_requirements = attributes.get('sun_requirements')
    if sun_requirements:
        st.write(f"**Sun Requirements:** {sun_requirements}")
    
    row_spacing = attributes.get('row_spacing')
    if row_spacing:
        st.write(f"**Row Spacing:** {row_spacing}")
    
    growing_degree_days = attributes.get('growing_degree_days')
    if growing_degree_days:
        st.write(f"**Growing Degree Days:** {growing_degree_days}")
    
    st.write("---")

# Run the app
filter_function()
