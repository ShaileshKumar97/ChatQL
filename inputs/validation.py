import streamlit as st


def validate_input(input):
    st.error(input)
    st.session_state.load_state = False
    st.stop()
