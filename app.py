# Required Libraries
import streamlit as st
import pandas as pd

#Tab Title (Titel der Registerkarte)
st.set_page_config(page_title="Gardening App for Students", page_icon=":seedling:")

#HERE STARTS OUR PLANT WEB APPLICATION

#Home: Title & Intro
def Introduction_WebApp():
   st.title("🌱 Peterli")
   
   # """ is needed to make spaces between the lines
   st.write("""Welcome to the gardening app for students and plant-friends!
  Peterli facilitates growing your own vegetables and herbs: 
  Based on your available space, your water availability and other preferences
  you will receive personalized plant recommendations and instructions:)""")
   
   #Buttons
   st.subheader("Peterli tries to help students life a healthier an happier life...") 
   if st.button("Three reasons why you should grow your own vegetables"):
       st.write("""
        1. You have a poor connection to nature due to urban living and staying inside
        2. You eat too much fast food and processed foods
        3. You buy vegetables which are wrapped in a lot of unnecessary plastic""")
   else: 
       st.write("Click the button to learn more about the issues Peterli tries to address.")


    #Searchbar
   search_term = st.text_input('Suche nach Pflanze')

    #Slider
   st.slider(label="how sunny is your plant's location", min_value=0, max_value=100)


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



    






    

  

