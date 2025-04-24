# streamlit/auth.py
import os
import json
import streamlit as st
from google.oauth2 import service_account

def get_bigquery_credentials():
    if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
        print("🔐 Using GitHub Actions secret for authentication.")
        credentials_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
        project_id = credentials_dict["project_id"]
    else:
        print("🔐 Using Streamlit secrets for local dev.")
        project_id = st.secrets["google_cloud"]["project_id"]
        with open(st.secrets["google_cloud"]["service_account_file"], "r") as f:
            credentials_dict = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    return credentials, project_id
