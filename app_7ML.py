# Required Libraries
# it might be necessary to enter "pip install matplotlib" into your terminal
import streamlit as st
import pandas as pd
import requests # used for fetching data from the API (search_bar, filter_function)
import matplotlib.pyplot as plt # important for data visualization (display_bar_chart)
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

#Tab Title = Titel der Registerkarte
st.set_page_config(page_title="Gardening Web App for Students")

#HERE STARTS OUR PLANT WEB APPLICATION

#Feedback-Form on the HOME tab (supported by: ChatGPT)
def collect_feedback():
    """
    This function collects user feedback from the user on streamlit in a simple form.
    The shared feedback will be locally stored in a text file on the computer where the
    python code file is stored too.

    """
    
    # Create a text input area for users to enter their feedback
    feedback = st.text_area("Let us know if you have any suggestions for improvement:")

    # If the user clicks the submit button
    if st.button("Submit Feedback"):
        if feedback:
            # Here feedback will be appended to a text file
            with open("user_feedback.txt", "a") as f:
                f.write(f"Feedback: {feedback}\n")

            st.success("Thank you for your feedback! We really appreciate it.")
        else:
            st.warning("Please enter some feedback before submitting.")


#HOME: Title & Intro
def Introduction_WebApp():
   """
   This function contains everything that is shown on the page HOME. 

   """

   st.title("Gardening Web App for Students 🌱")
   st.write("**Welcome to our Gardening Web App for Students and Plant Lovers!**")
   st.write("""With this app, we want to encourage students to grow their
   own vegetables and herbs. Based on your available space, the amount of sunlight
   at the planting site and your patience, you will receive personalized recommendations 
   for the best herbs and vegetables to plant!""")
    # """ is used to create spaces between the lines
    # ** are used to format the text bold

   st.write("🥦🥕🥬🥒🌱🍅🧅🧄🌶️🌽🍆🫑🥑🫛🫘🍠🍅🥦🥕🥬🥒🌱🍅🧅🧄🌶️🌽🍆🫑🥑🫛🫘")
   st.write("---")
    
   # Button and information for the user (supported by: 30 Days Streamlit Challenge https://30days-tmp.streamlit.app/?challenge=Day+3)

   st.subheader("Our goal 🎯")
   st.write("We aim to help students lead healthier an happier lives...")
   st.write("""With this web app and our personalized recommendations, we make it easy for you
    to start your own small urban garden - no matter how much time or space you have. Urban gardening 
    is not just about growing your own food... so click on the following button to find three reasons 
    why this gardening app could be useful for you.""")
   
   if st.button("Three reasons why you should grow your own herbs and vegetables"):
       st.write("""
        1. You feel disconnected from nature due to urban living and staying indoors.
        2. You eat too much fast food and processed foods.
        3. You often buy vegetables that are wrapped in a lot of unnecessary plastic.""")
   else: 
       st.write("Click the button to learn more about the main issues the gardening app tries to address.")

   st.write("---")

   st.subheader("Overview over the subpages 🧭")
   # description about what to expect under "plant recommendation" tabs
   st.write("""💡   Under the '_Vegetable Recommendations_' and '_Herb Recommendations_' tabs, after entering your available space, 
   the amount of sunlight at the planting site, and your patience, you will receive an optimal recommendation for which plant you should grow.""")

   # description about what to expect under the "I Know What I Want" tab
   st.write("🔎   If you already know which plant you want to grow, you can search for it in the search bar under the '_I Know What I Want_' tab.")

   st.write("---")

   st.subheader("Who We Are 👩🏼‍💻🧑🏻‍💻👩🏽‍💻🧑🏼‍💻👩🏻‍💻") 
   # the following text was revised with: ChatGPT
   st.write("""We are a team of five bachelor's students at the University of St. Gallen, united
   by a shared passion for business administration and a drive to make an impact. Since september, we have been 
   enrolled in the course "Fundamentals and Methods of Computer Science", which inspired us to dive into 
   practical programming and create this WebApp as part of our learning journey.""")
   st.write("""Our goal is to support other fellow students to lead healthier and happier lives
   with our gardening web app. Although we are not computer scientists (or magicians ;)) 
   we are dedicated to bringing our vision to life as effectively as possible.
   That said, our project does have some limitations, and we are always open to feedback.""")
    
   # Function call to display the feedback section
   collect_feedback()
   
   st.write("---")

   st.subheader("Limitations ⚠️")
   st.write("""Our limitations relate to our API. Our selected API ([OpenFarm About](https://openfarm.cc/pages/about?locale=en))
   is unfortunately not fully completed for every plant. It is therefore possible that our plant recommendation based on the input
   of the various criteria or the search result does
   not always match your input exactly. However, the next best possible result will be displayed.""")


#I KNOW WHAT I WANT: Search bar (supported by: the OpenFarm API documentation "https://github.com/openfarmcc/OpenFarm/blob/mainline/docs/api_docs.md" and ChatGPT )
def search_bar():
    """
    This search_bar function enables users to search for a specific plant. 
    Then it retrieves data from the OpenFarm API.
    Finally it displays the data in a user-friendly format (table & image if available)
    
    """
    
    # Feature explanations for the user
    st.title("Vegetable and Herb Information")
    st.subheader("Get detailed plant information based on your search")
    st.write("Search for a specific vegetable or herb and find out more about its details.")
    
    # Input field for a plant name
    plant_name = st.text_input("Enter vegetable or herb name:", "e.g., tomato 🍅") #tomato serves here as a default example 
    
    # Button that triggers API request
    if st.button("Search"):
        # Basis-URL für OpenFarm API
        base_url = "https://openfarm.cc/api/v1/crops"
        
        # send request to the API the plant_name serves hereby as a filter parameter
        try:
            response = requests.get(f"{base_url}?filter={plant_name}")
            if response.status_code == 200: #status code 200 means tha API call was successful
                data = response.json()
                
                # check if data is available
                if 'data' in data and data['data']: # list of plant data

                    # additional filter using the tags_array attribute: only return plants with the tag `vegetable` or `herb` 
                    filtered_plants = [
                        plant for plant in data['data'] 
                        if "tags_array" in plant['attributes'] and 
                        any(tag in ["vegetable", "herb"] for tag in plant['attributes']['tags_array'])
                    ]
                    
                    if filtered_plants:
                        # show details for the first matching plant
                        plant = filtered_plants[0]  # first matching plant
                        attributes = plant['attributes']

                        # all possible plant details without formating
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

                        # Renaming an existing field and display as 'Days to harvest'
                        # using 'growing_degree_days' as a substitute for "Days to harvest"
                        days_to_harvest = attributes.get('growing_degree_days', 'N/A')  # Default to 'N/A'

                        # plant details formated as a table (supported by: ChatGPT)
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

                        # show a picture if available
                        image_url = attributes.get('main_image_path')
                        if image_url:
                            st.image(image_url, caption=attributes.get('name'), use_column_width=True)
                    
                    # this is shown when you enter e.g. Apple... so when it has no tag
                    else:
                        st.write("No matching vegetable or herb found.")

                # this in contrast is shown when you enter fsfsf... so when it is not in the API at all
                else:
                    st.write("No matching plants found.")

            # this is shown when the API request failed
            else:
                st.write(f"Request failed with status code: {response.status_code}")
            
        except Exception as e:
            st.write(f"An error occurred: {e}")


#HERB RECOMMENDATION: Filter Function Herbs (supported by: ChatGPT)

def filter_function_herb():
    """
    This function contains everything that is needed for the herb recommendations.
    Based on 3 input parameters (sunlight, space and patience) the user can select his/her preferenced growing conditions.
    A list of herbs gets fetched from the OpenFarm API including their plant details. 
    Herbs are filtered based on the users input.
    Herbs and some of their details are displayed in a userfriendly way (including a bar chart for data visualization).

    """

    # Feature explanations for the user
    st.title("Herb Finder")
    st.subheader("Get plant recommendations based on your location")
    st.write("""On this page, the recommendations will provide you with an initial idea of plants 
    you can grow at home. For more detailed information, you can simply enter the plant name in the search bar on the '_I Know What I Want_' page.""")
    st.write("**Give us some information about your planned planting location and your patience ;)**")

    # According to this API Documentation "https://github.com/openfarmcc/OpenFarm/blob/mainline/docs/api_docs.md" crops need a filter to return something.
    # It was unfortunately not possible to query for the tag_array in the OpenFarm API. Therefore we needed to make a preselection based on the most common herbs in Switzerland.
    # Common herbs in Switzerland are mainly based on the seasonal calender from Swiss Farmers (source: https://www.swiss-farmers.ch/seasonal-calendar/) 
    # Basil, Chamomile, Chives, Cilantro, Cress, Dill, Fennel, Lemon Balm, Lovage, Marjoram, Oregano, Parsley, Peppermint, Rosemary, Saffron, Sage, Savory, Sorrel, Tarragon
    crop_name = "Sorrel, Rumex acetosa, Parsley, Thyme, Italian Oregano, Basil, Cilantro, Sage, Chives, Fernleaf Dill, Chamomile, Tarragon, Cress,lepidium sativum, Lovage, Mentha spicata / Mentha viridis, Summer Savory, Rosmarinus officinalis, Saffron, Fennel"
    # However there were crops that needed their binominal name too. In addition to that three crops did not work well with the others and where therefore left out. These are: "Rosemary", "Lemon Balm", "Marjoram"


    # Options for selection or input parameters
  
    #selectbox to indicate how sunny the place is
    sun_requirement = st.selectbox("☀️ How sunny is your place?", ("Any", "Full Sun", "Partial Sun"))
    
    #this dictionary is used to link user-friendly categories with concrete distance specifications and quickly access the numeric values that correspond to each description
    spacing_list = {'Any': 200, 'A lot (between 60 and 200cm)': 200, 'Some space (max. 60cm)': 60, 'A little bit (max. 30cm)': 30}
    #selectbox to indicate how much space is available. The selection consists of the dictionary 'spacing_list'.
    spacing_avail = st.selectbox('📐 How much space do you have?', list(spacing_list.keys()))
    #this line translates the entered value into an exact numerical value and is assigned to the 'spacing_value' variable
    spacing_value = spacing_list[spacing_avail]
    # small spread 0-30cm / medium spread 31-60cm / large spread 60cm and more 

    #this dictionary is used to link user-friendly categories with concrete time specifications and quickly access the numeric values that correspond to each description
    time_list = {'Any': 300, 'I have time (up to a year)': 300, 'About a semester (4 months)': 120, 'Not much (2 months)': 60}
    #selectbox to indicate how long you want to wait. The selection consists of the dictionary 'time_list'.
    gdd_avail = st.selectbox('⏳ How long do you want to wait?', list(time_list.keys()))
    #this line translates the entered value into an exact numerical value and is assigned to the 'ggd_avail_value' variable
    gdd_avail_value = time_list[gdd_avail]
    # short harvest time 0-60days / medium 61-120 days / long 120+ days

    st.write("The following vegetables and/or herbs meet your requirements...")

    # Button that triggers API request

    if st.button("Search"):
        base_url = "https://openfarm.cc/api/v1/crops"
        try:
            response = requests.get(f"{base_url}?filter={crop_name}")  # App sends a request to the API with a predefined list of herbs
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']:
                    for crop in data['data']:
                        attributes = crop['attributes']
                        if crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value): # checking if user preferences are met
                            display_crop_details(attributes) # show the recommended herbs
                else:
                    st.write("No crops match your specifications.")
            else:
                st.write(f"API request failed with status: {response.status_code}")
        except Exception as e:
            #st.write(f"Error: {e}")
            st.write("...")


# Filtering based on selected user input
def crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value):
    """
    This function filters the herbs based on the users input so that all preferences are met.
    
    """
    crop_sun_req = (attributes.get('sun_requirements') or '').lower()
    crop_spacing = attributes.get('spread')
    growing_deg_days = attributes.get('growing_degree_days')

    return (
        (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req) and
        spacing_value >= int(crop_spacing) and
        gdd_avail_value >= int(growing_deg_days)
    )

# Data Visualization, horizontal bar chart for herbs (supported by: ChatGPT)
def display_bar_chart_herb(attributes):
    """
    This function visualizes the spread in a bar chart.
    
    """
    # Default average spread for all plants
    average_spread_herb = 35
    # Actual spread for the plant (fetch from attributes)
    plant_spread_herb = attributes.get('spread', average_spread_herb)  # Default to average if not provided

    # Definition plant_name for the label
    plant_name_herb = attributes.get('name')

    # Horizontal bar chart
    plt.figure(figsize=(6, 1))
    
    # Modify y-values to increase space between bars
    y_values = [1, 1.4]  # Further spacing between bars
    x_values = [average_spread_herb, plant_spread_herb]
    
    # barh is used if you want the bar to be horizontal not vertical
    # Adjust bar height for thinner bars, add color and label
    plt.barh(y_values, x_values, color=['grey', 'green'], height=0.3, tick_label=["Average", plant_name_herb])
    
    # Adjust font size for title and labels
    plt.xlabel("Spread (cm)", fontsize=7)
    plt.title(f"Spread Comparison for {attributes.get('name', 'Unknown Plant')}", fontsize=9)
    
    # Adjust y-ticks and make the text smaller
    plt.yticks([1, 1.4], labels=["Average", plant_name_herb], fontsize=7)

    plt.tick_params(axis='x', labelsize=6)  # Change font size of the x-axis numbers
    
    # Display the plot
    st.pyplot(plt)

# Display recommended crops and their details
def display_crop_details(attributes):
    """
    This function is needed to display chosen attributes of the plants.
    It also contains (calls) the bar_chart function.

    """
    st.subheader(f"__{attributes.get('name')}__")
    #st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
    st.write(f"**Description:** {attributes.get('description')}")
    # st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
    st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
    #st.write(f"**Spread:** {attributes.get('spread')}")
    #st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
    #st.write(f"**Height:** {attributes.get('height')}")
    # st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
    st.write(f"**Tags:** {attributes.get('tags_array')}")

    # Call the bar chart display function
    display_bar_chart_herb(attributes)

    st.write("---")


#VEGETABLE RECOMMENDATION: Filter Function Vegetables (supported by: ChatGPT)

def filter_function_vegetable():
    """
    This function contains everything that is needed for the vegetable recommendations.
    Based on 3 input parameters (sunlight, space and patience) the user can select his/her preferenced growing conditions.
    A list of vegetables gets fetched from the OpenFarm API including their plant details. 
    Vegetables are filtered based on the users input.
    Vegetables and some of their details are displayed in a userfriendly way (including a bar chart for data visualization).

    """
    
    # Feature explanations for the user
    st.title("Vegetable Finder")
    st.subheader("Get plant recommendations based on your location")
    st.write("On this page, the recommendations will provide you with an initial idea of plants you can grow at home. For more detailed information, you can simply enter the plant name in the search bar on the '_I Know What I Want_' page.")
    st.write("**Give us some information about your planned planting location and your patience ;)**")

    
    # According to this API Documentation "https://github.com/openfarmcc/OpenFarm/blob/mainline/docs/api_docs.md" Crops need a filter to return something.
    # It was unfortunately not possible to query for the tag_array in the OpenFarm API. Therefore we needed to make a preselection based on the most common vegetables in Switzerland.
    # Common vegetables in Switzerland were selected based on the seasonal calender from Swiss Farmers (source: https://www.swiss-farmers.ch/seasonal-calendar/) 
    # Beetroot, Bell Pepper, Beans, Broccoli, Brussels Sprouts, Cabbage, Carrot, Cauliflower, Celeriac, Cucumber, Eggplant, Fennel, Garlic, Kale, Leek, Lettuce, Onion, Parsnip, Peas, Potato, Radicchio, Radish, Spinach, Squash, Sweet Corn, Swiss Chard, Tomato, Turnip, Zucchini
    crop_name = "Brassica oleracea", "RedPepper", "Onion", "Carrot", "Potato", "Onion", "Icicle Radish", "Lettuce", "Tomato", "Zucchini", "Zucchini", "Spinach", "Kale", "Broccoli", "Cauliflower", "Peas", "Green Beans", "Leek", "Swiss Chard", "Cabbage", "Beetroot", "Brussels Sprouts", "Celery", "Sweet Corn", "Turnip", "Parsnip", "Eggplant", "Cucumber", "Van Zerden Garlic", "Pepper", "Fennel", "Eggplant", "Radicchio"
    # However there were also crops that did not work well with the others and where therefore left out or had to be written twice.


    # Options for selection or input parameters

    #selectbox to indicate how sunny the place is
    sun_requirement = st.selectbox("☀️ How sunny is your place?", ("Any", "Full Sun", "Partial Sun"))

    #this dictionary is used to link user-friendly categories with concrete distance specifications and quickly access the numeric values that correspond to each description
    spacing_list = {'Any': 200, 'A lot (between 60 and 200cm)': 200, 'Some space (max. 60cm)': 60, 'A little bit (max. 30cm)': 30}
    #selectbox to indicate how much space is available. The selection consists of the dictionary 'spacing_list'.
    spacing_avail = st.selectbox('📐 How much space do you have?', list(spacing_list.keys()))
    #this line translates the entered value into an exact numerical value and is assigned to the 'spacing_value' variable
    spacing_value = spacing_list[spacing_avail]
    # small spread 0-30cm / medium spread 31-60cm / large spread 60cm and more 

   
    #this dictionary is used to link user-friendly categories with concrete time specifications and quickly access the numeric values that correspond to each description
    time_list = {'Any': 300, 'I have time (up to a year)': 300, 'About a semester (4 months)': 120, 'Not much (2 months)': 60}
    #selectbox to indicate how long you want to wait. The selection consists of the dictionary 'time_list'.
    gdd_avail = st.selectbox('⏳ How long do you want to wait?', list(time_list.keys()))
    #this line translates the entered value into an exact numerical value and is assigned to the 'ggd_avail_value' variable
    gdd_avail_value = time_list[gdd_avail]
    # short harvest time 0-60days / medium 61-120 days / long 120+ days

    st.write("The following vegetables and/or herbs meet your requirements...")

    #Button that triggers API request

    if st.button("Search"):
        base_url = "https://openfarm.cc/api/v1/crops"
        try:
            response = requests.get(f"{base_url}?filter={crop_name}")  # App sends a request to the API with a predefined list of vegetables
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']:
                    for crop in data['data']:
                        attributes = crop['attributes']
                        if crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value): # checking if user preferences are met
                            display_crop_details(attributes) # show the recommended vegetables
                else:
                    st.write("No crops match your specifications.")
            else:
                st.write(f"API request failed with status: {response.status_code}")
        except Exception as e:
            #st.write(f"Error: {e}")
            st.write("...")

# Filtering based on selected user input            
def crop_matches_criteria(attributes, sun_requirement, spacing_value, gdd_avail_value):
    """
    This function filters the herbs based on the user input so that all prefernces are met.

    """
    crop_sun_req = (attributes.get('sun_requirements') or '').lower()
    crop_spacing = attributes.get('spread')
    growing_deg_days = attributes.get('growing_degree_days')

    return (
        (sun_requirement == "Any" or sun_requirement.lower() in crop_sun_req) and
        spacing_value >= int(crop_spacing) and
        gdd_avail_value >= int(growing_deg_days)
    )


# Data Visualtization: horizontal bar chart for vegetables (supported by: ChatGPT)
def display_bar_chart_vegetable(attributes):
    """
    This function visualizes the spread in a bar chart.

    """
    # Default average spread for all plants
    average_spread_vegetable = 35
    # Actual spread for the plant (fetch from attributes)
    plant_spread_vegetable = attributes.get('spread', average_spread_vegetable)  # Default to average if not provided

    #Definition plant_name for the label
    plant_name_vegetable = attributes.get('name')

    # Horizontal bar chart
    plt.figure(figsize=(6, 1))
    
    # Modify y-values to increase space between bars
    y_values = [1, 1.4]  # Further spacing between bars
    x_values = [average_spread_vegetable, plant_spread_vegetable]
    
    # barh is used if you want the bar to be horizontal not vertical
    # Adjust bar height for thinner bars
    plt.barh(y_values, x_values, color=['grey', 'green'], height=0.3, tick_label=["Average", plant_name_vegetable])
    
    # Adjust font size for title and labels
    plt.xlabel("Spread (cm)", fontsize=7)
    plt.title(f"Spread Comparison for {attributes.get('name', 'Unknown Plant')}", fontsize=9)
    
    # Adjust y-ticks and make the text smaller
    plt.yticks([1, 1.4], labels=["Average", plant_name_vegetable], fontsize=7)

    plt.tick_params(axis='x', labelsize=6)  # Change font size of the x-axis numbers
    
    # Display the plot
    st.pyplot(plt)

# Display recommended crops and their details
def display_crop_details(attributes):
    """ 
    This function is needed to display chosen attributes of the plants.
    It also contains/calls the bar_chart function.

    """
    st.subheader(f"__{attributes.get('name')}__")
    #st.write(f"**Binomial Name:** {attributes.get('binomial_name')}")
    st.write(f"**Description:** {attributes.get('description')}")
    # st.write(f"**Sun Requirements:** {attributes.get('sun_requirements')}")
    st.write(f"**Sowing Method:** {attributes.get('sowing_method')}")
    #st.write(f"**Spread:** {attributes.get('spread')}")
    #st.write(f"**Row Spacing:** {attributes.get('row_spacing')}")
    #st.write(f"**Height:** {attributes.get('height')}")
    # st.write(f"**Growing Degree Days:** {attributes.get('growing_degree_days')}")
    st.write(f"**Tags:** {attributes.get('tags_array')}")

    # Call the bar chart display function
    display_bar_chart_vegetable(attributes)

    st.write("---")


# MACHINE LEARNING 

def fetch_plant_data():
    """
    Fetch plant data for specific crops one by one from OpenFarm API.
    """
    crop_names = [
        "Sorrel", "Parsley", "Thyme", "Italian Oregano", "Basil", "Cilantro", "Sage", "Chives",
        "Fernleaf Dill", "Chamomile", "Bay Laurel", "Tarragon", "Cress", "Lovage", "Peppermint",
        "Carrot", "Potato", "Onion", "Lettuce", "Tomato", "Zucchini", "Spinach", "Radish",
        "Kale", "Broccoli", "Cauliflower", "Peas", "Green Beans", "Leek", "Swiss Chard", 
        "Beetroot", "Brussels Sprouts", "Celery", "Sweet Corn", "Turnip", "Parsnip", 
        "Eggplant", "Cucumber", "Garlic", "Pepper", "Fennel"
    ]
    
    base_url = "https://openfarm.cc/api/v1/crops"
    all_plants = []

    # Iterate through each crop name and fetch data
    for crop in crop_names:
        try:
            response = requests.get(f"{base_url}?filter={crop}")
            if response.status_code == 200:
                data = response.json()
                if "data" in data and data["data"]:
                    for plant in data["data"]:
                        attributes = plant.get("attributes", {})
                        tags = attributes.get("tags_array", [])

                        # Only include plants with 'herb' or 'vegetable' tags
                        if any(tag in ["vegetable", "herb"] for tag in tags):
                            all_plants.append({
                                "plant_name": attributes.get("name", "Unknown"),
                                "sun_requirements": attributes.get("sun_requirements", "unknown"),
                                "spread": attributes.get("spread", "unknown"),
                                "description": attributes.get("description", "No description available")
                            })
        except Exception as e:
            st.error(f"Error fetching data for {crop}: {e}")

    # Convert to DataFrame
    if all_plants:
        return pd.DataFrame(all_plants)
    else:
        st.warning("No valid plant data found. Using fallback data.")
        return pd.DataFrame({
            "plant_name": ["Tomato", "Basil", "Lettuce"],
            "sun_requirements": ["full sun", "partial sun", "partial sun"],
            "spread": [50, 30, 40],
            "description": [
                "A delicious red fruit often mistaken as a vegetable.",
                "A fragrant herb used in Italian cuisine.",
                "A leafy green vegetable."
            ]  })

# Debugging and Validation
def debug_dataframe(df):
    """Debug and validate the DataFrame for potential issues."""
    st.write("Checking the fetched plant data:")
    st.write(df.head())  # Display the first few rows of the DataFrame

    if df.empty:
        st.error("The plant data DataFrame is empty. Ensure the API is working or provide fallback data.")
    else:
        # Validate columns
        missing_columns = [col for col in ["plant_name", "sun_requirements", "spread"] if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns in the DataFrame: {missing_columns}")
        else:
            st.success("Plant data fetched and validated successfully.")


# Initialize ML Model
def initialize_ml_model(df):
    if df.empty:
        st.error("No data available for training.")
        return None, None

    try:
        # Debug and filter invalid data
        st.write("Filtering invalid data from the DataFrame...")
        st.write(f"Original DataFrame shape: {df.shape}")
        
        # Filter entries with "unknown" sunlight requirements or spread
        df = df[df["sun_requirements"] != "unknown"]
        df["spread"] = pd.to_numeric(df["spread"], errors="coerce")  # Convert spread to numeric
        df = df.dropna(subset=["spread"])  # Drop rows with NaN values in spread
        st.write(f"Filtered DataFrame shape: {df.shape}")

        # Encode sunlight requirements
        le_sun = LabelEncoder()
        df["sun_encoded"] = le_sun.fit_transform(df["sun_requirements"])
        st.write("Label encoding for sunlight requirements applied.")
        st.write(df[["sun_requirements", "sun_encoded"]].drop_duplicates())  # Show encoding

        # Prepare features and labels
        X = df[["sun_encoded", "spread"]]
        y = df["plant_name"]

        # Train the model
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)
        st.success("Machine learning model trained successfully.")
        return model, le_sun
    except Exception as e:
        st.error(f"Error initializing the ML model: {e}")
        return None, None


# Analyze Uploaded Images
def analyze_image(image):
    try:
        width, height = image.size
        avg_color = np.array(image).mean(axis=(0, 1))
        brightness = avg_color.mean()
        if brightness > 180:
            light_condition = "full sun"
        elif brightness > 100:
            light_condition = "partial sun"
        else:
            light_condition = "shade"
        space = 150 if width > 1000 else (50 if width > 500 else 20)
        return light_condition, space
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return None, None


# Image-Based ML
def image_based_ml(model, le_sun):
    st.title("Image-Based Plant Recommendation")
    uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            light_condition, space = analyze_image(image)
            st.write(f"Detected Light Condition: {light_condition}")
            st.write(f"Detected Space: {space} cm")
            if model is not None and le_sun is not None:
                if light_condition in le_sun.classes_:
                    light_encoded = le_sun.transform([light_condition])[0]
                    input_data = np.array([[light_encoded, space]])
                    predicted_plant = model.predict(input_data)[0]
                    st.subheader(f"🌱 Recommended Plant: {predicted_plant}")
                else:
                    st.warning("Light condition not recognized.")
            else:
                st.error("Model is not initialized.")
        except Exception as e:
            st.error(f"Error processing image: {e}")


# NAVIGATION (supported by: Streamlit_Project.py - Bookly)
def main():
    """
    This main function of the streamlit application enables a navigation on the web app with different tabs/pages.
    With the sidebar users have the opportunity to choose the different sections 'Home', 'I Know What I Want',
    'Vegetable Recommendations', 'Herb Recommendations' and 'Machine Learning'. 
    The corresponding content is displayed based on the users selection.

    The feature 'st.session_state' is used here which allows the app to remember and preserve data. 
    This enables dynamic interaction without data loss when the page is reloaded.

    """

    # Set HOME as default section 
    if 'section' not in st.session_state:
        st.session_state['section'] = 'Home'

    # Naming and navgiation with sidebar buttons
    if st.sidebar.button('Home 🏡 '):
        st.session_state['section'] = 'Home'
    if st.sidebar.button('I Know What I Want 🔎'):
        st.session_state['section'] = 'I Know What I Want'
    if st.sidebar.button("Vegetable Recommendations 💡"):    
        st.session_state['section'] = 'Vegetable Recommendations'
    if st.sidebar.button("Herb Recommendations 💡"):   
        st.session_state['section'] = 'Herb Recommendations'
    if st.sidebar.button('Machine Learning ⚙️'):
        st.session_state['section'] = 'Machine Learning'

    # Displaying the respective section of the website you are currently in
    # Calling the necessary functions
    if st.session_state['section'] == 'Home':
        Introduction_WebApp()
    elif st.session_state['section'] == 'I Know What I Want':
        search_bar()
    elif st.session_state['section'] == 'Vegetable Recommendations':
        filter_function_vegetable() 
    elif st.session_state['section'] == 'Herb Recommendations':
        filter_function_herb() 
    elif st.session_state['section'] == 'Machine Learning':
        st.title("Coming soon... 🥦🍅🥕")
    
        if st.button("Fetch All Plant Data"):
            st.write("Fetching plant data... Please wait!")
            plants_df = fetch_plant_data()  # Fetch the data
        if not plants_df.empty:
            st.success("Successfully fetched plant data!")
            st.dataframe(plants_df)  # Display the table
            debug_dataframe(plants_df)  # Debug and validate DataFrame

        # Initialize ML Model
        model, le_sun = initialize_ml_model(plants_df)
        if model and le_sun:
            image_based_ml(model, le_sun)  # Allow image-based ML predictions
        else:
            st.error("Model initialization failed.")
    else:
        st.warning("No valid plant data fetched.")

       

   

# Call the main function
main()
