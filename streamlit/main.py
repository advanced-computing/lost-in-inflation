import subprocess
import sys
import os

# Use your virtual environment explicitly
venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

print("🔄 Running BigQuery loader...")
subprocess.run([venv_python, "streamlit/gbqload.py"], check=True)

print("🚀 Launching Streamlit app...")
subprocess.run(["streamlit", "run", "streamlit/my_streamlit_app.py"])
