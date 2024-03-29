import streamlit as st
import json
import requests

# Fetch JSON data from URL
url = 'https://raw.githubusercontent.com/pratyusa98/impact-fact/main/output.json'
response = requests.get(url)
if response.status_code == 200:
    json_data = json.loads(response.text)
else:
    print(f"Failed to fetch JSON data from {url}")
    json_data = None

# Use json_data as needed


# # Load JSON data from file
# with open('https://raw.githubusercontent.com/pratyusa98/impact-fact/main/output.json', 'r') as file:
#     json_data = json.load(file)

def get_impact_factor_by_partial_name(partial_name, data):
    matching_journals = []
    partial_name = partial_name.lower()  # Convert to lowercase for case-insensitive matching
    for entry in data:
        if partial_name in entry['Journal name'].lower():
            matching_journals.append((entry['Journal name'], entry['2022 JIF']))
    
    # Sort the matching journals by impact factor in descending order
    matching_journals.sort(key=lambda x: x[1], reverse=True)
    return matching_journals

# Streamlit UI
st.title("Journal Impact Factor Search")

# Input field for partial journal name
partial_name = st.text_input("Enter partial journal name:", "")

# Button to trigger search
if st.button("Search"):
    if partial_name:
        matching_journals = get_impact_factor_by_partial_name(partial_name, json_data)
        if matching_journals:
            st.write("Matching Journals (sorted by impact factor, descending):")
            # Render results with vertical scrollbar
            # Render results with vertical scrollbar and line breaks
            st.markdown(
                "<div style='height: 300px; overflow-y: scroll;'>"
                + "<br>".join([f"- {journal}: {impact_factor}" for journal, impact_factor in matching_journals])
                + "</div>", 
                unsafe_allow_html=True
            )

        else:
            st.write(f"No journals found matching the partial name '{partial_name}'")
    else:
        st.write("Please enter a partial journal name.")
