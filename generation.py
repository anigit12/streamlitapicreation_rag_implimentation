import streamlit as st
from model_class_creation.model import Model
import os 
import io
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from time import sleep
def load_vector_db():
    main_folder_path = r'.\vector_databased'
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
    sub_folder_name=[]
    sub_folder_path =[]
    for _,dirs,_ in os.walk(main_folder_path):
        for dir in dirs:
            sub_folder_name.append(dir)
            sub_folder_path.append(os.path.join(main_folder_path, dir))
    return sub_folder_name,sub_folder_path


st.title("😎Inquiro AI:Your AI-Powered Assistant")

st.subheader("Configuration")
st.subheader('Select Data Base')
data_bases,data_bases_path= load_vector_db()
data_bases.insert(0,'--select--')
data_bases_path.insert(0,'--select--')
data_base = st.selectbox("Data Base Selection:", data_bases, key=1, label_visibility="visible", help="Select the database to use")
if data_base != '--select--':
    selected_index = data_bases.index(data_base)
    selected_path = data_bases_path[selected_index]
    #declare section state variables for seleted database and the respective path
    st.session_state['selected_path'] = selected_path 
    st.session_state['selected_index'] = selected_index
    st.session_state['data_base'] = data_base
    st.success("Data base loaded successfully")
else:
    st.session_state['selected_path'] = None
    st.session_state['selected_index'] = None
    st.session_state['data_base'] = None
    st.info("Please select a data base")
#select model 
st.subheader('Select Large Language Model')
selected_model_options = ['--select--', 'gemini-1.5-flash']
selected_option_model = st.selectbox("Choose Your  Model:", selected_model_options, key=2, label_visibility="visible", help="Select the language model")
if selected_option_model != '--select--':
    st.session_state['selected_model'] = selected_option_model
    if selected_option_model == 'gemini-1.5-flash':
        # Create an instance of the Model class
        st.session_state['model_instance'] = Model.gemini_chat()
        st.success("Model loaded successfully")
else:
    st.session_state['selected_model'] = None
    st.session_state['model_instance'] = None
    st.info("Please select a model")

st.header("🤖 Conversation with Inquiro AI ")

# Button to disconnect and reload the section
if st.button("Disconnect & Reload"):
    st.session_state['messages'] = []

# Button to download the conversation
if st.session_state.get('messages'):
    conversation_text = ""
    for msg in st.session_state['messages']:
        conversation_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
    conversation_bytes = io.BytesIO(conversation_text.encode('utf-8'))
    st.download_button(
        label="Download Conversation",
        data=conversation_bytes,
        file_name="conversation.txt",
        mime="text/plain"
    )

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if input := st.chat_input('Hi I am here to help you'):
    with st.chat_message("user",avatar='🧑'):
        st.markdown(input)
    st.session_state['messages'].append({"role": "user", "content": input})
    #vector database loading 
    embedding_model = Model.gemini_embed()
    inde_db=FAISS.load_local(folder_path=st.session_state['selected_path'], embeddings=embedding_model,index_name='IndianBankOfficer',allow_dangerous_deserialization=True)
    retriver = inde_db.as_retriever(search_kwargs={"k": 1})
    context=retriver.invoke(input=input)
    prompt=PromptTemplate(
        input_variables=["context", "input"],
        template="You are a helpful assistant. Use the following context to answer the question.\n\nContext: {context}\n\nQuestion: {input}\n\nAnswer:"
    )
    chain = prompt | st.session_state['model_instance']
    response = chain.invoke(input={"context": context, "input": input}).content
    with st.chat_message("assistant", avatar='🤖'):
        placeholder = st.empty()
        displayed_text = ""
        for char in response:
            displayed_text += char
            placeholder.markdown(displayed_text)
            sleep(0.02)  # Adjust speed as needed
        placeholder.markdown(displayed_text)
    st.session_state['messages'].append({"role": "assistant", "content": response})

