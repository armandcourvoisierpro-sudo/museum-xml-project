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

### Streamlit loader

The Streamlit part provides an interactive interface for the pipeline. The main workflow is:

1. Load the XML dataset.
2. Validate the XML against the XSD.
3. Run an XSLT transformation.
4. Display or save the resulting output.

The Streamlit loader/interface work was carried out by **Person C** as part of the loader/validator work.

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

### Reproducibility

The dataset generation script uses a fixed random seed so that the development dataset can be reproduced consistently. The XML dataset is synthetic/fictional and is intended for development and testing.

### Group work

**Person A — Surya Pavan Karri**
- XML/database and dataset work
- HTML visualisation work
- XSD/schema work
- Working environment/tools section
- Schema maintenance after access/responsibility was transferred

**Person B — Aya Saadi**
- HTML visualisation work
- XML-to-XML transformations
- XML-to-YAML transformation

**Person C — Courvoisier Armand**
- XML-to-JSON transformation
- JSON Schema
- Python/Java loader/validator
- Streamlit loader/interface

The final report should be used as the authoritative record for the exact contribution percentages agreed by the group.

### Final consistency check

Before submission, check:

- XSD ↔ XML dataset
- Schema relationships and business rules
- XSLT ↔ XML element and attribute names
- JSON output ↔ JSON Schema
- Streamlit loader ↔ current schema and dataset
- Negative validation tests
- Report ↔ actual work completed
- GitHub repository ↔ final submission files
