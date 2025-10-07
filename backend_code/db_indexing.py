from langchain_community.vectorstores import FAISS
class DataBaseCreation:
    def __init__(self,embedding_model,texts,file_name):
        self.embedding=embedding_model
        self.texts=texts
        self.file_name=file_name
    def fiass_db_creation(self):
        index_db = FAISS.from_texts(texts=self.texts, embedding=self.embedding)
        filename=str(self.file_name).split('.')[0]
        filename=filename.replace('_','').replace('-','').replace(' ','')
        index_db.save_local(folder_path=f'.\\vector_databased\\index{filename}',index_name=filename)
        




