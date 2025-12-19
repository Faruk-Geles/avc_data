import streamlit as st 
#import pandas as pd 
#import matplotlib.pyplot as plt 
import pathlib 
import sys 
#import cv2
import os
import pathlib
import warnings
from glob import glob
#import torch
#from streamlit_drawable_canvas import st_canvas
#from PIL import Image, ImageDraw
#import tkinter as tk
#from tkinter import filedialog
from pathlib import Path






#project_dir = pathlib.Path(__file__).resolve().parent
project_dir = pathlib.Path(__file__).resolve().parents[1]
#sys.path.append(str(project_dir))
sys.path.append(str(project_dir))


from src.vidgets.filtering_vidgets import generate_filtering_vidgets
from src.vidgets.good_bad_labelling_widget5 import good_bad_labelling
#from avc_tool.utils.generate_folder_structure import GenerateFolderStructure



# Ignore UserWarnings and DeprecationWarnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# This function opens a folder browser
def pick_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


def generate_optical_flow_sam_main():
    #st.title("Optical flow sam labellening")
    st.sidebar.title('Navigation')
    options = st.sidebar.radio('Pages',
                               options = [
                               'Image Sorting App',])
    
    
    if options == 'Image Sorting App':
        
        #source_images_path, dest_images_root_path = generate_filtering_vidgets()
        #genfolder = GenerateFolderStructure(root_folder=dest_images_root_path)
        #genfolder.generate_folders()
        with st.sidebar:
            source_images_root_path = Path("/home/faruk/PROJECTS/CERTAIN_PROJECT/data/Kungsbacka_v20_originals_squared")
            # Get only subfolders
            orig_mages_path = Path("/home/faruk/PROJECTS/CERTAIN_PROJECT/data/Kungsbacka_images")
            
            
            class_folders = [f.name for f in source_images_root_path.iterdir() if f.is_dir()]

            if not class_folders:
                source_images_path = source_images_root_path
            else:
                selected_class = st.selectbox("Choose a folder:", class_folders)
                
                source_images_path = os.path.join(source_images_root_path, selected_class)
            
            dest_images_root_path = "/mnt/nas/Projects/CertAIn/AVC_data_labelling/classified_images"
            
        good_bad_labelling(orig_mages_path,source_images_path, dest_images_root_path)   
        
        

            

        
        
        
    
if __name__ == "__main__":
    generate_optical_flow_sam_main()