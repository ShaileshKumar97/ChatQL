# ChatQL 💬

**ChatQL** is an intuitive and user-friendly application that allows users to interact with their SQL database using natural language queries. Type in your questions or requests, and ChatQL will generate the appropriate SQL query and return the data you need. No more complex SQL queries or digging through tables - ChatQL makes it easy to access your data! By bringing data one step closer, ChatQL empowers users to make data-driven decisions faster and more efficiently, reducing the barriers between users and the insights they seek.

## 🌟 Features

- Interactive and user-friendly interface
- Integration with PostgreSQL and Snowflake Data Warehouse
- Utilizes OpenAI's GPT-4 and text-embedding-ada-002
- Uses In-memory Vector Database FAISS for storing and searching through vectors

## 🛠️ Installation

1. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
2. Run the Streamlit app to start chatting:
   ```
   streamlit run app.py
   ```
3. Select your database from dropdown and enter required credentials like Set up your `OPENAI_API_KEY`, PostgreSQL's `HOST`, `PORT`, `DATABASE`, `USERNAME`, `PASSWORD` and `SCHEMA` or Snowflake's `ACCOUNT`, `USER_NAME`, `PASSWORD`, `ROLE`, `DATABASE`, `SCHEMA` and `WAREHOUSE`. If you don't have access to GPT-4 change the script in chain.py replace gpt-4 in model_name to gpt-3.5-turbo.
4. And submit, It will now generate the schema of tables from database and store into a md file.
5. Now chat with your data.

## 📚 Usage

1. Launch the app by visiting the URL provided by Streamlit.
2. Type your query in natural language or SQL format in the input box and enter to generate the response.
3. The chatbot will generate a response based on your query and display the result, including any relevant data or SQL code.
