import streamlit as st 
import pandas as pd 
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
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog

#project_dir = pathlib.Path(__file__).resolve().parent
project_dir = pathlib.Path(__file__).resolve().parents[1]
#sys.path.append(str(project_dir))
sys.path.append(str(project_dir))


from src.vidgets.filtering_vidgets import generate_filtering_vidgets
from src.vidgets.good_bad_labelling_widget import good_bad_labelling
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
                               'extract_subset_filtering model',])
    
    
    if options == 'extract_subset_filtering model':
        
        source_images_path, dest_images_root_path = generate_filtering_vidgets()
        #genfolder = GenerateFolderStructure(root_folder=dest_images_root_path)
        #genfolder.generate_folders()
        
        good_bad_labelling(source_images_path, dest_images_root_path)   
        
        

            

        
        
        
    
if __name__ == "__main__":
    generate_optical_flow_sam_main()