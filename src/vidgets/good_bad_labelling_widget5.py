import streamlit as st
import pathlib
import os
import shutil
from PIL import Image, UnidentifiedImageError


import pandas as pd 
import numpy as np 
import pathlib, sys, os, shutil
from tkinter import Tk, filedialog
from functools import lru_cache

project_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(project_dir))

from src.vidgets.new_category_widget import generate_new_category
from src.utils.generate_folder_structure import GenerateFolderStructure


# ===========================================================
#                   IMAGE HELPERS
# ===========================================================

def list_images(folder):
    return sorted([
        p for p in pathlib.Path(folder).glob("*.*")
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ])


def is_valid_image(path: pathlib.Path) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


@lru_cache(maxsize=1024)
def load_image(path: pathlib.Path, target_width: int):
    img = Image.open(path).convert("RGB")

    w, h = img.size

    # --- CONFIG ---
    max_upscale = 1.5        # do not enlarge more than 150%
    allow_upscale = True

    scale = target_width / w

    if scale > 1.0:
        if not allow_upscale:
            return img
        scale = min(scale, max_upscale)

    new_w = int(w * scale)
    new_h = int(h * scale)

    # Choose resampling filter
    resample = Image.LANCZOS if scale < 1 else Image.BICUBIC

    img = img.resize((new_w, new_h), resample=resample)
    return img


"""@lru_cache(maxsize=1024)
def load_image(path: pathlib.Path, width: int):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = width / w
    img = img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)
    return img"""


# ===========================================================
#         BUILD VALID ORIGINAL–CROP PAIRS (FILTERING)
# ===========================================================

@st.cache_resource
def build_valid_pairs(originals, crops):
    pairs = []

    for orig in originals:
        if not is_valid_image(orig):
            continue

        prefix = orig.stem + "_"
        matched = [
            c for c in crops
            if c.stem.startswith(prefix) and is_valid_image(c)
        ]

        if matched:
            pairs.append((orig, matched))

    return pairs


# ===========================================================
#                  MAIN LABELING ROUTINE
# ===========================================================

def good_bad_labelling(
    source_images_folder: str,
    cropped_images_folder: str,
    dest_images_root: str
):
    
    os.makedirs(dest_images_root, exist_ok=True)
    directory_list = os.listdir(dest_images_root)

    # ----------------- NEW CATEGORY -----------------
    new_folder_name, new_button_name, new_folder_path = generate_new_category(dest_images_root)

    genfolder = GenerateFolderStructure(root_folder=dest_images_root)
    genfolder.generate_folders()

    if new_folder_path:
        st.success(f"New category folder created → {new_folder_path}")

    # ---------- LOAD FILES ----------
    originals = list_images(source_images_folder)
    all_crops = list_images(cropped_images_folder)

    pairs = build_valid_pairs(originals, all_crops)

    if not pairs:
        st.error("❌ No valid original–crop pairs found.")
        return

    # ---------- SESSION STATE ----------
    if "orig_idx" not in st.session_state:
        st.session_state.orig_idx = 0

    if "crop_idx" not in st.session_state:
        st.session_state.crop_idx = 0

    # ---------- END ----------
    if st.session_state.orig_idx >= len(pairs):
        st.success("🎉 All images processed!")
        return

    original, crops = pairs[st.session_state.orig_idx]

    if st.session_state.crop_idx >= len(crops):
        st.session_state.crop_idx = 0

    crop = crops[st.session_state.crop_idx]

    # ---------- SIDEBAR ----------
    size = st.sidebar.slider("Image width", 300, 1200, 600)
    """zoom = st.sidebar.slider("Zoom (%)",
                             min_value=25,
                             max_value=200,
                             value=100,
                             step=5
    )"""


    st.sidebar.markdown(
        f"""
        **Original:** {st.session_state.orig_idx + 1} / {len(pairs)}  
        **Crop:** {st.session_state.crop_idx + 1} / {len(crops)}
        """
    )

    # ---------- LOAD IMAGES ----------
    try:
        orig_img = load_image(original, size)
        crop_img = load_image(crop, size)
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        st.warning("⚠️ Image unreadable, skipping")
        st.session_state.crop_idx += 1
        st.rerun()
        return

    # ---------- DISPLAY ----------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(orig_img, caption=original.name)#, use_column_width=True)

    with col2:
        st.subheader("Crop")
        st.image(crop_img, caption=crop.name)#, use_column_width=True)


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

                    target_dir = os.path.join(dest_images_root, dir_name)
                    os.makedirs(target_dir, exist_ok=True)

                    try:
                        shutil.move(crop, target_dir)
                    except Exception as e:
                        st.error(f"Move failed: {e}")
                        # ---- advance logic ----
                        if st.session_state.crop_idx + 1 < len(crops):
                            st.session_state.crop_idx += 1
                        else:
                            st.session_state.crop_idx = 0
                            st.session_state.orig_idx += 1

                        st.rerun()

                    #st.session_state.index += 1
                    #st.rerun()
                    
                    # ---- advance logic ----
                    if st.session_state.crop_idx + 1 < len(crops):
                        st.session_state.crop_idx += 1
                    else:
                        st.session_state.crop_idx = 0
                        st.session_state.orig_idx += 1

                    st.rerun()

    # ===========================================================
    #                 DYNAMIC CATEGORY BUTTONS
    # ===========================================================
    st.write("### Dynamic Categories")

    if "categories" in st.session_state and st.session_state.categories:

        cols = st.columns(4)
        col_idx = 0

        for folder_name, button_label in st.session_state.categories.items():
            folder_path = os.path.join(dest_images_root, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            with cols[col_idx]:
                if st.button(button_label, key=f"dyn_btn_{col_idx}"):

                    shutil.move(crop, folder_path)
                    #st.session_state.index += 1
                    #st.rerun()
                    
                    # ---- advance logic ----
                    if st.session_state.crop_idx + 1 < len(crops):
                        st.session_state.crop_idx += 1
                    else:
                        st.session_state.crop_idx = 0
                        st.session_state.orig_idx += 1

                    st.rerun()

            col_idx += 1

            if col_idx == 4:
                cols = st.columns(4)
                col_idx = 0
