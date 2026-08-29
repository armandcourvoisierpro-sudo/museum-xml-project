import streamlit as st
from pathlib import Path
from lxml import etree



# Readme of the app
st.set_page_config(
    page_title="Museum XML Pipeline",
    page_icon="🏛️",
    layout="wide"
)

st.title("Museum XML Processing App")

st.markdown(
    """
    This application allows you to:
    - load an XML file,
    - parse it with XML APIs,
    - validate it against the XML schema,
    - apply an XSL stylesheet to transform the data.

    The goal is to process museum XML data from ingestion to validation and transformation in a simple, visual interface.
    """
)

st.caption("XML input → schema validation → XSL transformation")




# Upload section
st.subheader("Upload XML file")

uploaded_file = st.file_uploader(
    "Drag and drop an XML file here",
    type=["xml"],
    help="Upload a museum XML dataset to validate and transform it."
)

if uploaded_file is not None:
    st.success(f"File loaded successfully: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")

    xml_content = uploaded_file.getvalue()
else:
    st.info("Please upload an XML file to continue.")