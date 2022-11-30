

# from bokeh.plotting import figure

# from bokeh.models import GeoJSONDataSource
# from bokeh.models import ColumnDataSource, MultiLine

# from bokeh.tile_providers import ESRI_IMAGERY, get_provider

import geopandas as gpd
import leafmap.foliumap as leafmap

import streamlit as st
import shapely

# File 
from os import listdir, makedirs, remove, rmdir, path
from os.path import isfile, join, exists

st.set_page_config(
    page_icon="streamlit_app\logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    page_title ="About MCDA Prototype"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

data = st.file_uploader('Upload geojson data', accept_multiple_files=False, type = "Geojson")


if data != None:
    with open(path.join(f"user_data/{data.name}"),"wb") as f:
        # Could also delete existing files.
         f.write(data.getbuffer())

