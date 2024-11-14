# Required Libraries
import streamlit as st
import pandas as pd
import requests #wichtig für Funktion: search_bar 

#Tab Title (Titel der Registerkarte)
st.set_page_config(page_title="Gardening App for Students", page_icon=":seedling:")

#HERE STARTS OUR PLANT WEB APPLICATION

#HOME: Title & Intro
def Introduction_WebApp():
   """Diese Funktion beinhaltet alles, was auf dem Abschnitt HOME angezeigt werden soll"""
   
   st.title("🌱 Gardening App for Students")
   
   # """ is needed to make spaces between the lines
   st.write("""Welcome to our Gardening App for Students and Plant Lovers.
   With our Gardening App we aim to encourage students to grow more of their
   own vegetables and herbs. Based on your available space, the amount of sunlight
   at the planting site and other criteria, we will recommend personalized plants
   for you to plant!""")
   
     
   #Buttons
   st.subheader("Our goal 🎯")
   st.write("With our Gardening App we try to help students life a healthier an happier life...")
   # """spaces between lines
   st.write("""In this way, we try to motivate you to lead a healthier life and contribute to urban gardening. 
   Click on the following button to find three reasons why this gardening app could be useful for you.""")
   if st.button("Three reasons why you should grow your own vegetables"):
       st.write("""
        1. You have a poor connection to nature due to urban living and staying inside
        2. You eat too much fast food and processed foods
        3. You buy vegetables which are wrapped in a lot of unnecessary plastic""")
   else: 
       st.write("Click the button to learn more about the issues the Gardening App tries to address.")


   st.subheader("Overview over the subpages 🧭")
   # """Beschreibung was unter Plant Recommendation angezeigt wird"""
   st.write("""💡   Under the 'Plant recommendation' tab, after entering your available space, the amount of sunlight at the 
   planting site and other criteria, you will receive an optimal recommendation as to which plant you should plant.""")

   # """Beschreibung was unter I know what I want angezeigt wird"""
   st.write("🔎   If you already know which plant you want to plant, you can search for the corresponding plant in the search bar under the 'I know what I want' tab.")

   st.subheader("Who We Are 👩🏼‍💻🧑🏻‍💻👩🏽‍💻🧑🏼‍💻👩🏻‍💻") 
   #Text überarbeitet mit ChatGPT
   st.write("""We are a team of five bachelor`s students at the University of St. Gallen, united
   by a shared passion for business administration and a drive to make impact. Since september, we have been 
   enrolled in the course "Fundamentals and Methods of Computer Science", which inspired us to dive into 
   practical programming and create this WebApp as part of our learning journey.""")
   st.write("""Our goal is to support other fellow students to lead healthier and happier lives
   with our WebApp. Although we are not computer scientists (or magicians!) 
   we are dedicated to bringing our vision to life as effectively as possible.
   That said, our project does have some limitations, and we are always open to feedback.""")
   st.write("""Let us know if you have any suggestions for improvement - we`d love to hear from you!""")
   #should we add a contact here??? 

   
   st.subheader("Limitations ⚠️")
   st.write("""Our limitations relate to our API. Our selected API is not fully completed for every plant. 
   It is therefore possible that our plant recommendation based on the input of the various criteria does
   not match your input exactly. However, the next best possible result will be displayed.""")
   

    #Slider
   st.slider(label="How much space do you have for the plant to spread? Please indicate in cm.", min_value=0, max_value=100)

   #Auswahlfelder
   options = ['Full Sun ☀️', 'Partial Sun 🌤️', 'No Sun, Shadow ☁️']
   defaults = None
   selection = 1
   selected_option = st.multiselect('How sunny is the place for your plant?', options , default=defaults, max_selections=selection)


#PLANT RECOMMENDATION

#I KNOW WHAT I WANT: Search bar
def search_bar():
   """Diese Funktion erlaubt eine gezielte Suchanfrage für eine Pflanze."""
   
   #import requests is needed here
   st.title("Find vegetable informations here")
   st.write("Search for a specific vegetable or herb and find out more about the plant details.")

   #Input field for vegetable/herb name
   plant_name = st.text_input("Enter vegetable or herb name:", "e.g. tomato 🍅")

   #Button to start the API contact
   if st.button("Search"):
       # Base URL for OpenFarm API (supported by ChatGPT)
       base_url = "https://openfarm.cc/api/v1/crops"
       
       #Send a GET request to the API with the search term (supported by ChatGPT)
       response = requests.get(f"{base_url}?filter={plant_name}")
       
       # Check if the request was successful (supported by ChatGPT)
       if response.status_code == 200:
            data = response.json()
        
            # Check if any data is returned (supported by ChatGPT)
            if 'data' in data and data['data']:
            # Extract details of the first matching plant
                plant = data['data'][0]
                attributes = plant['attributes']

                #Display plant details (supported by ChatGPT)
                st.subheader("Plant Details")
                st.write(f"**Name:** {attributes.get('name')}")
                st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
                st.write(f"**Description:** {attributes.get('description')}")
                st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
                st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
                st.write(f"**Spread:** {attributes.get('spread')}")
                st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
                st.write(f"**Height:** {attributes.get('height')}")
                st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
                

                #i think we should delete companion link because it doesn`t work and add picture or sth. instead???
                # Companion link if available
                companions_link = plant['relationships']['companions']['links'].get('related')
                if companions_link:
                    st.write(f"[Companion Plants Link]({companions_link})")

            else:
                st.write("No matching plants found.")
                #could we add here something to get an output anyway? ChatGPT, Wikipedia,...???
       else:
           st.write(f"Request failed with status code: {response.status_code}")
   
def filter_function():
       # Set up the Streamlit interface
    st.title("Crop Finder")
    st.write("Search for a type of crop and add your specifications regarding sun or row spacing.")

    # Input field for crop name
    crop_name = st.text_input("Enter Crop Name", "maybe parsley?")

    # All the filters for sunlight, growing days, row spacing and spread

    #SUNLIGHT
    # Dropdown for selecting sunlight requirement filter
    sun_requirement = st.selectbox(
        "How sunny is your place?",
        ("Any", "Full Sun", "Partial Sun", "Shade")
    )

    #ROW SPACING
    # Define the spacing options
    spacing_list = {
        'A lot': int(2000),
        'A little bit': int(1000),
        'Not much': int(90)
    }
    # Select the spacing availability and convert the selected value to an integer
    spacing_avail = st.selectbox('How much space do you have?', list(spacing_list.keys()))
    spacing_value = spacing_list[spacing_avail]  # Convert the selected spacing to an integer value

    #GROWING DEGREE DAYS (GDD)
    time_list = {
        'I have time': int(2000),
        'One or Two years': int(500),
        'Less than a year': int(200)
    }
    gdd_avail = st.selectbox('How long do you want to wait?', list(time_list.keys()))
    gdd_avail_value = time_list[gdd_avail] # Convert the selected timeframe to an integer value

    # Button to trigger the API call
    if st.button("Search"):
        # Base URL for OpenFarm API
        base_url = "https://openfarm.cc/api/v1/crops"
        
        # Send a GET request to the API with the search term
        response = requests.get(f"{base_url}?filter={crop_name}")

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Check if there are results
            if 'data' in data and data['data']:
                found_crops = False  # Flag to track if any crops match the filter

                # Loop through the crops to filter by sunlight requirement
                for crop in data['data']:
                    attributes = crop['attributes']
                    
                    # Safely get the sun requirements and handle potential None values
                    crop_sun_req = attributes.get('sun_requirements') # Actual sunlight requirement from the API
                    crop_spacing = attributes.get('row_spacing') or 0  # Default to 0 if None
                    growing_deg_days = attributes.get('growing_degree_days') or 0  # Default to 0 if None

                    if isinstance(crop_sun_req, str):
                        crop_sun_req = crop_sun_req.lower()  # Convert to lowercase if it's a string
                    else:
                        crop_sun_req = ''  # Default to an empty string if None

                    # Check if the crop's sunlight requirement matches the user's selection
                    if (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req):
                        
                        # Ensure there is a valid spacing value
                        if spacing_value >= int(crop_spacing):  # Compare with the selected spacing value

                            if gdd_avail_value >= int(growing_deg_days):
                            
                                # If a crop matches the filter, display its details
                                st.subheader("Crop Details")
                                st.write(f"**Name:** {attributes.get('name')}")
                                st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
                                st.write(f"**Description:** {attributes.get('description')}")
                                st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
                                st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
                                st.write(f"**Spread:** {attributes.get('spread')}")
                                st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
                                st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
                                st.write(f"**Height:** {attributes.get('height')}")
                                st.write(f"**Tags:** {attributes.get('tags_array')}")
                                
                                found_crops = True

                if not found_crops:
                    st.write("No crops match the specified sunlight requirement.")
            else:
                st.write("No matching crops found.")
        else:
            st.write(f"Request failed with status code: {response.status_code}")


#MARKETPLACE


#Seitennavigation (in Anlehnung an Streamlit_Project.py von Bookly)
def main():
    """
    Die Hauptfunktion der Streamlit-Anwendung, die die Navigation und die Anzeige der verschiedenen Fenstern
    steuert. Nutzer können über den Sidebar zwischen verschiedenen Abschnitten wie 'Home', 'Plant Recommendations',
    'Data Analysis' und 'Marketplace' wählen. Die entsprechenden Inhalte werden basierend auf der Auswahl angezeigt.

    Innerhalb der 'Data Analysis' Sektion können Benutzer...

    Die Anwendung verwendet 'st.session_state' für die Zustandsverwaltung zwischen den Seitenaufrufen.
    Dies ermöglicht eine dynamische Interaktion ohne Datenverlust bei Neuladen der Seite.
    """

    if 'section' not in st.session_state:
        st.session_state['section'] = 'Home'

    #Navgiation mithilfe der Sidebar
    if st.sidebar.button('Home'):
        st.session_state['section'] = 'Home'
    if st.sidebar.button("Plant Recommendations"):   
        st.session_state['section'] = 'Plant Recommendations'
    if st.sidebar.button('I know what I want'):
        st.session_state['section'] = 'I know what I want'
    if st.sidebar.button('Marketplace'):
        st.session_state['section'] = 'Marketplace'

    #Anzeigen der jeweiligen Sektion der Website, auf welcher man sich befindet
    if st.session_state['section'] == 'Home':
        Introduction_WebApp()
    elif st.session_state['section'] == 'Plant Recommendations':
        st.title("Plant Recommendations based on your Location")
        filter_function()
         
    elif st.session_state['section'] == 'I know what I want':
        search_bar()
    elif st.session_state['section'] == 'Marketplace':
       st.title("Marketplace")

#Aufruf der Main Funktion
main()
