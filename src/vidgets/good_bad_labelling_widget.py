import streamlit as st 
import pandas as pd 
import numpy as pd 
import pathlib, sys, os, shutil
from tkinter import Tk, filedialog
import os
from PIL import Image
from functools import lru_cache

project_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(project_dir))

from src.vidgets.new_category_widget import generate_new_category
from src.utils.generate_folder_structure import GenerateFolderStructure


# ---------- CACHE IMAGE LIST ----------
@st.cache_resource
def get_images_list(source_images_folder):
    return sorted([f for f in pathlib.Path(source_images_folder).glob("*.*")])


# ---------- CACHE THUMBNAILS ----------
@lru_cache(maxsize=256)
def load_thumbnail(path, size):
    img = Image.open(path)
    img.thumbnail((size, size))
    return img


# ===========================================================
#                     MAIN LABELING FUNCTION
# ===========================================================

def good_bad_labelling(source_images_folder, dest_images_root_path):

    # ----------------- FIX: ENSURE BASE DIR EXISTS -----------------
    os.makedirs(dest_images_root_path, exist_ok=True)

    # ----------------- CREATE DEFAULT CATEGORY DIRECTORIES ----------
    directory_list = os.listdir(dest_images_root_path)
    
    # ----------------- CREATE NEW CATEGORY (WIDGET) -----------------
    new_folder_name, new_button_name, new_folder_path = generate_new_category(dest_images_root_path)

    genfolder = GenerateFolderStructure(root_folder=dest_images_root_path)
    genfolder.generate_folders()

    if new_folder_path:
        st.success(f"New category folder created → {new_folder_path}")

    # ----------------- LOAD IMAGES LIST -----------------
    images_list = get_images_list(source_images_folder)

    if "index" not in st.session_state:
        st.session_state.index = 0

    if st.session_state.index >= len(images_list):
        st.success("🎉 All images processed!")
        return

    img_path = images_list[st.session_state.index]

    # ----------------- DISPLAY IMAGE -----------------
    size = st.sidebar.slider("Image width (px)", 100, 1000, 800)
    img = load_thumbnail(img_path, size)
    st.image(img, caption=f"Image {st.session_state.index + 1}")

    # ===========================================================
    #                 FIXED CATEGORY BUTTONS
    # ===========================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        for dir in directory_list[0:4]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()

    with col2:
        for dir in directory_list[4:8]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()

    with col3:
        for dir in directory_list[8:12]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()

  

    # ========== DYNAMIC CATEGORY BUTTONS ==========
    # ========== DYNAMIC CATEGORY BUTTONS ==========
    """st.write("### Dynamic Categories")

    if "categories" in st.session_state and st.session_state.categories:
        
        for dir in directory_list[12:]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()"""
                
    # ----------------- DYNAMIC CATEGORY BUTTONS -----------------
    """st.write("### Dynamic Categories")

    if "categories" in st.session_state and st.session_state.categories:

        for folder_name, button_label in st.session_state.categories.items():

            folder_path = os.path.join(dest_images_root_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            if st.button(button_label):
                shutil.move(img_path, folder_path)
                st.session_state.index += 1
                st.rerun()"""


    # ----------------- DYNAMIC CATEGORY BUTTONS IN ROWS -----------------
    st.write("### Dynamic Categories")

    if "categories" in st.session_state and st.session_state.categories:

        cols = st.columns(4)   # number of buttons per row
        col_index = 0

        for folder_name, button_label in st.session_state.categories.items():

            folder_path = os.path.join(dest_images_root_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # place button inside the correct column
            with cols[col_index]:
                if st.button(button_label):
                    shutil.move(img_path, folder_path)
                    st.session_state.index += 1
                    st.rerun()

            col_index += 1

            # reset row after 4 buttons
            if col_index == 4:
                cols = st.columns(4)
                col_index = 0


 
 
