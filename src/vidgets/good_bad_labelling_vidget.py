import streamlit as st 
import pandas as pd 
import numpy as pd 
import pathlib, sys, os, shutil
from tkinter import Tk, filedialog


project_dir = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
#from container_mask_vidgets.folder_path_selection import folder_picker
from vidgets.new_category_widget import generate_new_category


import os
import pathlib
import streamlit as st
from PIL import Image
from functools import lru_cache

#source_images_folder = "/path/to/images"
#hard_plast_dir = "/path/to/hard_plast"
#wood_dir = "/path/to/wood"


# ---------- CACHE IMAGE LIST (FAST) ----------
@st.cache_resource
def get_images_list(source_images_folder):
    return sorted([f for f in pathlib.Path(source_images_folder).glob("*.*")])


# ---------- CACHE THUMBNAILS ----------
@lru_cache(maxsize=256)
def load_thumbnail(path, size):
    img = Image.open(path)
    img.thumbnail((size, size))
    return img



# -------- Display Image ----------
#size = st.sidebar.slider("Thumbnail size", 100, 1000, 600)
#img = load_thumbnail(img_path, size)
#st.image(img, caption=f"Image {st.session_state.index+1}")




def good_bad_labelling(source_images_folder, dest_images_root_path):
    
    with st.sidebar:
    
        #st.sidebar.markdown("---")
        #dest_images_root_path = st.text_area("dest folder path: ", 
        #                            "/mnt/nas/Projects/CertAIn/Optical_flow/paper_packaging/sam_masked_images_subset/source_data")
        
        #dest_images_path = st.text_area("dest folder path: ", 
        #                            "/mnt/nas/Projects/CertAIn/Optical_flow/paper_packaging/sam_masked_images_subset/source_data/raw_images")
        
        #good_dir = st.text_area("good folder path: ", 
        #                            "/mnt/nas/Projects/CertAIn/Optical_flow/paper_packaging/sam_masked_images_subset/source_data/good")
        
        #bad_dir = st.text_area("bad folder path: ", 
        #                            "/mnt/nas/Projects/CertAIn/Optical_flow/paper_packaging/sam_masked_images_subset/source_data/bad")
                
        
    
        hard_plast_dir = os.path.join(dest_images_root_path, "hard_plast")
        wood_dir = os.path.join(dest_images_root_path, "wood")
        treated_wood_dir = os.path.join(dest_images_root_path, "treated_wood")
        betong_dir = os.path.join(dest_images_root_path, "betong")
            
        energy_recovery_dir = os.path.join(dest_images_root_path, "energy_recovery")
        non_combustible_dir = os.path.join(dest_images_root_path, "non_combustible")
        metall_dir = os.path.join(dest_images_root_path, "metall")
        well_papp_dir = os.path.join(dest_images_root_path, "well_papp")
        
        paper_packaging_dir = os.path.join(dest_images_root_path, "paper_packaging")
        plastic_packaging_dir = os.path.join(dest_images_root_path, "plastic_packaging")
        isolering_dir = os.path.join(dest_images_root_path, "isolering")
        wee_dir = os.path.join(dest_images_root_path, "wee")
        
    
    new_folder_name, new_button_name, new_folder_path = generate_new_category(dest_images_root_path)  
        #st.sidebar.markdown("---")
    # Step 2 — Confirm creation (only if user pressed the button)
    if new_folder_path:
        st.success(f"New category folder ready → {new_folder_path}")

    # Step 3 — Show dynamic buttons
    st.write("### Categories")
    print(new_folder_path)

    #images_list = [f for f in pathlib.Path(source_images_folder).glob("*.*")]
    images_list = get_images_list(source_images_folder)
    
    if "index" not in st.session_state:
        st.session_state.index = 0 
        
    if st.session_state.index < len(images_list):
        
        img_path = images_list[st.session_state.index]
        
        size = st.sidebar.slider("Image width (px)", 100, 1000, 600)
        
        img = load_thumbnail(img_path, size)
        st.image(img, caption=f"Image {st.session_state.index+1}")
        
        #size = st.sidebar.slider("Image width (px)", 100, 1000, 600)
        
        #st.image(str(img_path), caption=f"Image {st.session_state.index+1}", width=size)#, use_container_width=True)
    
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("HARD PLAST"):
                shutil.move(img_path, hard_plast_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("WOOD"):
                shutil.move(img_path, wood_dir)
                st.session_state.index += 1 
                st.rerun()
            
            if st.button("TREATED_WOOD"):
                shutil.move(img_path, treated_wood_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("BETONG"):
                shutil.move(img_path, betong_dir)
                st.session_state.index += 1 
                st.rerun()
        
        with col2:
            if st.button("ENERGY RECOVERY"):
                shutil.move(img_path, energy_recovery_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("NON-COMBUSTIBLE"):
                shutil.move(img_path, non_combustible_dir)
                st.session_state.index += 1 
                st.rerun()
            
            if st.button("METALL"):
                shutil.move(img_path, metall_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("WELLPAPP"):
                shutil.move(img_path, well_papp_dir)
                st.session_state.index += 1 
                st.rerun()
                
        with col3:
            if st.button("PAPER PACKAGING"):
                shutil.move(img_path, paper_packaging_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("PLASTIC PACKAGING"):
                shutil.move(img_path, plastic_packaging_dir)
                st.session_state.index += 1 
                st.rerun()
            
            if st.button("ISOLERING"):
                shutil.move(img_path, isolering_dir)
                st.session_state.index += 1 
                st.rerun()
                
            if st.button("WEE"):
                shutil.move(img_path, wee_dir)
                st.session_state.index += 1 
                st.rerun()
        
        # Step 2 — Make dynamic buttons for each category
        if "categories" in st.session_state:
            for folder_name, button_label in st.session_state.categories.items():
                if st.button(button_label):
                    st.success(f"You clicked: {button_label} → Folder: {folder_name}")
                    # Example: move the current image
                    # shutil.move(current_image, os.path.join(BASE_DIR, folder_name))
                    shutil.move(img_path, new_folder_path)
                    st.session_state.index += 1 
                    st.rerun()

        

                
                
        
     
 