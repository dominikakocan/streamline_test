"""docuscan streamlit app."""
import streamlit as st
from io import StringIO, BytesIO
import pandas as pd
from PIL import ImageOps
import pypdfium2 as pdfium


st.set_page_config(layout="wide")

def visualize_pagination(images, key = 'original'):
    placeholder = st.empty()
    bottom_menu = st.columns((4, 1))
    with bottom_menu[1]:
        total_pages = len(images) if isinstance(images, list) else 1
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1, key = key)
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")
    with placeholder:
        try:
            st.image(images[current_page - 1])
        except TypeError:
            st.image(images)


def show_original(placeholder):
    placeholder.image(st.session_state.images[st.session_state.current_page - 1])

def show_signatures(placeholder):
    placeholder.image(st.session_state.images_sign[st.session_state.current_page_sign - 1])

def show_tables(placeholder):
    placeholder.image(st.session_state.images_tab[st.session_state.current_page_tab - 1])   

uploaded_file = st.file_uploader("Please load a file",accept_multiple_files=False,type=["pdf","png","jpg"])

if "global_dict" not in st.session_state:
    st.session_state.global_dict = None
if uploaded_file is not None:
    check = st.radio("Select operation mode:",["One-page document","Multi-page document"])
    if check:
        if uploaded_file.type == "application/pdf":
            bytes_data = uploaded_file.getvalue()
            decoded_string = bytes_data.decode("latin-1")
            document_pdf = pdfium.PdfDocument(bytes_data)
            num_pages = len(document_pdf)
            pages = [document_pdf.get_page(i) for i in range(num_pages)]
            images = [page.render(scale = 300/72).to_pil() for page in pages]
        else:
            image = ImageOps.Image.open(BytesIO(bytes_data))
            images = [ImageOps.exif_transpose(image)]

        if 'images' not in st.session_state:
            st.session_state.images = images

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            placeholder1 = st.empty()
            with placeholder1.container():
                bottom_menu1 = st.columns((4, 1))
                placeholder_image1 = st.empty()
                with placeholder_image1:
                    st.image(images[0])
                with bottom_menu1[1]:
                    total_pages1 = len(images) if isinstance(images, list) else 1
                    current_page1 = st.number_input(label = "Page", 
                                                    min_value = 1, 
                                                    max_value = total_pages1, 
                                                    step = 1, 
                                                    key = 'current_page',
                                                    on_change=show_original,
                                                    args = (placeholder_image1, ))
                with bottom_menu1[0]:
                    st.markdown(f"Page **{current_page1}** of **{total_pages1}** ")
        with col2:
            tab1,tab2,tab3 = st.tabs(["Raw text","Tables","Signatures"])
            with tab1:
                pass
            with tab2:
                images_tables = images
                st.session_state.images_tab = images_tables

                visualize_button = st.button("Visualize table")
                if visualize_button:
                    placeholder2 = st.empty()
                    with placeholder2.container():
                        bottom_menu2 = st.columns((4, 1))
                        placeholder_image2 = st.empty()
                        with placeholder_image2:
                            st.image(images_tables[0])
                        with bottom_menu2[1]:
                            total_pages2 = len(images_tables) if isinstance(images_tables, list) else 1
                            current_page2 = st.number_input(label = "Page", 
                                                            min_value=1, 
                                                            max_value=total_pages2, 
                                                            step=1, 
                                                            key = 'current_page_tab', 
                                                            on_change=show_tables,
                                                            args = (placeholder_image2, ))
                        with bottom_menu2[0]:
                            st.markdown(f"Page **{current_page2}** of **{total_pages2}** ")
            with tab3:                   
                images_signatures = images
                st.session_state.images_sign = images_signatures
                visualize_button = st.button("Visualize signatures")
                if visualize_button:
                    placeholder3 = st.empty()
                    with placeholder3.container():
                        bottom_menu3 = st.columns((4, 1))
                        placeholder_image3 = st.empty()
                        with placeholder_image3:
                            st.image(images_signatures[0])
                        with bottom_menu2[1]:
                            total_pages3 = len(images_signatures) if isinstance(images_signatures, list) else 1
                            current_page3 = st.number_input(label = "Page", 
                                                            min_value=1, 
                                                            max_value=total_pages3, 
                                                            step=1, 
                                                            key = 'current_page_sign', 
                                                            on_change=show_signatures,
                                                            args = (placeholder_image3, ))
                        with bottom_menu2[0]:
                            st.markdown(f"Page **{current_page3}** of **{total_pages3}** ")
