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
import shapely.wkt
import json
import ast


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


layers_overview_total = {}

if site_ok:

    # Here the site is handeled, and potentially center point extracted. 
    site = gpd.read_file("user_data/input_site/site.geojson")
    site_center = site.centroid 

    # st.write(site_center)

    # Here any logic for limiting the available layers should be placed



    # HERE CHECKS THE STORAGE WRT BBOX AND SITE 


    files = ["storage.csv", "storage_user_added.csv"]

    with open('storage.csv', mode='r') as csv_file_temp:
        storage = csv.reader(csv_file_temp)
        for option in storage:

            # Here check the BBOX wrt. the center of the site.
            # st.write(file_params)
            polygon = shapely.wkt.loads(option[3])

            for center in site_center:
                # Converting string to list
                if polygon.contains(center):
                    # st.write(polygon)

                    # Adds the WMS to the layers overview total
                    layers_overview_total[option[1]] = {}
                    layers_overview_total[option[1]]["option"] = option
                    layers_overview_total[option[1]]["type"] = "WMS" # Other alternatives == TIFF, GEOJSON, etc.
                    layers_overview_total[option[1]]["activated"] = False

                    break

            

            
    # HERE CHECKS THE USERSTORAGE WRT BBOX AND SITE

    ##We have wms layers and other uploaded layers, maybe also osm layers

with st.sidebar:
    # hacky solution for the main() as it does not support sidebar
    if __name__ == "__main__":

        st.info("Here the available datalayers and data for the area of interest is displayed.")
        st.write("Here could the active layers and legend be displayed.")

        with st.form("MapView data"):


            st.header("Data Catalogue")
            st.subheader("User Uploaded data")
            # Here itterate through User data

            st.write("here comes user uploaded data w. legend")


            st.subheader("Enernite data catalogue")

            if layers_overview_total == {}:
                st.write("No data found for given AOI.")

            # layers_overview_total could be sorted by category?

            with st.expander("Environmental data"):
                for layer in layers_overview_total:

                    # Here some folder structure could be added

                    st.write("Add the layer with tag: ", str(layer).strip("']["))
                    option = layers_overview_total[layer]["option"]

                    
                    agree_submit_bool = st.checkbox("Activate layer in view", key = option)

                    layers_overview_total[option[1]]["activated"] = agree_submit_bool

                    st.markdown("---")

            with st.expander("Technical data"):

                st.write("TBD")

            with st.expander("Regional Plans / Georeferenced PDFs"):

                st.write("TBD")
            submitted_view = st.form_submit_button("Genereate view")


if not submitted_view:
    Map = leafmap.Map(center=(40.3, 9.5), zoom=9)

    Map.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
    name="Google Satellite",
    attribution="Google",
    )

    Map.to_streamlit(height=800)



if submitted_view:

    Map = leafmap.Map(center=(40.3, 9.5), zoom=9)

    Map.add_tile_layer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        name="Google Satellite",
        attribution="Google",
    )


    # Here logic for adding the different layers, WMS and User data to the map should be implemented.

    if layers_overview_total is not None:
        for layer in layers_overview_total:
            if layers_overview_total[layer]["activated"]:
                option = layers_overview_total[layer]["option"]
                url = option[0]
                layers = np.array(option[1].strip('][').split(', ')).astype(str)
                legend_dict = ast.literal_eval(option[2])
                for layer in layers:
                    layer=layer[1:-1]
                    # st.write(layer)
                    Map.add_wms_layer(
                        url=url, layers=layer, name=layer, attribution="", transparent=True)
                Map.add_legend(legend_dict=legend_dict)
        
    Map.to_streamlit(height=800)


