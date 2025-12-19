import webview
import subprocess
import os
 
# Start streamlit server
script_path = os.path.join(os.path.dirname(__file__), "avc_data_app.py")

subprocess.Popen(["python", "-m", "streamlit", "run", script_path])
 
# Open in a webview window
webview.create_window("My App", "http://localhost:8501")
webview.start()