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



# --------------------------------------------------
# CONFIG
# --------------------------------------------------
VALID_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

@st.cache_resource
def list_images(folder):
    return sorted([
        p for p in pathlib.Path(folder).iterdir()
        if p.is_file() and p.suffix.lower() in VALID_EXTS
    ])

def matching_crops(original_path, all_crops):
    base = original_path.stem + "_"
    return [c for c in all_crops if c.stem.startswith(base)]

def safe_load(path):
    try:
        return Image.open(path).convert("RGB")
    except (UnidentifiedImageError, OSError):
        return None

# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def good_bad_labelling(
    source_images_folder: str,
    cropped_images_folder: str,
    dest_images_root: str
):
    
    os.makedirs(dest_images_root, exist_ok=True)
    #directory_list = os.listdir(dest_images_root_path)

    # ----------------- NEW CATEGORY -----------------
    new_folder_name, new_button_name, new_folder_path = generate_new_category(dest_images_root)

    genfolder = GenerateFolderStructure(root_folder=dest_images_root)
    genfolder.generate_folders()

    if new_folder_path:
        st.success(f"New category folder created → {new_folder_path}")
    
    
    #os.makedirs(dest_images_root, exist_ok=True)

    originals = list_images(source_images_folder)
    all_crops = list_images(cropped_images_folder)

    if not originals:
        st.error("No original images found.")
        return

    # ----------------- STATE -----------------
    st.session_state.setdefault("orig_idx", 0)
    st.session_state.setdefault("crop_idx", 0)

    # ----------------- CATEGORIES -----------------
    categories = sorted([
        d.name for d in pathlib.Path(dest_images_root).iterdir()
        if d.is_dir()
    ])

    if not categories:
        st.warning("No category folders found.")
        return

    # ----------------- SIDEBAR -----------------
    st.sidebar.header("Navigation")

    jump = st.sidebar.number_input(
        "Jump to original index",
        0, len(originals) - 1,
        st.session_state.orig_idx
    )

    if st.sidebar.button("Go"):
        st.session_state.orig_idx = int(jump)
        st.session_state.crop_idx = 0
        st.rerun()

    width = st.sidebar.slider("Image width", 300, 1200, 700)

    # ----------------- END -----------------
    if st.session_state.orig_idx >= len(originals):
        st.success("🎉 All images processed!")
        return

    original = originals[st.session_state.orig_idx]
    original_img = safe_load(original)

    if original_img is None:
        st.warning("Original corrupted, skipping")
        st.session_state.orig_idx += 1
        st.session_state.crop_idx = 0
        st.rerun()

    crops = matching_crops(original, all_crops)

    # ----------------- DISPLAY -----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(original_img, width=width, caption=original.name)

    with col2:
        st.subheader("Cropped")

        if not crops:
            st.info("No crops found for this image")
        else:
            if st.session_state.crop_idx >= len(crops):
                st.session_state.crop_idx = 0

            crop = crops[st.session_state.crop_idx]
            crop_img = safe_load(crop)

            if crop_img is None:
                st.warning("Crop corrupted, skipping")
                st.session_state.crop_idx += 1
                st.rerun()

            st.image(
                crop_img,
                width=width,
                caption=f"{crop.name} "
                        f"({st.session_state.crop_idx + 1}/{len(crops)})"
            )

    # ----------------- CATEGORY BUTTONS -----------------
    st.write("### Assign category")

    cols = st.columns(4)

    for i, cat in enumerate(categories):
        with cols[i % 4]:
            if st.button(cat, key=f"cat_{cat}"):

                target = pathlib.Path(dest_images_root) / cat
                target.mkdir(exist_ok=True)

                # move crop only
                if crops:
                    shutil.move(
                        crops[st.session_state.crop_idx],
                        target / crops[st.session_state.crop_idx].name
                    )

                # advance
                if crops and st.session_state.crop_idx + 1 < len(crops):
                    st.session_state.crop_idx += 1
                else:
                    st.session_state.crop_idx = 0
                    st.session_state.orig_idx += 1

                st.rerun()

    # ----------------- NAVIGATION -----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("◀ Prev"):
            if st.session_state.crop_idx > 0:
                st.session_state.crop_idx -= 1
            else:
                st.session_state.orig_idx = max(0, st.session_state.orig_idx - 1)
                st.session_state.crop_idx = 0
            st.rerun()

    with c2:
        if st.button("Next ▶"):
            if crops and st.session_state.crop_idx + 1 < len(crops):
                st.session_state.crop_idx += 1
            else:
                st.session_state.crop_idx = 0
                st.session_state.orig_idx += 1
            st.rerun()

    with c3:
        st.write(
            f"Original {st.session_state.orig_idx + 1}/{len(originals)}"
        )
