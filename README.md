# S26 Data Pipeline Part 1
## XML-Based Museum and Cultural Heritage Management Platform

### Project overview

This project develops an XML-based data pipeline for managing museum and cultural heritage information. The project uses an XML dataset and an XSD schema to define and validate the data. XSLT stylesheets transform the same source data into HTML, XML, YAML and JSON outputs.

A Python/Streamlit loader and validation interface is also included for working with the dataset and running the pipeline.

### Main components

- XML sample dataset
- Final XSD schema
- XSLT transformation stylesheets
- JSON Schema for the JSON output
- Python validation and transformation programs
- Streamlit loader/interface
- Negative validation tests
- Project report

### Data model

The XML model contains HistoricalPeriods, CulturalSites, Artists, Curators, Collections, Artifacts, Exhibitions, Loans, RestorationProjects, Visitors and Visits.

The sample dataset contains **83 artifact records**. Artifact records use references to related entities such as artists, collections, historical periods and cultural sites where applicable.

### Schema and validation

The XSD is the main structural definition of the XML database. It defines data types, relationships and validation rules, including XSD 1.1 assertions for project-specific business rules.

The Python validation step uses the `xmlschema` library because the schema uses `xs:assert`, which is an XSD 1.1 feature.

Negative-test XML files are included to check that invalid data is rejected by the schema.

### Transformation scenarios

Ten transformation scenarios are included:

1. Collection inventory — HTML
2. Exhibition schedule — HTML
3. Artist biographies — HTML
4. Preservation status — HTML
5. Loan agreements — HTML
6. Visitor attendance report — HTML
7. Loan manifest — XML
8. Exhibition press feed — XML
9. Curator assignments — YAML
10. Loan monitoring — JSON

### Streamlit

The Streamlit part provides an interactive interface for the pipeline. The main workflow is:

1. Load the XML name 08_exhibition_press_feed_xml.xml in the Output file.
2. Validate the XML against the XSD.
3. Run an XSLT transformation.
4. Display the XML as HTML

You can access also by this link : https://museum-xml-test.streamlit.app/

### Schema access and maintenance

Access/responsibility for the schema was transferred to **Surya Pavan Karri** during the project. The schema should be kept synchronized with the current XML dataset and the transformation files.

After a schema change, the XML dataset and relevant transformations should be checked again before the change is considered final.

### Working environment

The group used:

- Visual Studio Code for development and organisation of project files
- Notepad++ for checking XML/XSD/XSLT files
- GitHub for version control, backups and collaboration
- Microsoft Edge and Google Chrome for checking transformation outputs
- Python 3.10 for scripting and pipeline support
- `lxml` for XML parsing and XSLT transformation
- `xmlschema` for XSD 1.1 validation
- Streamlit for the interactive loader/validator

### Repository structure

```text
.
├── schema/
├── synthetic_data/
├── xslt/
├── outputs/
├── negative_tests/
├── generate_dataset.py
├── validate.py
├── run_negative_tests.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

The exact filenames may vary in the final repository.

### Basic commands

Validate the XML dataset:

```bash
python validate.py
```

Run the negative validation tests:

```bash
python run_negative_tests.py
```

Start the Streamlit interface:

```bash
streamlit run streamlit_app.py
```

Use the actual Streamlit filename if the repository uses a different entry point.

or use this link : https://museum-xml-test.streamlit.app/

### Reproducibility

The dataset generation script uses a fixed random seed so that the development dataset can be reproduced consistently. The XML dataset is synthetic/fictional and is intended for development and testing.

### Group work

**Surya Pavan Karri**
- XML/database and dataset work
- HTML visualisation work
- XSD/schema work
- Working environment/tools section
- Schema maintenance after access/responsibility was transferred

**Aya Saadi**
- HTML visualisation work
- XML-to-XML transformations
- XML-to-YAML transformation

**Courvoisier Armand**
- XML-to-JSON transformation
- JSON Schema
- Python loader/validator
- Streamlit loader/interface

