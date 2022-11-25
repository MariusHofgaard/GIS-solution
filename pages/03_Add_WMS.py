
import ast
import streamlit as st
import leafmap.foliumap as leafmap
from csv import writer
import json
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

def push_to_storage(url, layers, legend):
    list = [url, layers, ast.literal_eval(legend)]
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

        # kwargs = st.text_input("Enter kwargs as list (, as separator):", value="")
        # st.write(kwargs)


        # split_list = kwargs.split(",")

        # dict_kwargs = {}
        # for i, key in enumerate(split_list):
        #     if i%2 == 0:
        #         continue
            

        #     print(key)

        # st.write(split_list)
        empty = st.empty()

        if option:
            options = get_layers(option)

            default = None
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            add_legend = st.checkbox("Add a legend to the map", value=True)
            legend = ""

            legend_text = st.text_area(
                "Enter a legend as a dictionary {label: color}",
                value=legend,
                height=200,
                key="text")

            def clear_text():
                st.session_state["text"] = ""

            legend = legend_text
            if st.button("Push to storage"):
                push_to_storage(option,layers,legend)

        with row1_col1:
            m = leafmap.Map(center=(40.3, 9.5), zoom=9)

            if layers is not None:
                for layer in layers:
                    m.add_wms_layer(
                        option, layers=layer, name=layer, attribution=" ", transparent=True)
                    st.write(option, layer)

            if add_legend and legend_text:
                legend_dict = ast.literal_eval(legend_text)

                m.add_legend(legend_dict=legend_dict)

            m.to_streamlit(height=height)


app()
