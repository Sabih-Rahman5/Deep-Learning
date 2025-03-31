import streamlit as st
from ModelManager import GPUModelManager
import os

# Streamlit app
st.title("Test App")
manager = GPUModelManager().getInstance()
state = manager.getState()

knowledgeBase_pdf = st.file_uploader("Upload Knowledge Base", type=["pdf"])


if knowledgeBase_pdf is not None:
    save_path = os.path.join("knowledge_base", knowledgeBase_pdf.name)
    os.makedirs("knowledge_base", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(knowledgeBase_pdf.read())
        
    manager.knowledge_base = save_path
    st.success("Knowledge Base uploaded!")
    print(save_path)

assignment_pdf = st.file_uploader("Upload Assignemnt", type=["pdf"])
if assignment_pdf is not None:
    st.write("Assignment uploaded!")


# Dropdown menu for model selection
options = ["None", "Llama-3.2", "Gemma-3", "DeepSeek-r1"]


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
