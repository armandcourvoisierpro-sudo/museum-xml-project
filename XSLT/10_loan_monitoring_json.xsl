<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="text" encoding="UTF-8" indent="no"/>

<!--
  Scenario 6: Tracking loans of museum artefacts.

  The museum wishes to automatically generate a JSON file enabling the collections 
  management department to track active, pending and overdue loans. For each 
  selected loan, information regarding the loan, the artefact in question and its 
  collection is collated. Loans are sorted by status and then by end date to facilitate 
  the tracking of due dates. Where an insurance value is not recorded in the database, 
  it is replaced by null.
-->

<!-- Creates the main structure of the JSON output and selects active, pending or overdue loans, then sorts them by status and end date.-->
    <xsl:template match="/">
        {
            "loanMonitoring": {
                "description": "Active, pending and overdue museum loans",
                "loans": [
                    <xsl:apply-templates select="//Loan[
                        status = 'Active'
                        or status = 'Pending'
                        or status = 'Overdue'
                    ]">
                        <xsl:sort select="status" order="ascending"/>
                        <xsl:sort select="loanEndDate" order="ascending"/>
                    </xsl:apply-templates>
                ]
            }
        }
    </xsl:template>

<!--Converts each selected loan into a JSON object, retrieving its details, those of the associated artwork and those of its collection.-->
    <xsl:template match="Loan">
        {
            "loanId": "<xsl:value-of select="@id"/>",
            "status": "<xsl:value-of select="status"/>",
            "borrowingInstitution": "<xsl:value-of select="borrowingInstitution"/>",
            "loanStartDate": "<xsl:value-of select="loanStartDate"/>",
            "loanEndDate": "<xsl:value-of select="loanEndDate"/>",
            "insuranceValue": <xsl:call-template name="insurance-value"/>,
            "artifact": {
                "id": "<xsl:value-of select="//Artifact[@id = current()/@artifactRef]/@id"/>",
                "name": "<xsl:value-of select="//Artifact[@id = current()/@artifactRef]/name"/>",
                "type": "<xsl:value-of select="//Artifact[@id = current()/@artifactRef]/type"/>",
                "condition": "<xsl:value-of select="//Artifact[@id = current()/@artifactRef]/condition"/>"
            },
            "collection": {
                "id": "<xsl:value-of select="//Collection[@id = //Artifact[@id = current()/@artifactRef]/@collectionRef]/@id"/>",
                "name": "<xsl:value-of select="//Collection[@id = //Artifact[@id = current()/@artifactRef]/@collectionRef]/name"/>"
            }
        }<xsl:if test="position() != last()">,</xsl:if>
    </xsl:template>

    <!--Checks whether an insurance value has been entered: if so, it displays it; otherwise, it returns null.-->
    <xsl:template name="insurance-value">
        <xsl:choose>
            <xsl:when test="string-length(insuranceValue) > 0">
                <xsl:value-of select="insuranceValue"/>
            </xsl:when>
            <xsl:otherwise>null</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
