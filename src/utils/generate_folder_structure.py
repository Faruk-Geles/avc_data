import os 
import numpy as np 

import os
import tempfile




class GenerateFolderStructure:
    
    def __init__(self):
        #self.root_folder = root_folder
        pass
        
    def safe_output_folder(self, subfolder="classified_images"):
        base = "/mnt/nas/Projects/CertAIn/AVC_data_labelling"
        path = os.path.join(base, subfolder)
        os.makedirs(path, exist_ok=True)
        return path
    
    def generate_folders(self): 
        #folder_path = self.root_folder #os.path.join(self.root_folder, folder_name)
        #if not os.path.exists(self.root_folder):
        #    os.makedirs(self.root_folder)
              
        #classified_images_path = self.root_folder #os.path.join(folder_path, "classified_images")
        #if not os.path.exists(classified_images_path):
        #    os.makedirs(classified_images_path)
        classified_images_path = self.safe_output_folder("classified_images")
        
        
        hard_plast = os.path.join(classified_images_path, "hard_plast")
        wood = os.path.join(classified_images_path, "wood")
        treated_wood = os.path.join(classified_images_path, "treated_wood")
        
        betong = os.path.join(classified_images_path, "betong")
        energy_recovery = os.path.join(classified_images_path, "energy_recovery")
        non_combustible = os.path.join(classified_images_path, "non_combustible")
        
        metall = os.path.join(classified_images_path, "metall")
        well_papp = os.path.join(classified_images_path, "well_papp")
        paper_packaging = os.path.join(classified_images_path, "paper_packaging")
        
        plastic_packaging = os.path.join(classified_images_path, "plastic_packaging")
        isolering = os.path.join(classified_images_path, "isolering")
        wee = os.path.join(classified_images_path, "wee")
        
        os.makedirs(hard_plast, exist_ok=True)
        os.makedirs(wood, exist_ok=True)
        os.makedirs(treated_wood, exist_ok=True)
        
        os.makedirs(betong, exist_ok=True)
        os.makedirs(energy_recovery, exist_ok=True)
        os.makedirs(non_combustible, exist_ok=True)
        
        os.makedirs(metall, exist_ok=True)
        os.makedirs(well_papp, exist_ok=True)
        os.makedirs(paper_packaging, exist_ok=True)
        
        os.makedirs(plastic_packaging, exist_ok=True)
        os.makedirs(isolering, exist_ok=True)
        os.makedirs(wee, exist_ok=True)
       
            
            
               


    
    