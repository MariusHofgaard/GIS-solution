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

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import json
import ast


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

isExist = exists(r"user_data/input_site/site2.geojson")

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



with st.sidebar:
    
    st.info("Here the available datalayers and data for the area of interest is displayed.")

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


        submitted_view = st.form_submit_button("Genereate view")


def main(): 
    # Here the main part of the streamlit page is handeled

    # Here the site is handeled, and potentially center point extracted. 
    site = gpd.read_file("user_data/input_site/site2.geojson")
    site_center = site.centroid 

    st.write(site_center)



    # Here any logic for limiting the available layers should be placed

    all_wms_layers = []
    all_uploaded_layers = []
    all_user_uploaded_layers = []

    # HERE CHECKS THE STORAGE WRT BBOX AND SITE 


    files = ["storage.csv", "storage_user_added.csv"]


    with open('storage.csv', mode='r') as csv_file_temp:
        storage = csv.reader(csv_file_temp)
        for file_params in storage:

            # Here check the BBOX wrt. the center of the site.
            st.write(file_params)
            file_params[3] = np.array(file_params[3].strip(')(').split(', ')).astype(float)

            for center in site_center:
                # Converting string to list

                polygon = shapely.geometry.box(*file_params[3])
                if polygon.contains(center):
                    st.write(polygon)
                    all_wms_layers.append(file_params)
                    break

            
    # HERE CHECKS THE USERSTORAGE WRT BBOX AND SITE

    ##We have wms layers and other uploaded layers, maybe also osm layers


    if submitted_view:


        Map = leafmap.Map(center=(40.3, 9.5), zoom=9)

        Map.add_tile_layer(
            url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            name="Google Satellite",
            attribution="Google",
        )

        # Here logic for adding the different layers, WMS and User data to the map should be implemented.

        if all_wms_layers is not None:
            for option in all_wms_layers:
                url = option[0]
                layers = np.array(option[1].strip('][').split(', ')).astype(str)
                legend_dict = ast.literal_eval(option[2])
                for layer in layers:
                    layer=layer[1:-1]
                    st.write(layer)
                    Map.add_wms_layer(
                        url=url, layers=layer, name=layer, attribution="", transparent=True)
                Map.add_legend(legend_dict=legend_dict)
         
        Map.to_streamlit(height=800)


if site_ok:
    print("yes")
    main() 
