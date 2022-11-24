

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



isExist = exists(r"streamlit_app\input_site\area.geojson")

if isExist:
    st.write('Existing site found. Upload new site to re-define area of focus?')

site = st.file_uploader('Upload a site area to be analyzed', accept_multiple_files=False, type = "Geojson")


if site != None:
    # st.write(type(site))

    # if path.isfile(r"C:\Users\mariu\Documents\visual_studio_projects\streamlit_v2\streamlit_app\input_site\area.geojson"):
    #     remove(r"C:\Users\mariu\Documents\visual_studio_projects\streamlit_v2\streamlit_app\input_site\area.geojson")
    #     st.success('Previous site deleted')

    with open(path.join(r"streamlit_app\input_site\area.geojson"),"wb") as f:
        # Could also delete existing files.
         f.write(site.getbuffer())



if site != None:

    gdf = gpd.read_file(r'streamlit_app/input_site/area.geojson')

    gdf = gdf.set_crs('EPSG:4326')

    minx,miny,maxx,maxy = list(gdf.total_bounds)
    focus_x = (maxx + minx) / 2
    focus_y = (maxy + miny) / 2

    
    Map = leafmap.Map( center = (focus_y,focus_x), zoom=8,
        draw_control=False,
        measure_control=True,
        fullscreen_control=False,
        attribution_control=True,
    )

    Map.add_tile_layer(
        url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        name="Google Satellite",
        attribution="Google",
    )


    Map.add_geojson("streamlit_app/input_site/area.geojson", layer_name="result")
    # Map.add_geojson("points.geojson", layer_name="result") #, style_function=style)


    Map.to_streamlit(height=700)

filenames_definitions_exists = exists(r"streamlit_app\variables_params\file_names.pickle")
if filenames_definitions_exists:
    remove(r"streamlit_app\variables_params\file_names.pickle")
