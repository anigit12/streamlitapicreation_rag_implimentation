import streamlit as st
import os
from backend_code.load_dataset import LoadYourData
from backend_code.diffrent_chunking_techniques.splitting_your_data import SplittingClass
from backend_code.db_indexing import DataBaseCreation
from model_class_creation.model import Model

class KnowledgeDBCreator:
    def __init__(self):
        self.UPLOAD_FOLDER = r"D:\streamlitapicreation_rag_implimentation\data_upload"
        self.FILE_NAME = None
        self.split_pages = []
        self.selected_option_embedding = None
        self.selected_option_splitting = None
        self.chunk_size = 1000
        self.chunk_overlap = 100
        self.setup_upload_folder()

    def setup_upload_folder(self):
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)

    def render_ui(self):
        st.title('Create Your KnowledgeDB')
        self.upload_file_section()
        self.embedding_model_section()
        self.splitting_technique_section()
        self.chunk_settings_section()
        self.generate_db_button()

    def upload_file_section(self):
        st.header('Choose a File from Your Local Device', divider='red')
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file:
            self.FILE_NAME = uploaded_file.name
            save_path = os.path.join(self.UPLOAD_FOLDER, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            self.split_pages = self.load_file(save_path)
            st.success(f"File saved to {save_path}")

    def load_file(self, file_path):
        if file_path.lower().endswith('.pdf'):
            return LoadYourData.pdf_loader_for_split(pdf_file_path=file_path)
        elif file_path.lower().endswith('.txt'):
            return LoadYourData.text_loader_or_split(text_file_path=file_path)
        elif file_path.lower().endswith('.docx'):
            return LoadYourData.docx_loader_for_split(doc_file_path=file_path)
        elif file_path.lower().endswith('.csv'):
            return LoadYourData.csv_loader_for_split(csv_file_path=file_path)
        return []

    def embedding_model_section(self):
        st.header('Select Embedding Model', divider='blue')
        embedding_model_options = ['--select--', 'text-embedding-004']
        self.selected_option_embedding = st.selectbox("Choose an Embedding model:", embedding_model_options, key=1)

    def splitting_technique_section(self):
        st.header('Select Splitting Technique', divider='red')
        splitting_options = ['--select--', 'RecursiveCharecterSpliter', 'CharecterSpliter']
        self.selected_option_splitting = st.selectbox("Choose a Splitting Technique:", splitting_options, key=2)

    def chunk_settings_section(self):
        st.header('Set Chunk Size and Chunk Overlap', divider='green')
        self.chunk_size = st.slider("Select a value for Chunk Size", min_value=0, max_value=7000, value=1000, step=1)
        self.chunk_overlap = st.slider("Select a value for Chunk Overlap", min_value=0, max_value=500, value=100, step=1)

    def generate_db_button(self):
        st.header('Press Me to Generate a Knowledge DB👇', divider='orange')
        if st.button('Hey 🖐️I am here please press me', key=3, type='primary'):
            self.generate_knowledge_db()

    def generate_knowledge_db(self):
        if self.selected_option_splitting == 'RecursiveCharecterSpliter':
            reccharsplit = SplittingClass(
                splitter=self.selected_option_splitting,
                chunksize=self.chunk_size,
                chunkoverlap=self.chunk_overlap,
                data_for_splitting=self.split_pages
            )
            splitted_data_list = reccharsplit.recursive_split()
            self.create_database(splitted_data_list)
        elif self.selected_option_splitting == 'CharecterSpliter':
            charsplit = SplittingClass(
                splitter=self.selected_option_splitting,
                chunksize=self.chunk_size,
                chunkoverlap=self.chunk_overlap,
                data_for_splitting=self.split_pages
            )
            splitted_data_list = charsplit.char_basd_split()
            self.create_database(splitted_data_list)
        else:
            st.warning('Please Select Splitting technique')

    def create_database(self, splitted_data_list):
        if self.selected_option_embedding == 'text-embedding-004':
            data_base_creation = DataBaseCreation(
                embedding_model=Model.gemini_embed(),
                texts=splitted_data_list,
                file_name=self.FILE_NAME
            )
            data_base_creation.fiass_db_creation()


if __name__ == "__main__":
    app = KnowledgeDBCreator()
    app.render_ui()
