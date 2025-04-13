
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil


load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "../data/anand-obsidian-4-jul"

def get_chunks():
    # Load documents
    loader = DirectoryLoader(DATA_PATH, glob="*.md", recursive=True)
    documents: List[Document] = loader.load()

    # Split documents into chunks
    # https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/
    splitter = RecursiveCharacterTextSplitter(
     chunk_size=100,
     chunk_overlap=20,
     length_function=len,
     is_separator_regex=False,
    )
    chunks: List[Document] = splitter.split_documents(documents)
    print(f"Splited {len(documents)} documents into {len(chunks)} chunks")
    return chunks

if __name__ == "__main__":
    chunks = get_chunks()

    # Print a random chunk and its next chunk
    print(chunks[1])
    print(chunks[2])


