#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 08:12:45 2018

@author: ross.winans@gmail.com

This script will sift through a directory of .jpg images and look for images that are all 0s. If these images are found,
they are copied to a new directory (.../nodata) and the original is deleted.
"""

from os import walk, path, remove
from shutil import copy

import rasterio as rio
import numpy as np

in_dir = r"/media/ross/Data/02_data/DAR_Coastal_2015/hawaii"
out_dir = path.join(in_dir, "nodata")

for root, dirs, files in walk(path.join(in_dir, "retile")):
    for fi in files:
        if fi.endswith('.jpg'):
            print("working on: ", fi)
            in_path = path.join(root, fi)
            aux_in_path = in_path + ".aux.xml"
            
            out_path = path.join(out_dir, fi)
            aux_out_path = out_path + ".aux.xml"
            
            with rio.open(in_path, 'r') as img:
                band1 = img.read(1)
                band2 = img.read(2)
                band3 = img.read(3)
                
                zeros = np.zeros_like(band1)
                
                if np.array_equal(band1, zeros) and np.array_equal(band2, zeros) and np.array_equal(band3, zeros):
                    print(fi, "is most likely nodata.")
                    
                    if not path.exists(out_path) or not path.exists(aux_out_path):
                        print(fi, "is not in the no data folder. Copying...")
                        copy(in_path, out_path)
                        copy(aux_in_path, aux_out_path)
                    else:
                        print("{0} exists. Removing the data in the nodata folder and trying again.".format(fi))
                        remove(out_path)
                        remove(aux_out_path)
                        
                        copy(in_path, out_path)
                        copy(aux_in_path, aux_out_path)
                    
                    if path.exists(out_path) and path.exists(aux_out_path):
                        print("{0} exists in the no data folder. Deleting original... SUCCESS".format(fi))
                        remove(in_path)
                        remove(aux_in_path)
                    else:
                        print("{0} does not exist in the nodata folder. Cannot delete the original...PROBLEM?".format(fi))
                    
                else:
                    print(fi, "is most likely valid.")
