import streamlit as st
from langchain.document_loaders import PyPDFLoader
from ModelManager import GPUModelManager  # Import function from helper.py

# Streamlit app
st.title("Test App")

knowledgeBase_pdf = st.file_uploader("Upload Knowledge Base", type=["pdf"])
if knowledgeBase_pdf is not None:
    loader = PyPDFLoader(knowledgeBase_pdf)
    doc = loader.load()
    
    st.write("Knowledge Base uploaded!")


assignment_pdf = st.file_uploader("Upload Assignemnt", type=["pdf"])
if assignment_pdf is not None:
    st.write("Assignment uploaded!")




# Dropdown menu for model selection
options = ["None", "Llama-3.2", "Gemma-3", "DeepSeek-r1"]
manager = GPUModelManager().getInstance()
state = manager.getState()

if state == "empty":
    selected_option = st.selectbox("Select LLM:", options)
else:
    selected_option = st.selectbox("Select LLM:", options, index=options.index(manager.getLoadedModel()))

# Function to update status dynamically
def setStatus():
    if manager.getState() == "empty":
        st.write("No model loaded")
    elif manager.getState() == "loading":
        st.write("Loading model...")
    elif manager.getState() == "loaded":
        st.write(manager.getLoadedModel() + " loaded")

# Button to trigger model loading/unloading
if st.button("Load Model"):
    if selected_option == "None":
        st.write("Please select a model")
    else:
        if manager.getState() == "loaded":
            st.write("Unloading model: " + str(manager.getLoadedModel()))
        st.write(f"Loading Model: {selected_option}")
        manager.loadModel(selected_option)

setStatus()
