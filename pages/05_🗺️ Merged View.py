# from ossaudiodev import control_names
from re import S, sub
from tkinter import CENTER
import streamlit as st
import geopandas as gpd

import leafmap.foliumap as leafmap


# File 
from os import listdir, makedirs, remove, rmdir
from os.path import isfile, join, exists

import shapely
import numpy as np 
import random
from branca.colormap import linear

import pickle


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 





Map = leafmap.Map(  zoom=10,
            draw_control=False,
            measure_control=False,
            fullscreen_control=True,
            attribution_control=True,
        )

Map.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
    name="Google Satellite",
    attribution="Google",
)




# Map.add_raster("/Applications/Enernite/programs/streamlit_app_MCDA/input_layer/EGY_wind-speed_150m.tif",palette="terrain",layer_name = "Wind Speeds 150m")
# Map.add_raster("/Applications/Enernite/programs/streamlit_app_MCDA/input_layer/EGY_elevation_w_bathymetry.tif",palette="terrain",layer_name = "Elevation",kwargs={"show":False})
# Map.add_raster("/Applications/Enernite/programs/streamlit_app_MCDA/input_layer/streamlit_app/input_layer/population_data_egypt_2020.tif",layer_name = "Population",kwargs={"show":False})


with st.sidebar:

    with st.form("MCDA Scoring Weights"):

        agree = st.checkbox("Activate")

        st.form_submit_button("Genereate view")


if agree:
    Map.to_streamlit(height=800)
