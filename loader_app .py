"""
Museum XML Loader & Transformer (Streamlit app)
------------------------------------------------
Fulfils the project requirement:
"Write a Python or Java program to load an XML file, parse it, validate it
against the XML schema and apply an XSL stylesheet (using XML APIs)."

Parsing and XSLT use lxml (libxml2/libxslt bindings).
Validation uses the 'xmlschema' library instead of lxml's built-in XSD
support, because this project's schema uses <xs:assert> rules, which are an
XSD 1.1 feature. lxml (via libxml2) only implements XSD 1.0 and does not
recognise <xs:assert> at all. 'xmlschema' is a pure-Python library with full
XSD 1.1 support, so it can actually evaluate those assertions.

How to run:
1. Install dependencies:
       pip install streamlit lxml xmlschema
2. Save this file as loader_app.py
3. Run:
       streamlit run loader_app.py
4. Your browser opens automatically at http://localhost:8501
5. Upload your XML file, your XSD schema, and an XSL stylesheet, then click
   "Run pipeline".
"""

import io

import streamlit as st
import xmlschema
from lxml import etree

st.set_page_config(page_title="Museum XML Loader", layout="wide")
st.title("Museum XML Loader & Transformer")
st.write(
    "Loads an XML file, validates it against an XSD schema, then applies an "
    "XSL stylesheet - the three required steps for the Data Pipeline project."
)

# --- File uploaders -----------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    xml_file = st.file_uploader("1. XML data file", type=["xml"])
with col2:
    xsd_file = st.file_uploader("2. XSD schema file", type=["xsd"])
with col3:
    xsl_file = st.file_uploader("3. XSL stylesheet", type=["xsl", "xslt"])

run = st.button("Run pipeline", type="primary", disabled=not (xml_file and xsd_file and xsl_file))

if run:
    # --- Step 1: Parse the XML -------------------------------------------
    st.header("Step 1 - Parse XML")
    try:
        xml_bytes = xml_file.read()
        xml_doc = etree.fromstring(xml_bytes)
        st.success(f"Parsed successfully. Root element: <{xml_doc.tag}>")
    except etree.XMLSyntaxError as e:
        st.error(f"XML is not well-formed: {e}")
        st.stop()

    # --- Step 2: Validate against the XSD ---------------------------------
    # Uses xmlschema (not lxml) because it supports XSD 1.1 <xs:assert> rules.
    st.header("Step 2 - Validate against XSD")
    try:
        xsd_bytes = xsd_file.read()
        schema = xmlschema.XMLSchema11(io.BytesIO(xsd_bytes))
    except xmlschema.XMLSchemaException as e:
        st.error(f"The XSD schema itself could not be parsed: {e}")
        st.stop()

    errors = list(schema.iter_errors(io.BytesIO(xml_bytes)))
    if not errors:
        st.success("Valid against the schema (XSD 1.1, including <xs:assert> rules).")
    else:
        st.error(f"NOT valid against the schema. {len(errors)} error(s) found:")
        for err in errors:
            location = f"element <{err.elem.tag}>" if err.elem is not None else "document"
            st.write(f"- {location}: {err.reason}")
        st.stop()

    # --- Step 3: Apply the XSLT stylesheet --------------------------------
    st.header("Step 3 - Apply XSL stylesheet")
    try:
        xsl_bytes = xsl_file.read()
        xsl_doc = etree.fromstring(xsl_bytes)
        transform = etree.XSLT(xsl_doc)
        result = transform(xml_doc)
        output_text = str(result)

        st.success("Transformation complete.")

        # Try to guess a sensible language for the code viewer / file
        # extension based on the xsl:output method declared in the stylesheet.
        output_method = xsl_doc.xpath(
            "string(//*[local-name()='output']/@method)"
        ) or "xml"
        lang_map = {"html": "html", "text": "text", "xml": "xml"}
        display_lang = lang_map.get(output_method, "text")
        ext_map = {"html": "html", "text": "txt", "xml": "xml"}
        out_ext = ext_map.get(output_method, "txt")

        st.code(output_text, language=display_lang)

        st.download_button(
            label=f"Download result (.{out_ext})",
            data=output_text,
            file_name=f"transform_output.{out_ext}",
            mime="text/plain",
        )

        if transform.error_log:
            with st.expander("Transformation messages / warnings"):
                for entry in transform.error_log:
                    st.write(f"- {entry.message}")

    except etree.XSLTParseError as e:
        st.error(f"The XSL stylesheet could not be parsed: {e}")
    except etree.XSLTApplyError as e:
        st.error(f"Error while applying the stylesheet: {e}")

st.divider()
st.caption(
    "Built with lxml (libxml2 / libxslt bindings) for parsing and XSLT "
    "transformation, and xmlschema for XSD 1.1 validation (needed for "
    "<xs:assert> support) - genuine XML APIs covering all three required "
    "steps."
)
