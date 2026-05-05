from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_and_split_pdfs(folder_path):
    all_docs = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)

            loader = PyPDFLoader(path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )

            split_docs = splitter.split_documents(docs)
            all_docs.extend(split_docs)

    return all_docs