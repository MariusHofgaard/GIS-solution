
import ast
import streamlit as st
import leafmap.foliumap as leafmap
from csv import writer
from owslib.wms import WebMapService
from shapely.geometry import Polygon
import shapely
import tempfile
import streamlit.components.v1 as components
import folium


st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info(
    """
    GitHub repository: https://github.com/MariusHofgaard/GIS-solution
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    [Enernite](https://www.enernite.com)
    """
)


@st.cache
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options

def push_to_storage(url, layers, legend, bbox):
    list = [url, layers, legend, bbox]
    with open('storage.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()

def show_plot(plot):
    tmp_output_filename = tempfile.NamedTemporaryFile(suffix='.html').name
    plot.save(tmp_output_filename)

    f = open(tmp_output_filename, "r")
    components.html(f.read(), height=600, width=600)

def app():
    st.title("Web Map Service (WMS)")
    st.markdown(
        """
    This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service 
    in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find 
    some WMS URLs if needed.
    """
    )

    row1_col1, row1_col2 = st.columns([3, 1.3])
    width = 800
    height = 600
    layers = None

    with row1_col2:
        vincoli = "http://vincoliinrete.beniculturali.it/vir/vir/geoserver/wms"
        webgis2 = "http://webgis2.regione.sardegna.it/geoserver/ows"
        sitap = "http://sitap.beniculturali.it:8080/geoserver/apar.public/wms"
        idrogeo = "https://idrogeo.isprambiente.it/geoserver/idrogeo/wms"

        option = st.selectbox(
            "Choose which WMS URL you want to connect to",
            (vincoli, webgis2, sitap, idrogeo)
        )
        
        url = st.text_input(
            "Or write a new WMS URL:", value=""
        )
        if url:
            option=url
        empty = st.empty()


        if option:
            options =  get_layers(option)

            default = None
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            add_legend = st.checkbox("Add a legend to the map", value=True)
            legend = ""

            legend_text = st.text_input(
                "Add a name to this layer", value=""
            )

            color = st.color_picker("Pick a color", "#FF0000")
            st.write("The color is", color)

            wms = WebMapService(option)
            bbox = []
            if len(layers)>0:
                bbox = wms[layers[0]].boundingBoxWGS84
                bbox = shapely.geometry.box(*bbox[3])

            legend_dict = {legend_text : color}

            submitted = st.button("Submit", on_click=push_to_storage, args=(option, layers,legend_dict, bbox))
            if submitted:
                st.experimental_rerun()

        with row1_col1:
            m = leafmap.Map(center=(40.3,9.5), zoom=9)

            if layers is not None:
                for layer in layers:
                    m.add_wms_layer(
                        option, layers=layer, name=layer, attribution=" ", transparent=True)
                    st.write(option, layer)

            if add_legend and legend_text:

                m.add_legend(legend_dict=legend_dict)
               

            ## Check if we can add mbiles
            #m.add_tile_layer(url="http://{s}localhost:8988/test/{z}/{x}/{y}.png", name="tiles_test", attribution="Egeli")
            #m.add_layer(tile_layer)
            m.add_tile_layer(url="http://localhost:8080/services/tiles_test/tiles/{z}/{x}/{y}.png", name="tiles_test", attribution="Egeli", kwargs={"tms":"True"})
            #show_plot(m)
            m.to_streamlit(height=height)


app()
