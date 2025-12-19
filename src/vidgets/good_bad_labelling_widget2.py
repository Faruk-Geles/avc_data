import streamlit as st
import pathlib
import shutil
from PIL import Image, UnidentifiedImageError
from functools import lru_cache
import os, sys

project_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(project_dir))

from src.vidgets.new_category_widget import generate_new_category
from src.utils.generate_folder_structure import GenerateFolderStructure

# =============================
#          CACHES
# =============================

@st.cache_resource
def get_images_list(source_images_folder):
    """Return a sorted list of valid file paths."""
    p = pathlib.Path(source_images_folder)
    return sorted([f for f in p.glob("*.*") if f.is_file()])


@lru_cache(maxsize=256)
def load_thumbnail(path, size):
    """Load safe thumbnail. Return None if corrupted or unreadable."""
    try:
        img = Image.open(path)
        img.thumbnail((size, size))
        return img
    except (UnidentifiedImageError, OSError):
        return None


# ===========================================================
#               MAIN LABELING FUNCTION (STABLE)
# ===========================================================

def good_bad_labelling(source_images_folder, dest_images_root_path):

    genfolder = GenerateFolderStructure(root_folder=dest_images_root_path)
    genfolder.generate_folders()

    # Ensure output root exists
    os.makedirs(dest_images_root_path, exist_ok=True)

    # Read category folders
    directory_list = sorted(os.listdir(dest_images_root_path))

    # Load images list
    images_list = get_images_list(source_images_folder)

    # Track index
    if "index" not in st.session_state:
        st.session_state.index = 0

    # Done?
    if st.session_state.index >= len(images_list):
        st.success("🎉 All images processed!")
        return

    # Current image
    img_path = images_list[st.session_state.index]

    # =============================
    #      SAFE IMAGE LOADER
    # =============================

    size = st.sidebar.slider("Image width (px)", 200, 1000, 600)
    img = load_thumbnail(str(img_path), size)

    # If image unreadable → skip it
    if img is None:
        st.warning(f"⚠️ Skipping corrupted/unreadable: {img_path.name}")

        # Remove it from the list permanently
        images_list.pop(st.session_state.index)

        st.rerun()
        return

    # Show image
    st.image(img, caption=f"Image {st.session_state.index+1} / {len(images_list)}")

    st.divider()
    st.subheader("Choose Category")

    # ====================================
    #     GRID LAYOUT FOR CATEGORIES
    # ====================================

    cols_per_row = 4

    for i in range(0, len(directory_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            idx = i + j
            if idx >= len(directory_list):
                continue

            label = directory_list[idx]
            folder_path = os.path.join(dest_images_root_path, label)

            if cols[j].button(label, key=f"btn_{idx}"):

                # Ensure target exists
                os.makedirs(folder_path, exist_ok=True)

                # SAFE MOVE BLOCK
                try:
                    if not img_path.exists():
                        raise FileNotFoundError(f"File missing: {img_path}")

                    shutil.move(str(img_path), folder_path)

                except Exception as e:
                    st.error(f"❌ Could not move {img_path.name}: {e}")

                # Move index forward
                st.session_state.index += 1
                st.rerun()

    st.divider()

    # NEXT / SKIP BUTTON
    if st.button("Skip Image ➜"):
        st.session_state.index += 1
        st.rerun()
