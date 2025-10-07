import streamlit as st

class StreamlitApp:
    def __init__(self):
        self.pages = []

    def add_page(self, file_path, title, icon):
        page = st.Page(file_path, title=title, icon=icon)
        self.pages.append(page)

    def run(self):
        st.sidebar.title("🤖 Inquiro AI")
        pg = st.navigation(self.pages)
        pg.run()

if __name__ == "__main__":
    app = StreamlitApp()
    
    app.add_page(r'D:\streamlitapicreation_rag_implimentation\home_page.py', 'Home Page', '🏠')
    app.add_page(r'D:\streamlitapicreation_rag_implimentation\vector_db_creation.py', 'Embedding Creation', '📦')
    app.add_page(r'D:\streamlitapicreation_rag_implimentation\generation.py', 'Generate Output', '🔄')
    app.run()
