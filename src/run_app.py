import subprocess
import sys
import os
 
# Don't import streamlit directly in the launcher!
if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(bundle_dir, 'avc_data_app.py')
    # Run streamlit as a subprocess
    subprocess.run([
        'streamlit', 
        'run', 
        app_path,
        '--server.headless=true',
        '--server.port=8501'
    ])
    
    