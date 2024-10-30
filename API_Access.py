import requests
import json



#the base url for the OpenFarm API
base_url = "https://openfarm.cc/api/v1/crops"



# Set up parameters for the crop you want to search (e.g., "tomato")
params = {
    #After filter search for a crop
    "filter": "parsley",    
}



# Step 1: Sending a GET request to the API including the Query Parameters
response = requests.get(base_url, params=params)

# Step 2: Check if the request was successful
if response.status_code == 200:
    # Parse JSON response and assign it to data
    data = response.json()

    # Check if there are results
    if data['data']:
        # Select the first result in the response
        crop = data['data'][0]
        attributes = crop['attributes']  # Access the 'attributes' dictionary

        # Extract specific fields
        name = attributes.get('name')
        binomial_name = attributes.get('binomial_name')
        description = attributes.get('description')
        sun_requirements = attributes.get('sun_requirements')
        sowing_method = attributes.get('sowing_method')
        spread = attributes.get('spread')
        row_spacing = attributes.get('row_spacing')
        height = attributes.get('height')
        tags_array = attributes.get('tags_array')

        # For 'companions', which is nested in 'relationships'
        companions_link = crop['relationships']['companions']['links']['related']

        # Print the extracted data
        print(f"Name: {name}")
        print(f"Binomial Name: {binomial_name}")
        print(f"Description: {description}")
        print(f"Sun Requirements: {sun_requirements}")
        print(f"Sowing Method: {sowing_method}")
        print(f"Spread: {spread}")
        print(f"Row Spacing: {row_spacing}")
        print(f"Height: {height}")
        print(f"Tags: {tags_array}")
        print(f"Companions Link: {companions_link}")

        
    else:
        print("No matching crops found.")
else:
    print(f"Request failed with status code: {response.status_code}")