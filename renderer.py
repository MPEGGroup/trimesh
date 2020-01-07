#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:08:02 2019

@author: Imed Bouazizi
"""

import trimesh
from trimesh.viewer import SceneViewer
import pyglet
import cv2
from os import listdir
from os.path import isfile, join
import numpy as np

pccfiles = [f for f in listdir('content/livingroom/longdress') if isfile(join('content/livingroom/longdress', f)) and f.endswith('.bin')]

vidcap = cv2.VideoCapture('content/livingroom/bbb.mp4')

scene = trimesh.load('content/livingroom/scene.gltf')

frame_pos = 0
ticks = 0

def update(v,s):
    global frame_pos, ticks
    # read next video frame
    success,image = vidcap.read()
    if not success:
        vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
        success,image = vidcap.read()
    
    # set filename for next point cloud    
    if frame_pos >= len(pccfiles):
        frame_pos = 0
    fn = pccfiles[frame_pos]
    
    if v is not None:
        pil_image = pyglet.image.ImageData(image.shape[1], image.shape[0], 'RGB', image.tobytes(), pitch=-image.shape[1]*3)
        v.textures['TV_mesh'] = pil_image.get_texture()

        # render point clouds at lower frequency
        if ticks % 20 == 1:            
            with open('content/livingroom/longdress/'+fn, mode='rb') as file: 
                data = file.read()
                file.close()
                
                count = int(fn.split('_')[-1].replace('.bin',''))                
                length = 16 * count
                
                bufData = np.frombuffer(data[0:length], dtype="<f4")                
                vertices_data = np.lib.stride_tricks.as_strided(bufData, (count,3), (16,4))
                
                bufData = np.frombuffer(data[12:length], dtype="<u1")
                color_data = np.lib.stride_tricks.as_strided(bufData, (count,4), (16,1))                

                s.geometry['PCC_mesh'] = trimesh.PointCloud(vertices_data,colors=color_data)                
        
                frame_pos = frame_pos + 1
    ticks = ticks + 1
    
viewer = SceneViewer(scene,start_loop=True, background=(255,255,255),callback=update,callback_period=0.033)



