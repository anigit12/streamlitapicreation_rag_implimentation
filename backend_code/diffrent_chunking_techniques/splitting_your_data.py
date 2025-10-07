from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter


class SplittingClass:
    def __init__(self,splitter,chunksize,chunkoverlap,data_for_splitting):
        self.splitter=splitter
        self.chunksize=chunksize
        self.chunkoverlap=chunkoverlap
        self.data_for_splitting=data_for_splitting
    def recursive_split(self):
        data_splitter=RecursiveCharacterTextSplitter(chunk_size=self.chunksize,chunk_overlap=self.chunkoverlap,length_function=len)
        page_data=[]
        for page in self.data_for_splitting:
            res=data_splitter.split_text(page.page_content)
            page_data.extend(res)
        return page_data
    def char_basd_split(self):
        data_splitter=CharacterTextSplitter(chunk_size=self.chunksize,chunk_overlap=self.chunkoverlap,length_function=len)
        page_data=[]
        for page in self.data_for_splitting:
            res=data_splitter.split_text(page.page_content)
            page_data.extend(res)
        return page_data
    
    