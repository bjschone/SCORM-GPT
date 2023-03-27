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
    
    sources = os.listdir("scorm/scormcontent")
    st.write(sources)

   

query_str = st.text_input("Input query")
if st.button("submit"):
    message_bot = index.query(query_str)
    st.write(message_bot)


with st.expander("Course Description small"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate small"):
        cdesquery =  index.query("Generate a one-sentence summary description of the course material.")
        st.code(cdesquery)

with st.expander("Course Description medium"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate Medium"):
        cdesquerym =  index.query("Generate a three-sentence summary description of the course material.")
        st.code(cdesquerym)
        
with st.expander("Course Description Large"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate Large"):
        cdesqueryl =  index.query("Generate a five-sentence summary description of the course material.")
        st.code(cdesqueryl)
        
with st.expander("Learning Objectives"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate Objectives"):
        lo =  index.query("Generate Learning Objectives of the course material which Should be a list of 3-5 clear and measurable objectives that describe the information, skills, behaviors, or perspectives that the participants will acquire after reading and completing the course material. The learning objectives should clearly identify the outcomes or actions participants can expect to demonstrate as a result of the educational experience. Each objective should start with a verb, and depending on the complexity of the course material, use the language and levels found in Bloom’s taxonomy.")
        st.code(lo)
        
with st.expander("Marketing Email"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate Marketing-email"):
        me =  index.query("Generate a Marketing email for this course, Write 5 clever subject lines (formatted with bullet points) and an email that could be used to generate excitement and interest in the training course. The email should contain the Course Description (Medium) snippet and the Learning Objectives snippet.")
        st.code(me)

with st.expander("Enrolment Email"):
    # st.selectbox("Size",("Medium","Short","Long"))
    if st.button("Generate Enrollment-email"):
        ee =  index.query("Generate a Enrollment email for this course, Write 5 subject lines (formatted with bullet points) and an email that would be sent to a participant who has signed up for this training course. It should confirm that they are now ready and able to access the course at the following link: http://www.insert_course_link_here.com. The tone of the email should be practical and slightly enthusiastic, and it should describe what the individual will learn in the training course. The email should use the Course Description (Medium) text snippet and include the Learning Objectives snippet")
        st.code(ee)
      


# with st.expander("Learning Objectives"):
#     if st.button("Generate Objectives"):
#         st.write("This feature is still under construction")
        
# with st.expander("Marketing Email"):
#     st.code("This feature is still under construction")

        
# with st.expander("Enrollment Email"):
#     st.code("This feature is still under construction")
    
# with st.expander("Course Description"):
#     st.selectbox("Evaluation questions",("Knowledge Change","Performance Change"))
#     st.code("This feature is still under construction")
        

# # # Set up the Streamlit app
# # st.title('Zip File Uploader')

