import streamlit as st
from pathlib import Path
from lxml import etree

# Scenario : A museum staff member uploads an XML file 
# (08_exhibition_press_feed_xml.xml)containing exhibition information. 
# The application validates the file against an XSD schema to ensure 
# it is well-formed and compliant. If valid, it transforms the XML into 
# an HTML page for readable display. If invalid, it shows the exact 
# validation errors so the file can be corrected. The final result is
# user-friendly for checking and presenting museum data

# Page configuration
st.set_page_config(
    page_title="Museum XML Pipeline",
    page_icon="🏛️",
    layout="wide"
)

st.title("Museum XML Processing App")

st.markdown(
    """
    This application allows you to:
    1. upload an XML file,
    2. parse it with XML APIs,
    3. validate it against the XML schema,
    4. transform it into HTML for display.

    The goal is to process museum XML data from ingestion to validation and presentation in a simple interface.
    """
)

st.caption("XML input → schema validation → HTML transformation")

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "XSLT" / "xml_transfo.xsd"

HTML_XSL = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Exhibition Press Feed</title>
        <style>
          body {
            font-family: Georgia, "Times New Roman", serif;
            margin: 2rem;
            color: #2b2620;
            background: #faf7f2;
          }
          h1 {
            color: #7a5230;
            border-bottom: 3px solid #7a5230;
            padding-bottom: 0.5rem;
          }
          .show-card {
            background: white;
            border: 1px solid #ddd3c4;
            border-radius: 10px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
          }
          .show-card h2 {
            margin: 0 0 0.6rem 0;
            color: #2d4a5c;
          }
          .show-card p {
            margin: 0.25rem 0;
            line-height: 1.5;
          }
          strong {
            color: #3a2d24;
          }
        </style>
      </head>
      <body>
        <h1>Exhibition Press Feed</h1>
        <xsl:for-each select="PressFeed/Show">
          <div class="show-card">
            <h2><xsl:value-of select="Headline"/></h2>
            <p><strong>Reference:</strong> <xsl:value-of select="@ref"/></p>
            <p><strong>Venue:</strong> <xsl:value-of select="Venue"/></p>
            <p><strong>Dates:</strong> <xsl:value-of select="RunDates"/></p>
            <p><strong>Curator:</strong> <xsl:value-of select="Curator"/></p>
            <p><strong>Teaser:</strong> <xsl:value-of select="Teaser"/></p>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
"""


def parse_and_validate_xml(xml_bytes: bytes):
    try:
        xml_doc = etree.fromstring(xml_bytes)

        if not SCHEMA_PATH.exists():
            return False, f"Schema file not found: {SCHEMA_PATH}"

        schema_doc = etree.parse(str(SCHEMA_PATH))
        schema = etree.XMLSchema(schema_doc)

        is_valid = schema.validate(xml_doc)

        if is_valid:
            return True, "The XML file is valid according to the XSD schema."
        else:
            errors = []
            for error in schema.error_log:
                errors.append(str(error))
            return False, "\n".join(errors)

    except etree.XMLSyntaxError as exc:
        return False, f"XML syntax error: {exc}"
    except Exception as exc:
        return False, f"Error while parsing XML: {exc}"


def transform_to_html(xml_bytes: bytes):
    try:
        xml_doc = etree.fromstring(xml_bytes)
        xsl_root = etree.fromstring(HTML_XSL.encode("utf-8"))
        transform = etree.XSLT(xsl_root)
        html_doc = transform(xml_doc)
        return True, etree.tostring(html_doc, pretty_print=True, method="html", encoding="unicode")
    except Exception as exc:
        return False, f"Error while transforming to HTML: {exc}"


# Upload section
st.subheader("Upload XML file")

uploaded_file = st.file_uploader(
    "Drag and drop an XML file here",
    type=["xml"],
    help="Upload a museum XML file to validate and transform it."
)

validation_result = None
html_result = None

if uploaded_file is not None:
    xml_bytes = uploaded_file.getvalue()

    validation_result = parse_and_validate_xml(xml_bytes)

    if validation_result[0]:
        st.success(validation_result[1])
    else:
        st.error("XML validation failed.")
        st.text(validation_result[1])

    html_result = transform_to_html(xml_bytes)

    if html_result[0]:
        st.success("HTML transformation succeeded.")
    else:
        st.error(html_result[1])
else:
    st.info("Please upload an XML file to begin.")


# Final button
if st.button("View HTML"):
    st.subheader("HTML output")

    if uploaded_file is not None:
        if html_result and html_result[0]:
            st.components.v1.html(html_result[1], height=800, scrolling=True)
        else:
            st.info("The HTML transformation could not be generated.")
    else:
        st.info("Please upload an XML file to view the generated HTML.")