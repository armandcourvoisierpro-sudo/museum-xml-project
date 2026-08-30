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



BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "XSLT" / "schema.xsd"

def parse_and_validate_xml(xml_bytes: bytes):
    try:
        xml_doc = etree.fromstring(xml_bytes)
        st.write(f"Root element: {xml_doc.tag}")

        if not SCHEMA_PATH.exists():
            return False, f"Le schéma est introuvable: {SCHEMA_PATH}"

        schema_doc = etree.parse(str(SCHEMA_PATH))
        schema = etree.XMLSchema(schema_doc)

        is_valid = schema.validate(xml_doc)

        if is_valid:
            return True, "Le fichier XML est valide selon le schéma XSD."
        else:
            errors = []
            for error in schema.error_log:
                errors.append(str(error))
            return False, "\n".join(errors)

    except etree.XMLSyntaxError as exc:
        return False, f"Erreur de syntaxe XML: {exc}"
    except Exception as exc:
        return False, f"Erreur lors du parsing XML: {exc}"

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

    valid, message = parse_and_validate_xml(xml_content)

    if valid:
        st.success(message)
    else:
        st.error("Validation XML échouée.")
        st.text(message)

else:
    st.info("Please upload an XML file to continue.")


#Create a buton to developp a dashboard to show the XML content and the validation result

if st.button("Show Dashboard"):
    st.subheader("XML Content")
    if uploaded_file is not None:
        st.code(xml_content.decode("utf-8"), language="xml")
    else:
        st.info("Please upload an XML file to view its content.")

    st.subheader("Validation Result")
    if uploaded_file is not None:
        if valid:
            st.success("The XML file is valid according to the XSD schema.")
        else:
            st.error("The XML file is invalid according to the XSD schema.")
            st.text(message)
    else:
        st.info("Please upload an XML file to see validation results.")