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
    try:
        img = Image.open(path)
        img.verify()   # check if corrupted
        img = Image.open(path)  # reopen for actual processing
        img.thumbnail((size, size))
        return img
    except Exception:
        return None


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
    #img = load_thumbnail(img_path, size)
    #st.image(img, caption=f"Image {st.session_state.index + 1}")
    
    img = load_thumbnail(str(img_path), size)
    # If image is corrupted → skip to next one
    if img is None:
        st.warning(f"⚠️ Image corrupted or unreadable: {img_path.name}. Skipping…")
        st.session_state.index += 1
        st.rerun()

    # Display image normally
    st.image(img, caption=f"Image {st.session_state.index + 1}")

    # ===========================================================
    #                 FIXED CATEGORY BUTTONS
    # ===========================================================
    



    # Initialize index
    if "index" not in st.session_state:
        st.session_state.index = 0

    #st.write(f"Current index: {st.session_state.index}")

    cols_per_row = 4  # 8 buttons per row

    for i in range(0, len(directory_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            idx = i + j
            if idx < len(directory_list):

                dir_name = directory_list[idx]

                # CREATE BUTTON IN GRID
                if cols[j].button(dir_name, key=f"btn_{idx}"):

                    # CREATE TARGET FOLDER if not exists
                    target_dir = os.path.join(dest_images_root_path, dir_name)
                    os.makedirs(target_dir, exist_ok=True)

                    # MOVE IMAGE
                    shutil.move(img_path, target_dir)

                    # INCREMENT INDEX
                    st.session_state.index += 1

                    # RERUN APP
                    st.rerun()


    
    
    
    
    

    """col1, col2, col3, col4, col5,col6 = st.columns(6)

    with col1:
        for dir in directory_list[0:6]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()

    with col2:
        for dir in directory_list[6:12]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()

    with col3:
        for dir in directory_list[12:18]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()
                
    with col4:
        for dir in directory_list[18:24]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()
                
    with col5:
        for dir in directory_list[24:30]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()
                
    with col6:
        for dir in directory_list[30:32]:
            if st.button(dir):
                shutil.move(img_path, os.path.join(dest_images_root_path,dir))
                st.session_state.index += 1
                st.rerun()
                
    """
                

                


  

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
                if st.button(button_label, key=f"dup_btn_{col_index}"):
                    shutil.move(img_path, folder_path)
                    st.session_state.index += 1
                    st.rerun()

            col_index += 1

            # reset row after 4 buttons
            if col_index == 4:
                cols = st.columns(4)
                col_index = 0


 
 
