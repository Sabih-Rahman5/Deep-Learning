import streamlit as st
import json
import os

st.title("Test App")

# File to store the selected item
PERSISTENCE_FILE = "selected_item.json"

# Initializer function
def initialize_app():
    print("starting App")

# Function to load the last selected item
def load_last_selected():
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, "r") as file:
            return json.load(file).get("selected", "Select an item")
    return "Select an item"

# Function to save the selected item
def save_selected(item):
    with open(PERSISTENCE_FILE, "w") as file:
        json.dump({"selected": item}, file)

# Initialize app
initialize_app()

# Load the last selected item
if "selected_item" not in st.session_state:
    st.session_state.selected_item = load_last_selected()

# Dropdown menu
options = ["Select an item", "LLama 3.2", "DeepSeek-r1", "Gemma"]
selected_item = st.selectbox("Choose an item:", options, index=options.index(st.session_state.selected_item))

# Function to execute upon selection
def execute_function(item):
    if item != "Select an item":
        st.write(f"You selected: {item}")
        st.session_state.selected_item = item
        save_selected(item)  # Persist the selection

# Execute function when an item is selected
execute_function(selected_item)



# streamlit run app.py --server.address 0.0.0.0 --server.port 80