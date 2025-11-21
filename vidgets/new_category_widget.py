import streamlit as st
import os

def generate_new_category(BASE_DIR):
    # --- SESSION STATE INITIALIZATION ---
    if "categories" not in st.session_state:
        st.session_state.categories = {}  # {folder_name: button_label}

    new_folder_name = None
    new_button_name = None
    folder_path = None

    # --- SIDEBAR FOR ADDING NEW CATEGORY ---
    st.sidebar.header("➕ Add New Category")

    with st.sidebar.form("add_category_form"):
        new_folder_name = st.text_input("Enter folder name:")
        new_button_name = st.text_input("Enter button name:")

        submitted = st.form_submit_button("Add Category")

        if submitted:
            if new_folder_name and new_button_name:
                # Create the folder
                folder_path = os.path.join(BASE_DIR, new_folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Store the category in state
                st.session_state.categories[new_folder_name] = new_button_name

                st.success(
                    f"✅ New Category Created!\n\n"
                    f"**Button Label:** {new_button_name}\n"
                    f"**Folder Name:** {new_folder_name}\n"
                    f"**Folder Path:** `{folder_path}`"
                )
            else:
                st.error("⚠️ You must enter BOTH a folder name and a button name!")

    # 🔄 Return values so they can be used in your main app
    return new_folder_name, new_button_name, folder_path


def show_category_buttons(BASE_DIR):
    """
    Creates dynamic buttons for each category in st.session_state.categories.
    Returns the selected folder if a button is clicked.
    """
    if "categories" not in st.session_state:
        return None  # No categories yet

    selected_category = None

    for folder_name, button_label in st.session_state.categories.items():
        if st.button(button_label):
            selected_category = os.path.join(BASE_DIR, folder_name)

    return selected_category