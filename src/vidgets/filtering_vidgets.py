import streamlit as st 
import pandas as pd 
import numpy as pd 
import pathlib, sys, os

import tkinter.font as tkFont
from tkinter import Tk, filedialog
import tkinter as tk
from tkinter import ttk

project_dir = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))
#from container_mask_vidgets.folder_path_selection import folder_picker

 
def browse_folder():
    
    root = tk.Tk()
    root.withdraw()
    
    # Create a custom toplevel window
    dialog = tk.Toplevel(root)
    dialog.title("Select Folder")
    dialog.geometry("800x600")  # Set custom size
    
    # Configure fonts
    custom_font = ("Arial", 14)
    
    # Create a frame with larger elements
    frame = ttk.Frame(dialog, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Use standard file dialog (will still be limited in customization)
    dialog.destroy()
    
    # Adjust font before opening dialog
    default_font = tk.font.nametofont("TkDefaultFont")
    default_font.configure(size=14)
    root.wm_attributes('-topmost', 1)
    
    folder_path = filedialog.askdirectory(parent=root)
    root.destroy()
    return folder_path



def browse_folder_old():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    
    
    # Configure font size   
    default_font = tkFont.nametofont("TkDefaultFont")     
    default_font.configure(size=16)  # Increase font size 
        
    text_font = tkFont.nametofont("TkTextFont")    
    text_font.configure(size=16)
         
    fixed_font = tkFont.nametofont("TkFixedFont")     
    fixed_font.configure(size=16)     
    
    # Option 1: Using askdirectory with custom window size (limited control)     
    folder_path = filedialog.askdirectory(title="Select a folder",
                                          initialdir="/" )
    
    
    #folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path
 



def generate_filtering_vidgets():
    
    with st.sidebar:
        
        if 'selected_path_1' not in st.session_state:
            st.session_state.selected_path_1 = "/home/faruk/GITHUB/avc_data/test_data/source_images"
        if 'selected_path_2' not in st.session_state:
            st.session_state.selected_path_2 = "/mnt/nas/Projects/CertAIn/AVC_data_labelling/classified_images"
        
        
        
        col1, col2 = st.columns([4, 1])
        with col1:
            path1 = st.text_input("Source Images, Path", 
                                 value=st.session_state.selected_path_1, 
                                 key="path1_input")
        with col2:
            st.write("")
            st.write("")
            if st.button("Browse", key="browse1"):
                selected = browse_folder()
                if selected:
                    st.session_state.selected_path_1 = selected
                    st.rerun()
        

        col3, col4 = st.columns([4, 1])
        with col3:
            path2 = st.text_input("Labelled Images Path", 
                                 value=st.session_state.selected_path_2, 
                                 key="path2_input")
        with col4:
            st.write("")
            st.write("")
            if st.button("Browse", key="browse2"):
                selected = browse_folder()
                if selected:
                    st.session_state.selected_path_2 = selected
                    st.rerun()

        
    
        st.sidebar.markdown("---")
        #source_images_path = st.text_area("Enter images folder path:",
        #                           value = "/mnt/nas/Projects/CertAIn/AVC_data_labelling/sam_masked_images")
        """num_images = st.number_input("Number of images: ",
                                     min_value=0,
                                     max_value=10000,
                                     value = 3000, 
                                     step=1,
                                     format="%d")"""
        #dest_images_root_path = st.text_area("dest folder path: ", 
        #                            "/mnt/nas/Projects/CertAIn/AVC_data_labelling/classified_images")
        
        
        st.sidebar.markdown("---")

            

        return st.session_state.selected_path_1, st.session_state.selected_path_2