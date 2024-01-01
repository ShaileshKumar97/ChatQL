# Use a base image with Python and Streamlit dependencies
FROM python:3.8

# Define Arguments
ARG OPENAI_API_KEY_ARG
ARG USER_NAME_ARG
ARG PASSWORD_ARG
ARG ACCOUNT_ARG
ARG WAREHOUSE_ARG
ARG ROLE_ARG
ARG DATABASE_ARG
ARG SCHEMA_ARG

# Create directory structure: Establish the main folder structure
RUN mkdir -p /app/faiss_index_snowflake
RUN mkdir -p /app/sql
RUN mkdir -p /app/ui
RUN mkdir -p /app/utils

WORKDIR /app

# Define environmental variables
ENV OPENAI_API_KEY=${OPENAI_API_KEY_ARG}
ENV USER_NAME=${USER_NAME_ARG}
ENV PASSWORD=${PASSWORD_ARG}
ENV ACCOUNT=${ACCOUNT_ARG}
ENV WAREHOUSE=${WAREHOUSE_ARG}
ENV ROLE=${ROLE_ARG}
ENV DATABASE=${DATABASE_ARG}
ENV SCHEMA=${SCHEMA_ARG}

COPY faiss_index_snowflake /app/faiss_index_snowflake
COPY sql /app/sql
COPY ui /app/ui
COPY utils /app/utils
COPY app.py /app/
COPY __init__.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD streamlit run app.py --server.port=8050 --server.address=0.0.0.0 --logger.level error
