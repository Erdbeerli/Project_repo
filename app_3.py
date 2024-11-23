# Required Libraries
import streamlit as st
import pandas as pd
import requests #wichtig für Funktion: search_bar and filter_function 

#Tab Title (Titel der Registerkarte)
st.set_page_config(page_title="Gardening App for Students", page_icon=":seedling:")

#HERE STARTS OUR PLANT WEB APPLICATION

#Feedback-Form
def collect_feedback():
    """Collect user feedback from the web app."""
    
    # Create a text area for users to enter their feedback
    feedback = st.text_area("Let us know if you have any suggestions for improvement:")


    # If the user clicks the submit button
    if st.button("Submit Feedback"):
        if feedback:
            # Here you can save the feedback to a file, database, or send it via email
            with open("user_feedback.txt", "a") as f:
                f.write(f"Feedback: {feedback}\n")

            st.success("Thank you for your feedback! We really appreciate it.")
        else:
            st.warning("Please enter some feedback before submitting.")

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

   st.write("🥦🥕🥬🥒🌱🍅🧅🧄🌶️🌽🍆🫑🥑🫛🫘🍠🍅🥦🥕🥬🥒🌱🍅🧅🧄🌶️🌽🍆🫑🥑🫛🫘🍠")
    
   #Buttons
   st.subheader("Our goal 🎯")
   st.write("With our Gardening App we try to help students live a healthier an happier life...")
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

   st.write("---")
   st.subheader("Overview over the subpages 🧭")
   # """Beschreibung was unter Plant Recommendation angezeigt wird"""
   st.write("""💡   Under the 'Plant Recommendations' tab, after entering your available space, the amount of sunlight at the 
   planting site and other criteria, you will receive an optimal recommendation as to which plant you should plant.""")

   # """Beschreibung was unter I know what I want angezeigt wird"""
   st.write("🔎   If you already know which plant you want to plant, you can search for the corresponding plant in the search bar under the 'I know what I want' tab.")

   st.write("---")
   st.subheader("Who We Are 👩🏼‍💻🧑🏻‍💻👩🏽‍💻🧑🏼‍💻👩🏻‍💻") 
   #Text überarbeitet mit ChatGPT
   st.write("""We are a team of five bachelor`s students at the University of St. Gallen, united
   by a shared passion for business administration and a drive to make an impact. Since september, we have been 
   enrolled in the course "Fundamentals and Methods of Computer Science", which inspired us to dive into 
   practical programming and create this WebApp as part of our learning journey.""")
   st.write("""Our goal is to support other fellow students to lead healthier and happier lives
   with our WebApp. Although we are not computer scientists (or magicians ;)carr) 
   we are dedicated to bringing our vision to life as effectively as possible.
   That said, our project does have some limitations, and we are always open to feedback.""")
   #st.write("""Let us know if you have any suggestions for improvement - we`d love to hear from you!""")
   #should we add a contact here???
    
   # Call the function to display the feedback section
   collect_feedback()
   
   st.write("---")
   st.subheader("Limitations ⚠️")
   st.write("""Our limitations relate to our API. Our selected API ([OpenFarm About](https://openfarm.cc/pages/about?locale=en)) is not fully completed for every plant. 
   It is therefore possible that our plant recommendation based on the input of the various criteria or the search result does
   not always match your input exactly. However, the next best possible result will be displayed.""")


#I KNOW WHAT I WANT: Search bar
def search_bar():
    """Diese Funktion erlaubt eine gezielte Suchanfrage für eine Pflanze."""
    
    st.title("Vegetable and Herb Information")
    st.subheader("Get detailed plant information based on your search")
    st.write("Search for a specific vegetable or herb and find out more about its details.")
    
    # Eingabefeld für den Namen der Pflanze
    plant_name = st.text_input("Enter vegetable or herb name:", "e.g., tomato 🍅")
    
    # Button zur API-Anfrage
    if st.button("Search"):
        # Basis-URL für OpenFarm API
        base_url = "https://openfarm.cc/api/v1/crops"
        
        # Anfrage an die API senden
        try:
            response = requests.get(f"{base_url}?filter={plant_name}")
            if response.status_code == 200:
                data = response.json()
                
                # Überprüfen, ob Daten vorhanden sind
                if 'data' in data and data['data']:
                    # Filter: Nur Pflanzen mit dem Tag `vegetable` oder `herb`
                    filtered_plants = [
                        plant for plant in data['data'] 
                        if "tags_array" in plant['attributes'] and 
                        any(tag in ["vegetable", "herb"] for tag in plant['attributes']['tags_array'])
                    ]
                    
                    if filtered_plants:
                        # Details der ersten passenden Pflanze anzeigen
                        plant = filtered_plants[0]  # Erste passende Pflanze
                        attributes = plant['attributes']



                        # Pflanzendetails anzeigen OHNE FORMATIERUNG
                        #st.subheader("Plant Details")
                        #st.write(f"**Name:**                {attributes.get('name')}")
                        #st.write(f"**Binomial Name:**       {attributes.get('binomial_name')}")
                        #st.write(f"**Description:**         {attributes.get('description')}")
                        #st.write(f"**Sun Requirements:**    {attributes.get('sun_requirements')}")
                        #st.write(f"**Sowing Method:**       {attributes.get('sowing_method')}")
                        #st.write(f"**Spread:**              {attributes.get('spread')}")
                        #st.write(f"**Row Spacing:**         {attributes.get('row_spacing')}")
                        #st.write(f"**Height:**              {attributes.get('height')}")
                        #st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
                        #st.write(f"**Tags:**                {attributes.get('tags_array')}")


                        # Renaming an existing field for display as 'Days to harvest'
                        # using 'growing_degree_days' as a substitute for "Days to harvest"
                        days_to_harvest = attributes.get('growing_degree_days', 'N/A')  # Default to 'N/A'

                        #plant details formated as a table
                        st.subheader("Plant Details")

                        details_table = f"""
                        <table style="width:100%; text-align:left;">
                            <tr><th style="width:30%;">Attribute</th><th>Value</th></tr>
                            <tr><td><strong>Name:</strong></td><td>{attributes.get('name', 'N/A')}</td></tr>
                            <tr><td><strong>Binomial Name:</strong></td><td>{attributes.get('binomial_name', 'N/A')}</td></tr>
                            <tr><td><strong>Description:</strong></td><td>{attributes.get('description', 'N/A')}</td></tr>
                            <tr><td><strong>Sun Requirements:</strong></td><td>{attributes.get('sun_requirements', 'N/A')}</td></tr>
                            <tr><td><strong>Sowing Method:</strong></td><td>{attributes.get('sowing_method', 'N/A')}</td></tr>
                            <tr><td><strong>Spread:</strong></td><td>{attributes.get('spread', 'N/A')}</td></tr>
                            <tr><td><strong>Row Spacing:</strong></td><td>{attributes.get('row_spacing', 'N/A')}</td></tr>
                            <tr><td><strong>Height:</strong></td><td>{attributes.get('height', 'N/A')}</td></tr>
                            <tr><td><strong>Days to harvest:</strong></td><td>{days_to_harvest}</td></tr> 
                            <tr><td><strong>Tags:</strong></td><td>{", ".join(attributes.get('tags_array', [])) or "No tags available"}</td></tr>
                        </table>
                        """

                        st.markdown(details_table, unsafe_allow_html=True)

                        st.write("")

                        
                        # Bild anzeigen, falls verfügbar
                        image_url = attributes.get('main_image_path')
                        if image_url:
                            st.image(image_url, caption=attributes.get('name'), use_column_width=True)
                    
                    #this is shown when you enter e.g. Apple... so when it has no tag
                    else:
                        st.write("No matching vegetable or herb found.")

                #this in contrast is shown when you enter fsfsf... so when it is not in the API at all
                else:
                    st.write("No matching plants found.")
            else:
                st.write(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            st.write(f"An error occurred: {e}")


#PLANT RECOMMENDATION: Filter Function

def filter_function():
    st.title("Vegetable and Herb Finder")
    st.subheader("Get plant recommendations based on your location")
    st.write("Give us some information about your planned planting location and your patience ;)")


# Vegetables: Potato, Lettuce, Tomato, Zucchini, Cucumber, Spinach, Radish, Kale, Broccoli, Cauliflower, Peas, Beans, Onion, Garlic, Leek, Swiss Chard, Beetroot, Pumpkin, Brussels Sprouts, Celery, Parsley, Dill, Basil, Cabbage, Sweet Corn, Turnip, Parsnip, Eggplant, Pepper
# Herbs: Basil, Parsley, Thyme, Oregano, Rosemary, Chives, Sage, Mint, Cilantro, Dill, Fennel, Lavender, Tarragon, Lemon Balm, Marjoram, Chamomile, Bay Laurel, Sorrel, Lovage, Cress

    crop_name = "Potato", "Lettuce", "Tomato", "Zucchini", "Cucumber", "Spinach", "Radish", "Kale", "Broccoli", "Cauliflower", "Peas", "Beans", "Onion", "Garlic", "Leek", "Swiss Chard", "Beetroot", "Pumpkin", "Brussels Sprouts", "Celery", "Parsley", "Dill", "Basil", "Cabbage", "Sweet Corn", "Turnip", "Parsnip", "Eggplant", "Pepper", "Basil", "Parsley", "Thyme", "Oregano", "Rosemary", "Chives", "Sage", "Mint", "Cilantro", "Dill", "Fennel", "Lavender", "Tarragon", "Lemon Balm", "Marjoram", "Chamomile", "Bay Laurel", "Sorrel", "Lovage", "Cress"
    sun_requirement = st.selectbox("☀️ How sunny is your place?", ("Any", "Full Sun", "Partial Sun"))

    
    # small spread 10-30cm / medium spread 30-60cm / large spread 60cm and more 
    spacing_list = {'Any': 200, 'A lot (between 60 and 200cm)': 200, 'Some space (max. 60cm)': 60, 'A little bit (max. 30cm)': 30}
    spacing_avail = st.selectbox('📐 How much space do you have?', list(spacing_list.keys()))
    spacing_value = spacing_list[spacing_avail]
    

    # short harvest time 0-60days / medium 60-120 days / long 120+ days
    time_list = {'Any': 300, 'I have time (up to a year)': 300, 'About a semester (4 months)': 120, 'Not much (2 months)': 60}
    gdd_avail = st.selectbox('⏳ How long do you want to wait?', list(time_list.keys()))
    gdd_avail_value = time_list[gdd_avail]

    st.write("The following vegetables and/or herbs meet your requirements...")

    if st.button("Search"):
        base_url = "https://openfarm.cc/api/v1/crops"
        try:
            response = requests.get(f"{base_url}?filter={crop_name}")  #(f"**Tags:** {attributes.get('tags_array')}") = was hat "tags für einen Parameter" -> ich gebe im get request nur den parameter und es sucht den parameter
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']:
                    for crop in data['data']:
                        attributes = crop['attributes']
                        if crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value):
                            display_crop_details(attributes)
                else:
                    st.write("No crops match your specifications.")
            else:
                st.write(f"API request failed with status: {response.status_code}")
        except Exception as e:
            st.write(f"Error: {e}")

def crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value):
    crop_sun_req = (attributes.get('sun_requirements') or '').lower()
    crop_spacing = attributes.get('row_spacing') or 0
    growing_deg_days = attributes.get('growing_degree_days') or 0
    return (
        (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req) and
        spacing_value >= int(crop_spacing) and
        gdd_avail_value >= int(growing_deg_days)
    )

def display_crop_details(attributes):
    st.write(f"**Name:** {attributes.get('name')}")
    #st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
    st.write(f"**Description:** {attributes.get('description')}")
    # st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
    st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
    #st.write(f"**Spread:** {attributes.get('spread')}")
    #st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
    #st.write(f"**Height:** {attributes.get('height')}")
    # st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
    st.write(f"**Tags:** {attributes.get('tags_array')}")
    st.write("---")



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
        filter_function()
         
    elif st.session_state['section'] == 'I know what I want':
        search_bar()
    elif st.session_state['section'] == 'Marketplace':
       st.title("Coming soon... 🥦🍅🥕")
   

#Aufruf der Main Funktion
main()
