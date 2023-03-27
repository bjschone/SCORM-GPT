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
    st.success('Zip file extracted Successfuly',icon="✅")
    documents = SimpleDirectoryReader('scorm/scormcontent').load_data()
    index = GPTSimpleVectorIndex(documents)
    index.save_to_disk('indx.json')
    st.success('index created successfully',icon="✅")

    
    # sources = os.listdir("scorm/scormcontent")
    # st.write(sources)

   

col1, col2 = st.columns(2)

try:
    with col1.expander("Course Description small"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate small"):
        cdesquery =  index.query("Generate a one-sentence summary , of the course Description.")
        if 'cdesquery' not in st.session_state:
            st.session_state['cdesquery'] = cdesquery
        st.code(st.session_state['cdesquery'], language=None)

    with col1.expander("Course Description medium"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Medium"):
        cdesquerym =  index.query("Generate a three-sentence summary , of the course Description.")
        if 'cdesquerym' not in st.session_state:
            st.session_state['cdesquerym'] = cdesquerym
        st.code(st.session_state['cdesquerym'], language=None)
        
    with col1.expander("Course Description Large"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Large"):
        cdesqueryl =  index.query("Generate a five-sentence summary , of the course Description.")
        if 'cdesqueryl' not in st.session_state:
            st.session_state['cdesqueryl'] = cdesqueryl
        st.code(st.session_state['cdesqueryl'], language=None)
        
    with col1.expander("Learning Objectives"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Objectives"):
        lo =  index.query("Generate Learning Objectives which Should be a list of 3-5 clear and measurable objectives, The learning objectives should clearly identify the outcomes or actions participants can expect to demonstrate as a result of the educational experience. Each objective should start with a verb, and depending on the complexity of the course material, use the language and levels found in Bloom’s taxonomy.")
        if 'lo' not in st.session_state:
            st.session_state['lo'] = lo
        st.code(st.session_state['lo'], language=None)
        
    with col1.expander("Marketing Email"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Marketing-email"):
        me =  index.query("Generate a Marketing email for this course, Write 5 clever subject lines (formatted with bullet points) and an email that could be used to generate excitement and interest in the training course. The email should contain the Course Description (Medium) snippet and the Learning Objectives snippet.")
        if 'me' not in st.session_state:
            st.session_state['me'] = me
        st.code(st.session_state['me'], language=None)

    with col1.expander("Enrolment Email"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Enrollment-email"):
        ee =  index.query("Generate a Enrollment email for this course, Write 5 subject lines (formatted with bullet points) and an email that would be sent to a participant who has signed up for this training course. It should confirm that they are now ready and able to access the course at the following link: http://www.insert_course_link_here.com. The tone of the email should be practical and slightly enthusiastic, and it should describe what the individual will learn in the training course. The email should use the Course Description (Medium) text snippet and include the Learning Objectives snippet")
        if 'ee' not in st.session_state:
            st.session_state['ee'] = ee
        st.code(st.session_state['ee'], language=None)
    
    with col1.expander("Completion Email"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Completion-email"):
        cc =  index.query("Generate a Completion email for this course,Write 5 subject lines (formatted with bullet points) and an email that would be sent to a participant who has completed this training course. It should confirm that they have finished the experience and it describe what they learned")
        if 'cc' not in st.session_state:
            st.session_state['cc'] = cc
        st.code(st.session_state['cc'], language=None)
    
    with col1.expander("Evaluation Questions (Knowledge Change)"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Evaluation Questions-kc"):
        eq =  index.query("Generate 5-10 quiz questions to evaluate if a participant gained the knowledge and skills outlined in the " + str(st.session_state['lo']) )
        if 'eq' not in st.session_state:
            st.session_state['eq'] = eq
        st.code(st.session_state['eq'], language=None)
    
    with col1.expander("Evaluation Questions (Performance Change)"):
        # st.selectbox("Size",("Medium","Short","Long"))
        # if st.button("Generate Evaluation Questions-pc"):
        pc =  index.query("Generate a Evaluation Questions for this course, Write 5-10 quiz questions to evaluate if a participant’s behavior or performance related to the course material may have changed  in their day to day activities (i.e., have they changed how they do their job, as it relates to the course material and the Learning Objectives).")
        if 'pc' not in st.session_state:
            st.session_state['pc'] = pc
        st.code(st.session_state['pc'], language=None)
    
    with col2.expander("Copy everything together"):
        try:
            string = "Course Description Large\n" + str(st.session_state['cdesqueryl']) + "\n\n\n" + "Course Description Medium\n" + str(st.session_state['cdesquerym']) + "\n\n\n" + "Course Description small\n" + str(st.session_state['cdesquery']) + "\n\n\n"+ "Learning Objectives\n"  + str(st.session_state['lo']) + "\n\n\n" + "Marketing email\n" + str(st.session_state['me']) + "\n\n\n" + "Enrollment Email\n" + str(st.session_state['ee']) +  "Completion email\n" + str(st.session_state['cc']) + "\n\n\n"+  "Evaluation Questions (Knowledge Change)\n" + str(st.session_state['eq']) + "\n\n\n"+  "Evaluation Questions (Performance Change)\n" + str(st.session_state['pc']) 
            st.code(string, language=None)
            st.session_state.clear()
        except KeyError:
            st.warning("Some of the Contents are not generated competley, Click All Buttons before collapsing this")

except NameError:
    st.warning("Please Upload a Zip File Before Generating anything",icon="⚠️")
