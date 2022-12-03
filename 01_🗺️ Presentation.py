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
import glob
import os


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

    ##Adding some OSM layers:

    osm_tags = [{"tags" : {"power" : "plant"},
                "layer_name": "Power plants",
                "style": {"color": "#FF0000"}},
                {"tags" : {"power" : "line"},
                "layer_name": "Grid",
                "style": {"color": "#FFFF00"}},
                {"tags" : {"power" : "substation"},
                "layer_name": "Substations",
                "style": {"color": "#000000"}},
                {"tags" : {"highway" : True},
                "layer_name": "Roads",
                "style": {"color": "#000000"}},
                {"tags" : {"natural" : "Water"},
                "layer_name": "Water",
                "style": {"color": "#0000FF"}},
                {"tags" : {"landuse": True},
                "layer_name": "Landuse",
                "style": {"color": "#00FF4D"}}]

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

def format_func(option):
    return str(layers_overview_total[option]["option"][2]).split(":")[0].strip("']{[")

def format_func_osm(option):
    return option["layer_name"]

def format_func_user(option):
    return option.split(".")[0]

with st.sidebar:
    # hacky solution for the main() as it does not support sidebar
    if __name__ == "__main__":

        st.info("Here the available datalayers and data for the area of interest is displayed.")
        st.write("Here could the active layers and legend be displayed.")

        with st.form("MapView data"):
            st.header("Data Catalogue")
            st.subheader("User Uploaded data")
            # Here itterate through User data

            data_names = (file for file in os.listdir("user_data") if os.path.isfile(os.path.join("user_data", file)))
            user_options = st.multiselect(
                    "Choose the data layers you want to see",
                    data_names,
                    format_func=format_func_user
            )


            st.subheader("Enernite data catalogue")

            if layers_overview_total == {}:
                st.write("No data found for given AOI.")

            # layers_overview_total could be sorted by category?

            with st.expander("Environmental data"):
                #Just testing multiselect
                env_options = st.multiselect(
                    "Choose the data layers you want to see",
                    layers_overview_total,
                    format_func=format_func
                )
                # for layer in layers_overview_total:

                #     # Here some folder structure could be added


                #     option = layers_overview_total[layer]["option"]
                #     st.write("Add the layer with labelname: ", str(option[2]).split(":")[0].strip("']{["))
                    
                #     agree_submit_bool = st.checkbox("Activate layer in view", key = option)

                #     layers_overview_total[option[1]]["activated"] = agree_submit_bool

                #     st.markdown("---")

            with st.expander("Technical data"):

                st.write("TBD")

            with st.expander("Regional Plans / Georeferenced PDFs"):
                st.write("**EXAMPLE**")

                germany = st.checkbox("Add Wind plan from Germany (EXAMPLE)")

            with st.expander("OSM data"):
                osm_options = st.multiselect(
                    "Choose the data layers you want to see",
                    osm_tags,
                    format_func=format_func_osm
                )
                # for osm in range(len(osm_tags)):
                #     option = osm_tags[osm]["layer_name"]
                #     st.write("Add the layer with labelname: ", option)
                    
                #     agree_submit_bool = st.checkbox("Activate layer in view", key = option)

                #     osm_tags[osm]["activated"] = agree_submit_bool
            submitted_view = st.form_submit_button("Genereate view")

if not submitted_view:
    Map = leafmap.Map(center=(40.3, 9.5), zoom=9)

    Map.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
    name="Google Satellite",
    attribution="Google",
    )

    Map.to_streamlit(height=800, width=800)



if submitted_view:
    Map = leafmap.Map(zoom=9)


    if site_ok:
        
        site = gpd.read_file("user_data/input_site/site.geojson")
        centroid = site.unary_union.centroid
        y, x = centroid.y, centroid.x

        Map = leafmap.Map(center = (x,y),zoom=9)

        Map.add_gdf(site, layer_name="User Uploaded Site",style={"color": "#0000FF"})

    Map.add_tile_layer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        name="Google Satellite",
        attribution="Google",
    )

    if germany:
        Map.add_raster(source="/Applications/Enernite/programs/GIS-solution/gpkg/kSOAjX7OjtoiF8eMR_4w0ATxIWjbk9iMndXjp3ulSdE.gpkg")



    legend_dict={"Site": "#0000FF"}
    # Here logic for adding the different layers, WMS and User data to the map should be implemented.

    #Another approach based on the multiselect:
    if len(env_options)>0:
        for layer in env_options:
            option = layers_overview_total[layer]["option"]
            url = option[0]
            layers = np.array(option[1].strip('][').split(', ')).astype(str)
            dict = ast.literal_eval(option[2])
            legend_dict.update(dict)
            for layer in layers:
                layer=layer[1:-1]
                Map.add_wms_layer(
                    url=url, layers=layer, name=layer, attribution="", transparent=True)

    if len(osm_options)>0:
        for osm in osm_options:
            try:
                Map.add_osm_from_point(center_point=(y,x),
                                        dist=5000,
                                        tags=osm["tags"],
                                        layer_name=osm["layer_name"],
                                        style=osm["style"])

                legend_dict[osm["layer_name"]] = osm["style"]["color"]
            except:
                st.write("Found no elements with tag {} inside an area of 5km radius".format(osm["layer_name"]))

    if len(user_options)>0:
        for user in user_options:
            layer_name = user.split(".")[0]
            Map.add_geojson(in_geojson=os.path.join("user_data", user),
                            layer_name=layer_name)



    # if layers_overview_total is not None:
    #     for layer in layers_overview_total:
    #         if layers_overview_total[layer]["activated"]:
    #             option = layers_overview_total[layer]["option"]
    #             url = option[0]
    #             layers = np.array(option[1].strip('][').split(', ')).astype(str)
    #             dict = ast.literal_eval(option[2])
    #             legend_dict.update(dict)
    #             for layer in layers:
    #                 layer=layer[1:-1]
    #                 Map.add_wms_layer(
    #                     url=url, layers=layer, name=layer, attribution="", transparent=True)
    
    # for osm in osm_tags:
    #     if osm["activated"]:
    #         Map.add_osm_from_point(center_point=(lat,lon),
    #                                 dist=5000,
    #                                 tags=osm["tags"],
    #                                 layer_name=osm["layer_name"],
    #                                 style=osm["style"])

    #         legend_dict[osm["layer_name"]] = osm["style"]["color"]

    Map.add_legend(legend_dict=legend_dict)

    Map.to_streamlit(height=800, width=800)

    Map.to_html("WMS_presentation_example.html")

