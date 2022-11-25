
import ast
import streamlit as st
import leafmap.foliumap as leafmap
from csv import writer
from owslib.wms import WebMapService
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

def push_to_storage(url, name, layers, legend, bbox):
    list = [url, name, layers, legend, bbox]
    with open('storage.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()

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
    height = 800
    layers = None

    with row1_col2:
        with st.form("My form", clear_on_submit=True):
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

            name = st.text_input(
                "Add a name to this layer", value=""
            )

            if option:
                options = get_layers(option)

                default = None
                layers = empty.multiselect(
                    "Select WMS layers to add to the map:", options, default=default
                )
                add_legend = st.checkbox("Add a legend to the map", value=True)
                legend = ""



                legend_text = st.text_area(
                    "Enter a legend to this",
                    value=legend,
                    height=200,
                    key="text")

                color = st.color_picker("Pick a color", "#FF0000")
                st.write("The color is", color)

                wms = WebMapService(option)
                bbox = []
                if len(layers)>0:
                    bbox = wms[layers[0]].boundingBoxWGS84

                legend_dict = {legend_text : color}

                submitted = st.form_submit_button("Submit")
                if submitted:
                    push_to_storage(option, name,layers,legend_dict, bbox)

        with row1_col1:
            m = leafmap.Map(center=(40.3, 9.5), zoom=9)

            if layers is not None:
                for layer in layers:
                    m.add_wms_layer(
                        option, layers=layer, name=layer, attribution=" ", transparent=True)
                    st.write(option, layer)

            if add_legend and legend_text:

                m.add_legend(legend_dict=legend_dict)

            m.to_streamlit(height=height)


app()
