import os 
import numpy as np 

import os
import tempfile




class GenerateFolderStructure:
    
    def __init__(self, root_folder):
        self.root_folder = root_folder
        pass
    
    def generate_folders(self): 
        #folder_path = self.root_folder #os.path.join(self.root_folder, folder_name)
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
              
        classified_images_path = self.root_folder #os.path.join(folder_path, "classified_images")
        #if not os.path.exists(classified_images_path):
        #    os.makedirs(classified_images_path)
        trägårdsavfall = os.path.join(classified_images_path, "Trädgårdsavfall")
        trä = os.path.join(classified_images_path, "Trä") 
        ej_återvinningsbart = os.path.join(classified_images_path, "Ej återvinninsbart")
        metall = os.path.join(classified_images_path, "Metall") 
        sten_betong = os.path.join(classified_images_path, "Sten-Betong")
        wellpapp = os.path.join(classified_images_path, "Wellpapp")
        ris_grenar = os.path.join(classified_images_path, "Ris-Grenar")
        impregnerat_trä = os.path.join(classified_images_path, "Impregnerat trä")
        gibs = os.path.join(classified_images_path, "Gips")
        energieåtervinning = os.path.join(classified_images_path, "Energieåtervinning")
        jord = os.path.join(classified_images_path, "Jord")
        däck_med_fälg = os.path.join(classified_images_path, "Däck med Fälg")
        däck = os.path.join(classified_images_path, "Däck")
        asbest = os.path.join(classified_images_path, "Asbest")
        fönster = os.path.join(classified_images_path, "Fönster")
        stoppade_möbler = os.path.join(classified_images_path, "Stoppade Möbler")
        hårdplast = os.path.join(classified_images_path, "Hårdplast")
        återbruk = os.path.join(classified_images_path, "Återbruk")
        fallfrukt = os.path.join(classified_images_path, "Fallfrukt")
        elektronik = os.path.join(classified_images_path, "Elektronik")
        farligt_avfall = os.path.join(classified_images_path, "Farligt Avfall")
        textil = os.path.join(classified_images_path, "Textil")
        böcker = os.path.join(classified_images_path, "Böcker")
        lastpall = os.path.join(classified_images_path, "Lastpall")
        glasförpackningar = os.path.join(classified_images_path, "Glasförpackningar")
        invasiva_väster = os.path.join(classified_images_path, "Invasiva växter")
        jord_invasiva_väster = os.path.join(classified_images_path, "Jord med invasiva väster")
        metallförpackningar = os.path.join(classified_images_path, "Metallförpackningar")
        mjukplast = os.path.join(classified_images_path, "Mjukplast")
        pappersförpackningar = os.path.join(classified_images_path, "Pappersförpackningar")
        plastvörpackningar = os.path.join(classified_images_path, "Plastförpackningar")
        tidningar = os.path.join(classified_images_path, "Tidningar")
          
        full_soppsäck = os.path.join(classified_images_path, "full soppsäck")
        tomp_soppsäck = os.path.join(classified_images_path, "tomp soppsäck")
        oidentifiered = os.path.join(classified_images_path, "oidentifiered")
        
        
        
        
    
        os.makedirs(trägårdsavfall, exist_ok=True)
        os.makedirs(trä, exist_ok=True)
        os.makedirs(ej_återvinningsbart, exist_ok=True)
        os.makedirs(metall, exist_ok=True)
        os.makedirs(sten_betong, exist_ok=True)
        
        os.makedirs(wellpapp, exist_ok=True)
        os.makedirs(ris_grenar, exist_ok=True)
        os.makedirs(impregnerat_trä, exist_ok=True)
        os.makedirs(gibs, exist_ok=True)
        os.makedirs(energieåtervinning, exist_ok=True)
        
        os.makedirs(jord, exist_ok=True)
        os.makedirs(däck_med_fälg, exist_ok=True)
        os.makedirs(däck, exist_ok=True)
        os.makedirs(asbest, exist_ok=True)
        os.makedirs(fönster, exist_ok=True)
        
        os.makedirs(stoppade_möbler, exist_ok=True)
        os.makedirs(hårdplast, exist_ok=True)
        os.makedirs(återbruk, exist_ok=True)
        os.makedirs(fallfrukt, exist_ok=True)
        os.makedirs(elektronik, exist_ok=True)
        
        os.makedirs(farligt_avfall, exist_ok=True)
        os.makedirs(textil, exist_ok=True)
        os.makedirs(böcker, exist_ok=True)
        os.makedirs(lastpall, exist_ok=True)
        os.makedirs(glasförpackningar, exist_ok=True)
        
        os.makedirs(invasiva_väster, exist_ok=True)
        os.makedirs(jord_invasiva_väster, exist_ok=True)
        os.makedirs(metallförpackningar, exist_ok=True)
        os.makedirs(mjukplast, exist_ok=True)
        os.makedirs(pappersförpackningar, exist_ok=True)
        
        os.makedirs(plastvörpackningar, exist_ok=True)
        os.makedirs(tidningar, exist_ok=True)
        
        os.makedirs(oidentifiered, exist_ok=True)
        os.makedirs(full_soppsäck, exist_ok=True)
        os.makedirs(tomp_soppsäck, exist_ok=True)
  
       
            
            
               


    
    