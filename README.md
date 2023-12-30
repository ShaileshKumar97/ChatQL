# ChatQL
ChatQL: Querying Databases Through Conversation with Power of LLMs

This application is combination of techniques in Natuaral Language Processing, for eg. [Retrieval Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401).

## What is RAG
Retrieval-Augmented Generation allows language models to tap into external data sources, such as enterprise document repositories or databases. This ensures that responses are up-to-date and reflect the unique business rules of the specific domain.

## How it Works?
It first takes an input question and retrieves relevant documents to it from an external database with the help of Vector Stores (eg. Milvus, FAISS etc.). Then, it passes those chunks as a context in a prompt to help an LLM generate an augmented answer.

## Steps involved in RAG Pipeline: with application steps
- Loaders to parse external data in different formats: PDFs, websites, Doc files, etc. (in this application: Database Schema).
- Splitters to chunk the raw data into smaller pieces of text
- An embedding model to convert the chunks into vectors (Sentence Transformer)
- A vector database to store the vectors and query them (FAISS, as it takes a small memory to operate compared to milvus which used in enterprise grade apps)
- A prompt to combine the question and the retrieved documents
- An LLM to generate the answer (OpenAI's GPT-3.5-turbo (API key required))
