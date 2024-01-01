import warnings

import streamlit as st
from snowflake.connector.errors import ProgrammingError
from streamlit import components

from constants import Databases
from utils.chatql_ui import extract_code
from utils.chatql_ui import is_sql_query
from utils.chatql_ui import load_chain
from utils.chatql_ui import message_func
from utils.chatql_ui import reset_chat_history
from utils.snowddl import Snowddl
from utils.snowflake import query_data_warehouse

warnings.filterwarnings("ignore")


MAX_INPUTS = 1
chat_history = []
db_history = []


def update_progress_bar(value, prefix, progress_bar=None):
    if progress_bar is None:
        progress_bar = st.empty()

    key = f"{prefix}_progress_bar_value"
    if key not in st.session_state:
        st.session_state[key] = 0

    st.session_state[key] = value
    progress_bar.progress(st.session_state[key])
    if value == 100:
        st.session_state[key] = 0
        progress_bar.empty()


def execute_chain(database_name, query):
    """
    Execute the chain and handle error recovery.

    Args:
        query (str): The query to be executed

    Returns:
        chain_result (dict): The result of the chain execution

    """
    chain_result = None
    try:
        chain = load_chain(database_name)
        chain_result = chain(query)
    except Exception as error:
        print("error", error)
        # Handle error using self_heal mechanism
    return chain_result


def self_heal(cursor, database_name, df, to_extract, i):
    """
    If the query fails, try to fix it by extracting the code from the error message and running it again.

    Args:
        df (pandas.DataFrame): The dataframe generated from the query
        to_extract (str): The query
        i (int): The index of the query in the chat history

    Returns:
        df (pandas.DataFrame): The dataframe generated from the query

    """

    error_message = str(df)
    error_message = (
        "I have an SQL query that's causing an error. FIX The SQL query by searching the schema definition:  \n```sql\n"
        + to_extract
        + "\n```\n Error message: \n "
        + error_message
    )
    recover = execute_chain(database_name, error_message)
    message_func(recover["result"])
    to_extract = extract_code(recover["result"])
    st.session_state["generated"][i] = recover["result"]
    if is_sql_query(to_extract):
        df = query_data_warehouse(cursor, database_name, to_extract)
    return df


def generate_df(cursor, database_name, to_extract: str, i: int):
    """
    Generate a dataframe from the query by querying the data warehouse.

    Args:
        to_extract (str): The query

    Returns:
        df (pandas.DataFrame): The dataframe generated from the query
    """
    df = query_data_warehouse(cursor, database_name, to_extract)
    if isinstance(df, ProgrammingError) and is_sql_query(to_extract):
        message_func("uh oh, I made an error, let me try to fix it")
        del st.session_state["generated"][i]
        df = self_heal(cursor, database_name, df, to_extract, i)
    st.dataframe(df, use_container_width=True)


st.set_page_config(
    page_title="ChatQL",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "About": """ChatQL is a chatbot designed to help you with Snowflake Database. It is built using OpenAI's GPT-4 and Streamlit.
            """
    },
)

snow_ddl = Snowddl()

st.title("ChatQL")
st.caption("Talk your way through data")
st.sidebar.markdown("# ChatQL")
database_name = st.sidebar.selectbox(
    "Select your Database:", options=["", "Snowflake", "PostgreSQL"]
).lower()
if "embeddings_created" not in st.session_state:
    st.session_state["embeddings_created"] = False

if "credentials_created" not in st.session_state:
    st.session_state["credentials_created"] = False


def get_selected_db_credentials(database_name):

    if database_name == Databases.Snowflake.value and "db_name" not in st.session_state:
        from inputs.snowflake_input import snowflake_input

        snowflake_input()
    elif (
        database_name == Databases.PostgreSQL.value
        and "db_name" not in st.session_state
    ):
        from inputs.postgres_input import postgres_input

        postgres_input()
    elif database_name == "":
        st.session_state["credentials"] = False
    else:
        st.session_state["credentials"] = False


if not st.session_state["credentials_created"]:
    st.text(
        "Please select your Database and provide your DB & OpenAI Credentials in sidebar."
    )
    get_selected_db_credentials(database_name)


if (
    not st.session_state["embeddings_created"]
    and st.session_state["credentials"]
    and database_name not in db_history
):
    from embeddings.faiss import create_embeddings_with_schema

    st.sidebar.write(f":green[Your {database_name} credentials are logged!]")
    with st.sidebar:
        with st.spinner("Please wait as we prepare your data for seamless chatting."):
            if database_name == Databases.Snowflake.value:
                from utils.snowflake import snowflake_client

                cursor = snowflake_client()
            if database_name == Databases.PostgreSQL.value:
                from utils.postgresql import postgres_client

                cursor = postgres_client()
            if "cursor" not in st.session_state:
                st.session_state.cursor = cursor
            create_embeddings_with_schema(cursor, database_name)
        st.write(":green[Your app is ready to use. Happy Chatting!]")
        db_history.append(database_name)
        st.session_state.embeddings_created = True

if st.session_state["credentials"] and st.session_state.embeddings_created:
    cursor = st.session_state.cursor
    with open("ui/sidebar.md") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("ui/styles.md") as styles_file:
        styles_content = styles_file.read()

    # Display the DDL for the selected table
    st.sidebar.markdown(f"# Chat with you're {database_name} Data")
    st.sidebar.markdown(sidebar_content)

    # Create a sidebar with a dropdown menu
    selected_table = st.sidebar.selectbox(
        "Select a table:", options=list(snow_ddl.ddl_dict.keys())
    )
    st.sidebar.markdown(f"### DDL for {selected_table} table")
    st.sidebar.dataframe(snow_ddl.ddl_dict[selected_table])  # , hide_index=True)

    st.write(styles_content, unsafe_allow_html=True)

    if "generated" not in st.session_state:
        st.session_state["generated"] = [
            f"HI, I'm ChatQL Assistant, your SQL-speaking sidekick, ready to chat up {database_name.capitalize()} and "
            "get answers faster than a snowball fight in summer! ❄️🔍"
        ]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey!"]
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            (
                f"Hello! I'm a chatbot designed to help you with {database_name.capitalize()} Database."
            )
        ]

    if "query_count" not in st.session_state:
        st.session_state["query_count"] = 0

    RESET = True
    messages_container = st.container()

    with st.form(key="my_form"):
        query = st.text_input(
            "Query: ",
            key="input",
            value="",
            placeholder="Type your query here...",
            label_visibility="hidden",
        )
        submit_button = st.form_submit_button(label="Submit")
    col1, col2 = st.columns([1, 3.2])
    reset_button = col1.button("Reset Chat History")

    if reset_button or st.session_state["query_count"] >= MAX_INPUTS and RESET:
        RESET = False
        st.session_state["query_count"] = 0
        reset_chat_history(database_name.capitalize())

    if "dataframes" not in st.session_state:
        st.session_state["dataframes"] = [0]

    if len(query) > 2 and submit_button:
        submit_progress_bar = st.empty()
        messages = st.session_state["messages"]
        update_progress_bar(33, "submit", submit_progress_bar)

        result = execute_chain(database_name, query)

        update_progress_bar(66, "submit", submit_progress_bar)
        st.session_state["query_count"] += 1
        messages.append((query, result["result"]))
        st.session_state.past.append(query)
        st.session_state.generated.append(result["result"])
        update_progress_bar(100, "submit", submit_progress_bar)

    with messages_container:
        if st.session_state["generated"]:
            for i in range(len(st.session_state["generated"])):
                message_func(st.session_state["past"][i], is_user=True)
                message_func(st.session_state["generated"][i])
                if (
                    i > 0
                    and i not in chat_history
                    and is_sql_query(st.session_state["generated"][i])
                ):
                    code = extract_code(st.session_state["generated"][i])
                    try:
                        if is_sql_query(code):
                            generate_df(cursor, database_name, code, i)
                            chat_history.append(i)
                    except Exception as e:
                        print(e)

    if st.session_state["query_count"] == MAX_INPUTS and RESET:
        st.warning(
            "You have reached the maximum number of inputs. The chat history will be cleared after the next input."
        )

    col2.markdown(
        f'<div style="line-height: 2.5;">{st.session_state["query_count"]}/{MAX_INPUTS}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div id="input-container-placeholder"></div>', unsafe_allow_html=True)

    components.v1.html(
        """
        <script>
        window.addEventListener('load', function() {
            const inputContainer = document.querySelector('.stTextInput');
            const inputContainerPlaceholder = document.getElementById('input-container-placeholder');
            inputContainer.id = 'input-container';
            inputContainerPlaceholder.appendChild(inputContainer);
            document.getElementById("input").focus();
        });
        </script>
        """,
        height=0,
    )
