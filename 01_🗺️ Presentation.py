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
import csv


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

isExist = exists(r"user_data/input_site/site.geojson")

site_ok = True
if not isExist:  
    st.subheader("Note: you must upload a site or AOI to ")
    site_ok = False

    data = st.file_uploader('Upload site data to be analyzed', accept_multiple_files=False, type = "Geojson")
    st.info("Note: Any file format can be integrated.")

    if data != None:
        with open(join(f"user_data/input_site/site.geojson"),"wb") as f:
            # Could also delete existing files.
            f.write(data.getbuffer())
        st.experimental_rerun()
else: 
    submitted = st.button('Reset and delete current site')

    if submitted:
        remove(r"user_data/input_site/site.geojson")
        site_ok = False
        st.experimental_rerun()


def main(): 
    # Here the main part of the streamlit page is handeled

    # Here the site is handeled, and potentially center point extracted. 
    site = gpd.read_file("user_data/input_site/site.geojson")
    site_center = site.centroid 

    st.write(site_center)



    # Here any logic for limiting the available layers should be placed

    all_wms_layers = []
    all_uploaded_layers = []
    all_user_uploaded_layers = []



    with open('storage.csv', mode='r') as csv_file_temp:
        storage = csv.reader(csv_file_temp)
        for file_params in storage:

            # Here check the BBOX wrt. the center of the site.
            st.write(file_params)


    for file_params in storage:

        for center in site_center:
            pass

            # If intersects. break for loop and add to respective list
        
        
    


    with st.sidebar:
        st.write("Here could the active layers and legend be displayed.")

        with st.form("MCDA Scoring Weights"):

            agree = st.checkbox("Activate")
            # This does not run anything fefore "st.form" is submitted.

            st.header("Data Catalogue")

            st.subheader("User Uploaded data")
            # Here itterate through User data

            st.write("here comes user uploaded data w. legend")

            st.subheader("Enernite data catalogue")
            st.write("Here comes enernite data catalogue & WMS.")


            submitted = st.form_submit_button("Genereate view")


    if submitted:


        Map = leafmap.Map(  zoom=10)
        leafmap.tile

        leafmap.TitilerEndpoint

        Map.add_tile_layer(
            url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            name="Google Satellite",
            attribution="Google",
        )

        # Here logic for adding the different layers, WMS and User data to the map should be implemented. 

        Map.to_streamlit(height=800)


if site_ok:
    print("yes")
    main() 
