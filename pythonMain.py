import streamlit as st
import langchain_helper

st.title("Restaurant Name Generator")

# Sidebar to pick a cuisine
cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

if cuisine:
    # Fetch restaurant data
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    
    # Display the restaurant name
    st.header(response['restaurant_name'])
    
    # Split menu items into a list
    menu_items = response['menu_items'].split(",")
    
    # Display menu items
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-", item.strip())
        
   
    