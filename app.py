# Required Libraries
import streamlit as st

#Tab Title (Titel der Registerkarte)
st.set_page_config(page_title="Gardening App for Students", page_icon=":seedling:")

#Title & Intro
st.title("Peterli")
# """ is needed to make spaces between the lines
st.write("""Welcome to the gardening app for students and plant-friends! 
Peterly facilitates growing your own vegetables and herbs: 
Based on your available space, your water availability and other preferences
you will receive personalized plant recommendations and insstructions:)""")

#Buttons
st.subheader("Peterly tries to help students life a healthier an happier life...") 
if st.button("Three reasons why you should grow your own vegetable"):
  st.write("""
  1. You have a poor connection to nature due to urban living and staying inside
  2. You eat too much fast food and processed foods
  3. You buy vegetables which are wrapped in a lot of unnecessary plastic""")
else: 
  st.write("Click the button to learn more about the issues Peterly tries to address."

  

st.write("yessssss it works!")
st.write("this is so cool")
st.write("I think it works")
st.write("one more time")
st.write("this is cool")
st.write("HELLO")
