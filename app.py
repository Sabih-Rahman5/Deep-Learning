import streamlit as st
from ModelManager import GPUModelManager
import os
import fitz  # PyMuPDF- pdf editor and reader

from PyPDF2 import PdfReader


# Streamlit app
st.set_page_config(page_title="Grader App", page_icon="assets/personal.png")
st.title("Grader App")

manager = GPUModelManager().getInstance()
state = manager.getState()




# --- Initialize session state flags ---
# if "edit_assignment_mode" not in st.session_state:
#     st.session_state.edit_assignment_mode = False

# if "edited_assignment_text" not in st.session_state:
#     st.session_state.edited_assignment_text = ""

# if "uploaded_assignment" not in st.session_state:
#     st.session_state.uploaded_assignment = None

    
    

# knowledgeBase uploader
knowledgeBase_pdf = st.file_uploader("Upload Knowledge Base", type=["pdf"])
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
    #print(save_path)




# assignment uploader
# if(st.session_state.edited_assignment_text == ""):
#     assignment_pdf = st.file_uploader("Upload Assignment", type=["pdf"], key="assign_upload")
# else:
#     print("returned")
#     assignment_pdf = None


# if assignment_pdf is not None:
#     save_path = os.path.join("assignment", assignment_pdf.name)
#     print ("Saving assignment to:", save_path)
#     # Clear previous files
#     if not os.path.exists("assignment"):
#         os.makedirs("assignment")
    
#     for file_name in os.listdir("assignment"):
#         file_path = os.path.join("assignment", file_name)
#         os.remove(file_path)

#     # Save uploaded PDF
#     with open(save_path, "wb") as f:
#         f.write(assignment_pdf.read())

#     manager.assignment = save_path
#     st.success("Assignment uploaded!")

#     # Show Edit button
#     if st.button("📝 Edit Assignment"):
#         print("Edit button clicked")
#         # Extract text once and store it in session state
#         doc = fitz.open(save_path)
#         full_text = "\n\n".join([page.get_text() for page in doc])
#         doc.close()

#         st.session_state.edited_assignment_text = full_text
#         st.session_state.edit_assignment_mode = True
#         st.session_state.uploaded_assignment = assignment_pdf

# # --- PDF Text Editor Interface ---
# if st.session_state.edit_assignment_mode:
#     st.subheader("📄 PDF Text Editor")
#     edited_text = st.text_area("Edit Assignment Content", st.session_state.edited_assignment_text, height=500)

#     # Save edited version
#     if st.button("💾 Save Edited Assignment"):
#         new_doc = fitz.open()
#         lines = edited_text.split('\n')
#         page = new_doc.new_page()
#         y = 72  # Starting Y position

#         for line in lines:
#             page.insert_text((72, y), line, fontsize=12)
#             y += 15
#             if y > 800:
#                 page = new_doc.new_page()
#                 y = 72

#         new_doc.save(manager.assignment)  # Overwrite original
#         new_doc.close()
#         assignment_pdf = new_doc

#         st.success(f"✅ Assignment PDF updated and saved to: {manager.assignment}")
#         st.session_state.edit_assignment_mode = False  # Exit editor

#     # Optional: Cancel editing
#     if st.button("❌ Cancel Editing"):
#         st.session_state.edit_assignment_mode = False
#         st.info("Editing canceled.")



# # Dropdown menu for model selection
# options = ["None", "Llama-3.2", "Gemma-3", "DeepSeek-r1"]
# selected_option = st.selectbox("Select LLM:", options)

    
# # Function to update status dynamically
# def setStatus():
#     st.empty()
#     if manager.getState() == "empty":
#         st.write("No model loaded")
#     elif manager.getState() == "loading":
#         st.write("Loading model...")
#     elif manager.getState() == "loaded":
#         st.write(manager.getLoadedModel() + " loaded")


# def runButtonClick():
#     if(manager.getState() == "empty"):
#         st.write("No model loaded")
#         return
#     if(manager.getState() == "loading" or manager.getState() == "unloading"):
#         st.write("Please wait for the model to load")
#         return
#     if(manager.assignment is None):
#         st.write("Please upload an assignment")
#         return
    
#     if(manager.getState() == "loaded"):
#         st.write("Running inference...")
        
#         progress_bar = st.progress(0)
        
#         def update_progress(fraction):
#             progress_bar.progress(fraction)
            
#         if(manager.runInference(progress_callback=update_progress)):
#             progress_bar.empty()  # Remove progress bar
#             st.write("✅ Inference completed")
            
#             with open("output.pdf", "rb") as f:
#                 pdf_data = f.read()
            
#             print("PDF data loaded successfully")
#             st.download_button(
#             label="📄 Download PDF",
#             data=pdf_data,
#             file_name="result.pdf",
#             mime="application/pdf"
#             )
#         else:
#             st.write("Inference failed")
        
    
        

# def loadButtonClick():
    
#     if(selected_option == "None"):
#         st.write("Please select a model")
#         return

#     if(selected_option == "loading" or selected_option == "unloading"):
#         st.write("Please wait for the model to load/unload")
#         return

#     if manager.getState() == "loaded":
#         print("Button clicked")
#         if selected_option == manager.getLoadedModel():
#             st.write("Model already loaded")
#             return
#         else:
#             st.write("Unloading model: " + str(manager.getLoadedModel()))
#             manager.clearGpu()
#     manager.loadModel(selected_option)


# # Button to trigger model loading/unloading
# if st.button("Load Model"):
#     loadButtonClick()
#     setStatus()
    
# if st.button("Run inference"):
#     if not st.session_state.uploaded_assignment:
#         st.error("Please upload an assignment first")
#     else:
#         manager.runInference()
    
    
    
    
    
    # streamli  t run app.py --server.address 0.0.0.0 --server.port 80