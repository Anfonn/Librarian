import os
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = ""

loader = GoogleDriveLoader (
    folder_id="",
    credentials_path=r"",
    token_path=r"",
    )

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
texts = text_splitter.split_documents(documents)

persist_directory = r""
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory, metadatas=[{"source": str(i)} for i in range(len(texts))]).persist()