import streamlit as st

# Title of the app
st.title("Dropdown Menu Example")

# Dropdown menu
options = ["Select an item", "LLama 3.2", "DeepSeek-r1", "Gemma", "Date"]
selected_item = st.selectbox("Choose an item:", options)

# Function to execute upon selection
def execute_function(item):
    if item != "Select an item":    
        st.write(f"You selected: {item}")

# Execute function when an item is selected
if selected_item:
    execute_function(selected_item)
