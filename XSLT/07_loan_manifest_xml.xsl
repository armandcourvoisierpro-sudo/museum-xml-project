<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 7: Loan Manifest Export (XML to XML)

  Reformats the Pending and Active loans into a compact shipping/
  insurance manifest in a different vocabulary from our own database
  (LoanManifest/Shipment instead of Loans/Loan), the kind of document a
  registrar would hand to a courier or insurer. This is one of the two
  "exploitation in another XML format" scenarios from the brief.

  Only Pending/Active loans are included, since Returned/Cancelled/
  Overdue loans are not upcoming shipments a courier needs to plan for.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

  <xsl:key name="artifactById" match="Artifact" use="@id"/>

  <xsl:template match="/DATA">
    <LoanManifest generatedFor="courier-and-insurer" recordCount="{count(Loans/Loan[status='Pending' or status='Active'])}">
      <xsl:apply-templates select="Loans/Loan[status='Pending' or status='Active']">
        <xsl:sort select="loanStartDate"/>
      </xsl:apply-templates>
    </LoanManifest>
  </xsl:template>

  <xsl:template match="Loan">
    <xsl:variable name="artifact" select="key('artifactById', @artifactRef)"/>
    <Shipment id="{@id}" status="{status}">
      <ObjectReference><xsl:value-of select="@artifactRef"/></ObjectReference>
      <ObjectTitle><xsl:value-of select="$artifact/name"/></ObjectTitle>
      <ObjectType><xsl:value-of select="$artifact/type"/></ObjectType>
      <ObjectCondition><xsl:value-of select="$artifact/condition"/></ObjectCondition>
      <Destination><xsl:value-of select="borrowingInstitution"/></Destination>
      <DepartureDate><xsl:value-of select="loanStartDate"/></DepartureDate>
      <ReturnDueDate><xsl:value-of select="loanEndDate"/></ReturnDueDate>
      <xsl:if test="insuranceValue">
        <InsuredValue currency="EUR"><xsl:value-of select="insuranceValue"/></InsuredValue>
      </xsl:if>
    </Shipment>
  </xsl:template>

</xsl:stylesheet>
