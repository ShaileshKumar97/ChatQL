import os

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from utils.snowflake import query_table_schema


def create_embeddings_with_schema(cursor, database_name: str):

    query_table_schema(cursor, database_name, f"{database_name}_schema.md")

    loader = UnstructuredMarkdownLoader(f"{database_name}_schema.md")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_documents(data)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    docsearch = FAISS.from_documents(texts, embeddings)

    docsearch.save_local(f"faiss_index_{database_name}")
