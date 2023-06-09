import os
from dotenv import load_dotenv
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

loader = GoogleDriveLoader (
    folder_id=os.getenv('GOOGLE_FOLDER_ID'),
    credentials_path=os.getenv('GOOGLE_CREDENTIALS.JSON_PATH'),
    token_path=os.getenv('GOOGLE_TOKEN.JSON_PATH'),
    )

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
texts = text_splitter.split_documents(documents)

persist_directory = os.getenv('CHROMA_PERSIST_PATH')
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory, metadatas=[{"source": str(i)} for i in range(len(texts))]).persist()