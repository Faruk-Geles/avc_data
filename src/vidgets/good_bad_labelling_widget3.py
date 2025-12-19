import streamlit as st 
import pandas as pd 
import numpy as np 
import pathlib, sys, os, shutil
from tkinter import Tk, filedialog
from PIL import Image, UnidentifiedImageError
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
@lru_cache(maxsize=1024)
def load_thumbnail(path, size):
    img = Image.open(path)
    img.thumbnail((size, size))
    return img
    

"""@lru_cache(maxsize=256)
def load_thumbnail(path, target_width):
    img = Image.open(path).convert("RGB")

    w, h = img.size

    max_upscale = 2.0  # allow up to 2x enlargement

    scale = min(target_width / w, max_upscale)

    # scale factor
    #scale = target_width / w
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize (allows upscaling AND downscaling)
    img = img.resize((new_w, new_h), Image.BILINEAR)#Image.LANCZOS)

    return img"""


# ===========================================================
#                     MAIN LABELING FUNCTION
# ===========================================================

def good_bad_labelling(source_images_folder, dest_images_root_path):

    os.makedirs(dest_images_root_path, exist_ok=True)
    directory_list = os.listdir(dest_images_root_path)

    # ----------------- NEW CATEGORY -----------------
    new_folder_name, new_button_name, new_folder_path = generate_new_category(dest_images_root_path)

    genfolder = GenerateFolderStructure(root_folder=dest_images_root_path)
    genfolder.generate_folders()

    if new_folder_path:
        st.success(f"New category folder created → {new_folder_path}")

    # ----------------- LOAD IMAGES -----------------
    images_list = get_images_list(source_images_folder)

    if "index" not in st.session_state:
        st.session_state.index = 0

    # ----------------- SIDEBAR JUMP TO INDEX -----------------
    st.sidebar.subheader("Jump to Image Index")

    max_index = len(images_list) - 1

    jump_to = st.sidebar.number_input(
        "Go to index:",
        min_value=0,
        max_value=max_index,
        value=st.session_state.index,
        step=1
    )

    if st.sidebar.button("Go"):
        st.session_state.index = int(jump_to)
        st.rerun()

    # ----------------- END OF LIST -----------------
    if st.session_state.index >= len(images_list):
        st.success("🎉 All images processed!")
        return

    img_path = images_list[st.session_state.index]

    # ===========================================================
    #         LOAD IMAGE SAFELY (SKIP IF CORRUPTED / MISSING)
    # ===========================================================
    size = st.sidebar.slider("Image width (px)", 100, 1000, 600)

    try:
        img = load_thumbnail(img_path, size)

    except (FileNotFoundError, UnidentifiedImageError, OSError):
        st.error(f"⚠️ Problem loading image: {img_path.name}, skipping...")

        # Remove or skip?
        st.session_state.index += 1
        st.rerun()
        return

    st.image(img, caption=f"Image {st.session_state.index + 1}")

    # ===========================================================
    #                 CATEGORY BUTTONS GRID
    # ===========================================================
    cols_per_row = 4

    for i in range(0, len(directory_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            idx = i + j
            if idx < len(directory_list):

                dir_name = directory_list[idx]

                if cols[j].button(dir_name, key=f"btn_{idx}"):

                    target_dir = os.path.join(dest_images_root_path, dir_name)
                    os.makedirs(target_dir, exist_ok=True)

                    try:
                        shutil.move(img_path, target_dir)
                    except Exception as e:
                        st.error(f"Move failed: {e}")
                        st.session_state.index += 1
                        st.rerun()

                    st.session_state.index += 1
                    st.rerun()

    # ===========================================================
    #                 DYNAMIC CATEGORY BUTTONS
    # ===========================================================
    st.write("### Dynamic Categories")

    if "categories" in st.session_state and st.session_state.categories:

        cols = st.columns(4)
        col_idx = 0

        for folder_name, button_label in st.session_state.categories.items():
            folder_path = os.path.join(dest_images_root_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            with cols[col_idx]:
                if st.button(button_label, key=f"dyn_btn_{col_idx}"):

                    shutil.move(img_path, folder_path)
                    st.session_state.index += 1
                    st.rerun()

            col_idx += 1

            if col_idx == 4:
                cols = st.columns(4)
                col_idx = 0
