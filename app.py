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
    save_path = os.path.join("assignment", assignment_pdf.name)
    os.makedirs("assignment", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(assignment_pdf.read())
        
    manager.assignment = save_path
    st.success("Knowledge Base uploaded!")
    print(save_path)


# Dropdown menu for model selection
options = ["None", "Llama-3.2", "Gemma-3", "DeepSeek-r1"]
selected_option = st.selectbox("Select LLM:", options)

    


# Function to update status dynamically
def setStatus():
    st.empty()
    if manager.getState() == "empty":
        st.write("No model loaded")
    elif manager.getState() == "loading":
        st.write("Loading model...")
    elif manager.getState() == "loaded":
        st.write(manager.getLoadedModel() + " loaded")


def buttonClick():
    
    if(selected_option == "None"):
        st.write("Please select a model")
        return

    if(selected_option == "loading" or selected_option == "unloading"):
        st.write("Please wait for the model to load/unload")
        return

    if manager.getState() == "loaded":
        print("Button clicked")
        if selected_option == manager.getLoadedModel():
            st.write("Model already loaded")
            return
        else:
            st.write("Unloading model: " + str(manager.getLoadedModel()))
            manager.clearGpu()
          
    manager.loadModel(selected_option)


# Button to trigger model loading/unloading
if st.button("Load Model"):
    buttonClick()
    setStatus()