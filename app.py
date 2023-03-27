import streamlit as st
import zipfile
import os
# import streamlit as st
import openai 
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader,PromptHelper,QuestionAnswerPrompt
import os 
from streamlit_chat import message as st_message

# favicon = "favicon.ac8d93a.69085235180674d80d902fdc4b848d0b.png"
# st.set_page_config(page_title="Flipick Chat", page_icon=favicon)

openai.api_key = os.getenv("API_KEY")


# Define the function to extract the zip file and save the contents to a directory
def extract_zipfile(zip_file, save_directory):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(save_directory)

             
        
# Create a file uploader component for the zip file
zip_file = st.file_uploader('Upload a zip file', type='zip')

# If the user uploads a file, extract its contents and save them to a directory
if zip_file is not None:
    # Create a directory for the extracted files
    save_directory = 'scorm'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Call the extract_zipfile function to extract the zip file and save the contents to the directory
    extract_zipfile(zip_file, save_directory)
    
    # Display a success message
    st.success('Zip file extracted and saved to directory: {}'.format(save_directory))
    documents = SimpleDirectoryReader('scorm/scormcontent').load_data()
    index = GPTSimpleVectorIndex(documents)
    index.save_to_disk('indx.json')
    st.success('index created successfully')

# try:
#     index = GPTSimpleVectorIndex.load_from_disk('indx.json')
# except FileNotFoundError:
#     # Loading from a directory
    
    sources = os.listdir("scorm")
    st.write(sources)

   

query_str = st.text_input("Input query")
if st.button("submit"):
    message_bot = index.query(query_str)
    st.write(message_bot)
    with st.expander("Course Description"):
        st.selectbox("Size",("Medium","Short","Long"))
        if st.button("Generate"):
            st.write("This feature is still under construction")
            
    with st.expander("Learning Objectives"):
        if st.button("Query"):
            st.write("This feature is still under construction")
            
    with st.expander("Marketing Email"):
        st.code("This feature is still under construction")

            
    with st.expander("Enrollment Email"):
        st.code("This feature is still under construction")
        
    with st.expander("Course Description"):
        st.selectbox("Evaluation questions",("Knowledge Change","Performance Change"))
        st.code("This feature is still under construction")
        

# # Set up the Streamlit app
# st.title('Zip File Uploader')

