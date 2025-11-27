import streamlit as st 
import pandas as pd 
import numpy as pd 
import pathlib, sys, os

project_dir = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
#from container_mask_vidgets.folder_path_selection import folder_picker



def generate_filtering_vidgets():
    
    with st.sidebar:
             
    
        st.sidebar.markdown("---")
        source_images_path = st.text_area("Enter images folder path:",
                                   value = "/mnt/nas/Projects/CertAIn/AVC_data_labelling/sam_masked_images")

        dest_images_root_path = st.text_area("dest folder path: ", 
                                    "/mnt/nas/Projects/CertAIn/AVC_data_labelling/classified_images")
        
        
        st.sidebar.markdown("---")

            

        return source_images_path, dest_images_root_path