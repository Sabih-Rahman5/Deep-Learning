import streamlit as st
from ModelManager import GPUModelManager  # Import function from helper.py

# Streamlit app
st.title("Test App")

# Dropdown menu
options = ["Select Model", "Llama-3.2", "Gemma-3", "DeepSeek-r1"]
selected_option = st.selectbox("Select an option:", options)


def setStatus():
    manager = GPUModelManager().getInstance()
    if(manager.getState() == "empty"):
        st.write("No model loaded")
    elif(manager.getState() == "loading"):
        st.write("Loading model...")
    elif(manager.getState() == "loaded"):
        st.write(manager.getLoadedModel() + " loaded")

# Button to trigger function
if st.button("Run"):
    manager = GPUModelManager().getInstance()
    manager.loadModel(selected_option)  
    
    st.write(f"You selected: {selected_option}")

# streamlit run app.py --server.address 0.0.0.0 --server.port 80