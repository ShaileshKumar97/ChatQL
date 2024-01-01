import os

import streamlit as st

from inputs.validation import validate_input


def snowflake_input():
    OPENAI_API_KEY = st.sidebar.text_input(
        "Provide your OpenAI API Key",
        placeholder="Please enter Your OpenAI API Token!",
        type="password",
    )
    USER_NAME = st.sidebar.text_input(
        "Provide your Snowflake User Name",
        placeholder="Please enter your Snowflake User Name!",
        type="password",
    )
    PASSWORD = st.sidebar.text_input(
        "Provide your Snowflake Password",
        placeholder="Please enter your Snowflake Password!",
        type="password",
    )
    ACCOUNT = st.sidebar.text_input(
        "Provide your Snowflake Account",
        placeholder="Please enter your Snowflake Account!",
        type="password",
    )
    DATABASE = st.sidebar.text_input(
        "Provide your Snowflake Database Name",
        placeholder="Please enter your Snowflake Database Name!",
        type="password",
    )
    SCHEMA = st.sidebar.text_input(
        "Provide your Snowflake Schema",
        placeholder="Please enter your Snowflake Schema!",
        type="password",
    )
    WAREHOUSE = st.sidebar.text_input(
        "Provide your Snowflake Warehouse",
        placeholder="Please enter your Snowflake Warehouse!",
        type="password",
    )
    ROLE = st.sidebar.text_input(
        "Provide your Snowflake Role",
        placeholder="Please enter your Snowflake Role!",
        type="password",
    )

    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    if st.sidebar.button("Submit") or st.session_state.load_state:
        st.session_state.load_state = True

        if not OPENAI_API_KEY:
            validate_input("Snowflake OPENAI_API_KEY is missing.")
        elif not USER_NAME:
            validate_input("Snowflake USER_NAME is missing.")
        elif not PASSWORD:
            validate_input("Snowflake PASSWORD is missing.")
        elif not ACCOUNT:
            validate_input("Snowflake ACCOUNT is missing.")
        elif not DATABASE:
            validate_input("Snowflake DATABASE is missing.")
        elif not SCHEMA:
            validate_input("Snowflake SCHEMA is missing.")
        elif not WAREHOUSE:
            validate_input("Snowflake WAREHOUSE is missing.")
        elif not ROLE:
            validate_input("Snowflake ROLE is missing.")
        else:
            st.session_state["db_name"] = 1

            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            os.environ["USER_NAME"] = USER_NAME
            os.environ["PASSWORD"] = PASSWORD
            os.environ["ACCOUNT"] = ACCOUNT
            os.environ["DATABASE"] = DATABASE
            os.environ["SCHEMA"] = SCHEMA
            os.environ["WAREHOUSE"] = WAREHOUSE
            os.environ["ROLE"] = ROLE

            st.session_state["credentials"] = True
            st.session_state["credentials_created"] = True

            st.experimental_rerun()
