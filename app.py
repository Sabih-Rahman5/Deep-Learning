import streamlit as st
from ModelManager import GPUModelManager
import os
import fitz  # PyMuPDF- pdf editor and reader

# Streamlit app
st.title("Test App")
manager = GPUModelManager().getInstance()
state = manager.getState()

# knowledgeBase uploader
# knowledgeBase_pdf = st.file_uploader("Upload Knowledge Base", type=["pdf"])
# if knowledgeBase_pdf is not None:
#     save_path = os.path.join("knowledge_base", knowledgeBase_pdf.name)
#     os.makedirs("knowledge_base", exist_ok=True)
    
#     for file_name in os.listdir("knowledge_base"):
#         file_path = os.path.join("knowledge_base", file_name)
#         os.remove(file_path)

#     with open(save_path, "wb") as f:
#         f.write(knowledgeBase_pdf.read())
        
#     manager.knowledge_base = save_path
#     st.success("Knowledge Base updated!")
#     print(save_path)


knowledgeBase_pdf = st.file_uploader("Upload Knowledge Base", type=["pdf"], key="kb_upload")
if knowledgeBase_pdf is not None:
    save_path = os.path.join("knowledge_base", knowledgeBase_pdf.name)
    os.makedirs("knowledge_base", exist_ok=True)
    
    for file_name in os.listdir("knowledge_base"):
        file_path = os.path.join("knowledge_base", file_name)
        os.remove(file_path)

    with open(save_path, "wb") as f:
        f.write(knowledgeBase_pdf.read())
        
    manager.knowledge_base = save_path
    st.success("Knowledge Base updated!")
    
    # --- Editor button ---
    if st.button("📝 Edit Knowledge Base"):
        doc = fitz.open(save_path)
        full_text = "\n\n".join([page.get_text() for page in doc])
        edited_text = st.text_area("Edit Knowledge Base Content", full_text, height=500)
        
        if st.button("💾 Save Edited Knowledge Base"):
            new_doc = fitz.open()
            new_page = new_doc.new_page()
            new_page.insert_text((72, 72), edited_text, fontsize=12)
            new_doc.save(save_path)
            new_doc.close()
            st.success("Knowledge Base PDF updated.")



# assignment uploader
# assignment_pdf = st.file_uploader("Upload Assignemnt", type=["pdf"])
# if assignment_pdf is not None:
#     save_path = os.path.join("assignment", assignment_pdf.name)
#     os.makedirs("assignment", exist_ok=True)
    
#     for file_name in os.listdir("assignment"):
#         file_path = os.path.join("assignment", file_name)
#         os.remove(file_path)
    
#     with open(save_path, "wb") as f:
#         f.write(assignment_pdf.read())
        
#     manager.assignment = save_path
#     st.success("assignment uploaded!")
#     print(save_path)

# assignment uploader
assignment_pdf = st.file_uploader("Upload Assignment", type=["pdf"], key="assign_upload")
if assignment_pdf is not None:
    save_path = os.path.join("assignment", assignment_pdf.name)
    os.makedirs("assignment", exist_ok=True)
    
    for file_name in os.listdir("assignment"):
        file_path = os.path.join("assignment", file_name)
        os.remove(file_path)
    
    with open(save_path, "wb") as f:
        f.write(assignment_pdf.read())
        
    manager.assignment = save_path
    st.success("Assignment uploaded!")
    
    # --- Editor button ---
    if st.button("📝 Edit Assignment"):
        doc = fitz.open(save_path)
        full_text = "\n\n".join([page.get_text() for page in doc])
        edited_text = st.text_area("Edit Assignment Content", full_text, height=500)
        
        if st.button("💾 Save Edited Assignment"):
            new_doc = fitz.open()
            new_page = new_doc.new_page()
            new_page.insert_text((72, 72), edited_text, fontsize=12)
            new_doc.save(save_path)
            new_doc.close()
            st.success("Assignment PDF updated.")





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


def runButtonClick():
    if(manager.getState() == "empty"):
        st.write("No model loaded")
        return
    if(manager.getState() == "loading" or manager.getState() == "unloading"):
        st.write("Please wait for the model to load")
        return
    if(manager.assignment is None):
        st.write("Please upload an assignment")
        return
    
    if(manager.getState() == "loaded"):
        st.write("Running inference...")
        if(manager.runInference()):
            st.write("Inference completed")
            with open("output.pdf", "rb") as f:
                pdf_data = f.read()
                
            st.download_button(
            label="📄 Download PDF",
            data=pdf_data,
            file_name="result.pdf",
            mime="application/pdf"
        )
        else:
            st.write("Inference failed")
        
    
        

def loadButtonClick():
    
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
    loadButtonClick()
    setStatus()
    
if st.button("Run inference"):
    runButtonClick()
    
    
    
    
    
    # streamlit run app.py --server.address 0.0.0.0 --server.port 80