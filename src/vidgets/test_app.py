import streamlit as st
import subprocess
import sys, pathlib

#project_dir = pathlib.Path(__file__).resolve().parent
project_dir = pathlib.Path(__file__).resolve().parents[1]
#sys.path.append(str(project_dir))
sys.path.append(str(project_dir))
from vidgets.folder_picker import pick_folder


# ---- Session state init (MUST be before widgets) ----
if "folder_path" not in st.session_state:
    st.session_state.folder_path = ""

st.title("Folder Picker")

col1, col2 = st.columns([4, 1])

# 🔹 Textbox that shows selected folder (value comes from session_state only)
col1.text_input(
    "Selected Folder",
    value=st.session_state.folder_path,
    key="folder_display",
)

# 🔹 Browse button
if col2.button("📁 Browse"):
    python_exe = sys.executable
    helper_script = pick_folder()

    result = subprocess.run(
        [python_exe, helper_script],
        capture_output=True,
        text=True,
    )

    selected = result.stdout.strip()

    if selected:
        # Update session state ONLY
        st.session_state.folder_path = selected
        st.experimental_rerun()

