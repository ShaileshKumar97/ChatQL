# ChatQL 💬

**ChatQL** is an intuitive and user-friendly application that allows users to interact with their SQL database using natural language queries. Type in your questions or requests, and ChatQL will generate the appropriate SQL query and return the data you need. No more complex SQL queries or digging through tables - ChatQL makes it easy to access your data! By bringing data one step closer, ChatQL empowers users to make data-driven decisions faster and more efficiently, reducing the barriers between users and the insights they seek.

## 🌟 Features

- Interactive and user-friendly interface
- Integration with Snowflake Data Warehouse
- Utilizes OpenAI's GPT-4 and text-embedding-ada-002
- Uses In-memory Vector Database FAISS for storing and searching through vectors

## 🛠️ Installation

1. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

2. Set up your `OPENAI_API_KEY`, Snowflake `ACCOUNT`, `USER_NAME`, `PASSWORD`, `ROLE`, `DATABASE`, `SCHEMA` and `WAREHOUSE` in project directory `secrets.toml`. If you don't have access to GPT-4 change the script in chain.py replace gpt-4 in model_name to gpt-3.5-turbo

3. Make you're schema.md that matches you're database.

4. Run `python /embeddings/faiss.py` to get convert to embeddings and store as an index file.

5. Run the Streamlit app to start chatting:
   streamlit run app.py

## 📚 Usage

1. Launch the app by visiting the URL provided by Streamlit.
2. Type your query in natural language or SQL format in the input box.
3. Press "Submit" to generate the response.
4. The chatbot will generate a response based on your query and display the result, including any relevant data or SQL code.
