# Required Libraries
import streamlit as st
import pandas as pd

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
   st.subheader("Our goal")
   st.write("With our Gardening App we try to help students life a healthier an happier life...")
   # """spaces between lines
   st.write("In this way, we try to motivate you to lead a healthier life and contribute to urban gardening. Click on the following button to find three reasons why this gardening app could be useful for you.")
   if st.button("Three reasons why you should grow your own vegetables"):
       st.write("""
        1. You have a poor connection to nature due to urban living and staying inside
        2. You eat too much fast food and processed foods
        3. You buy vegetables which are wrapped in a lot of unnecessary plastic""")
   else: 
       st.write("Click the button to learn more about the issues the Gardening App tries to address.")


   st.subheader("Overview over the subpages")
   # """Beschreibung was unter Plant Recommendation angezeigt wird"""
   st.write("Under the 'Plant recommendation' tab, after entering your available space, the amount of sunlight at the planting site and other criteria, you will receive an optimal recommendation as to which plant you should plant.")

   # """Beschreibung was unter I know what I want angezeigt wird"""
   st.write("If you already know which plant you want to plant, you can search for the corresponding plant in the search bar under the 'I know what I want' tab.")

   st.subheader("Origin and Limitations of this WebApp")
   st.write("Our limitations relate to our API. Our selected API is not fully completed for every plant. It is therefore possible that our plant recommendation based on the input of the various criteria does not match your input exactly. However, the next best possible result will be displayed.")
   
    #Searchbar
   search_term = st.text_input('Search for plant')

    #Slider
   st.slider(label="How much space do you have for the plant to spread? Please indicate in cm.", min_value=0, max_value=100)

   #Auswahlfelder
   options = ['Full Sun ☀️', 'Partial Sun 🌤️', 'No Sun, Shadow ☁️']
   defaults = None
   selection = 1
   selected_option = st.multiselect('How sunny is the place for your plant?', options , default=defaults, max_selections=selection)
   

   #Text von Medea
   st.write("""Welcome to the gardening app for students and plant-friends!
   Peterli facilitates growing your own vegetables and herbs: 
   Based on your available space, your water availability and other preferences
   you will receive personalized plant recommendations and instructions:)""")


#PLANT RECOMMENDATION

#DATA ANALYSIS

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
    if st.sidebar.button('Data Analysis'):
        st.session_state['section'] = 'Data Analysis'
    if st.sidebar.button('Marketplace'):
        st.session_state['section'] = 'Marketplace'

    #Anzeigen der jeweiligen Sektion der Website, auf welcher man sich befindet
    if st.session_state['section'] == 'Home':
        Introduction_WebApp()
    elif st.session_state['section'] == 'Plant Recommendations':
        st.title("Plant Recommendations based on your Location")
    elif st.session_state['section'] == 'Data Analysis':
        st.title("Data Analysis")
    elif st.session_state['section'] == 'Marketplace':
       st.title("Marketplace")

#Aufruf der Main Funktion
main()



    






    

  

