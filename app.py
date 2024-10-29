# Required Libraries
import streamlit as st
from Feature_01 import return_even

original_list = [i for i in range(10)]

even_list = return_even(original_list)

#Tab Title (Titel der Registerkarte)
st.set_page_config(page_title="Gardening App for Students", page_icon=":seedling:")

#Title & Intro
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

  

