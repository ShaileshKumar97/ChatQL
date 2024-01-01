import os

import streamlit as st

from inputs.validation import validate_input


def postgres_input():
    OPENAI_API_KEY = st.sidebar.text_input(
        "Provide your OpenAI API Key",
        placeholder="Please enter Your OpenAI API Token!",
        type="password",
    )
    USER_NAME = st.sidebar.text_input(
        "Provide your PostgreSQL User Name",
        placeholder="Please enter your PostgreSQL User Name!",
        type="password",
    )
    PASSWORD = st.sidebar.text_input(
        "Provide your PostgreSQL Password",
        placeholder="Please enter your PostgreSQL Password!",
        type="password",
    )
    HOST = st.sidebar.text_input(
        "Provide your PostgreSQL HOST",
        placeholder="Please enter your PostgreSQL HOST!",
        type="password",
    )
    PORT = st.sidebar.text_input(
        "Provide your PostgreSQL PORT",
        placeholder="Please enter your PostgreSQL PORT!",
        type="password",
    )
    DATABASE = st.sidebar.text_input(
        "Provide your PostgreSQL Database Name",
        placeholder="Please enter your PostgreSQL Database Name!",
        type="password",
    )
    SCHEMA = st.sidebar.text_input(
        "Provide your PostgreSQL Schema",
        placeholder="Please enter your PostgreSQL Schema!",
        type="password",
    )

    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    if st.sidebar.button("Submit") or st.session_state.load_state:
        st.session_state.load_state = True

        if not OPENAI_API_KEY:
            validate_input("PostgreSQL OPENAI_API_KEY is missing.")
        elif not USER_NAME:
            validate_input("PostgreSQL USER_NAME is missing.")
        elif not PASSWORD:
            validate_input("PostgreSQL PASSWORD is missing.")
        elif not HOST:
            validate_input("PostgreSQL HOST is missing.")
        elif not DATABASE:
            validate_input("PostgreSQL DATABASE is missing.")
        elif not SCHEMA:
            validate_input("PostgreSQL SCHEMA is missing.")
        elif not PORT:
            validate_input("PostgreSQL PORT is missing.")
        else:
            st.session_state["db_name"] = 1

            os.environ["open"] = "dadfadfasdf"
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            os.environ["USER_NAME"] = USER_NAME
            os.environ["PASSWORD"] = PASSWORD
            os.environ["HOST"] = HOST
            os.environ["DATABASE"] = DATABASE
            os.environ["SCHEMA"] = SCHEMA
            os.environ["PORT"] = PORT

            st.session_state["credentials"] = True
            st.session_state["credentials_created"] = True

            st.experimental_rerun()
