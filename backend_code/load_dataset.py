from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import CSVLoader
class LoadYourData:
      @staticmethod
      def text_loader_or_split(text_file_path):
            return TextLoader(text_file_path).load_and_split()
      @staticmethod
      def csv_loader_for_split(csv_file_path):
            return CSVLoader(csv_file_path).load_and_split()
      @staticmethod
      def pdf_loader_for_split(pdf_file_path):
            return PyPDFLoader(pdf_file_path).load_and_split()
      @staticmethod
      def docx_loader_for_split(doc_file_path):
            return Docx2txtLoader(doc_file_path).load_and_split()
            
             







