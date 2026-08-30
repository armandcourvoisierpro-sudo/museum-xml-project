<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 9: Curator Assignments (XML to YAML)

  For each curator, lists the collections, exhibitions and restoration
  projects they are responsible for: a lightweight staffing/workload
  summary someone could read without any special tooling. This is the
  YAML scenario from the brief.

  XSLT has no built-in YAML serializer (unlike xsl:output method="json"
  in XSLT 3.0), so this stylesheet uses method="text" and builds the
  YAML syntax by hand, one curator at a time via apply-templates. Free
  text values are double-quoted because several exhibition titles
  contain a colon (e.g. "Light on the Seine: French Impressionism"),
  which YAML would otherwise read as a nested mapping.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="UTF-8"/>

  <xsl:key name="collectionsByCurator" match="Collection" use="@curatorRef"/>
  <xsl:key name="exhibitionsByCurator" match="Exhibition" use="@curatorRef"/>
  <xsl:key name="restorationsByCurator" match="RestorationProject" use="@curatorRef"/>

  <xsl:template match="/DATA">
    <xsl:text>curators:&#10;</xsl:text>
    <xsl:apply-templates select="Curators/Curator">
      <xsl:sort select="name"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="Curator">
    <xsl:text>  - id: </xsl:text><xsl:value-of select="@id"/><xsl:text>&#10;</xsl:text>
    <xsl:text>    name: "</xsl:text><xsl:value-of select="name"/><xsl:text>"&#10;</xsl:text>
    <xsl:text>    department: "</xsl:text><xsl:value-of select="department"/><xsl:text>"&#10;</xsl:text>
    <xsl:text>    collections:</xsl:text>
    <xsl:call-template name="idNameList">
      <xsl:with-param name="items" select="key('collectionsByCurator', @id)"/>
      <xsl:with-param name="nameField" select="'name'"/>
    </xsl:call-template>
    <xsl:text>    exhibitions:</xsl:text>
    <xsl:call-template name="idNameList">
      <xsl:with-param name="items" select="key('exhibitionsByCurator', @id)"/>
      <xsl:with-param name="nameField" select="'title'"/>
    </xsl:call-template>
    <xsl:text>    restorationProjectsLed:</xsl:text>
    <xsl:call-template name="idOnlyList">
      <xsl:with-param name="items" select="key('restorationsByCurator', @id)"/>
    </xsl:call-template>
  </xsl:template>

  <!-- Shared helper: renders a YAML list of "ID - Name" scalars, or
       an inline empty list if the curator has none of that kind. -->
  <xsl:template name="idNameList">
    <xsl:param name="items"/>
    <xsl:param name="nameField"/>
    <xsl:choose>
      <xsl:when test="count($items) = 0">
        <xsl:text> []&#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;</xsl:text>
        <xsl:for-each select="$items">
          <xsl:sort select="*[name()=$nameField]"/>
          <xsl:text>      - "</xsl:text>
          <xsl:value-of select="@id"/>
          <xsl:text> - </xsl:text>
          <xsl:value-of select="*[name()=$nameField]"/>
          <xsl:text>"&#10;</xsl:text>
        </xsl:for-each>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Same idea but for restoration projects, listed by ID only since
       they don't carry a short title field. -->
  <xsl:template name="idOnlyList">
    <xsl:param name="items"/>
    <xsl:choose>
      <xsl:when test="count($items) = 0">
        <xsl:text> []&#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;</xsl:text>
        <xsl:for-each select="$items">
          <xsl:sort select="@id"/>
          <xsl:text>      - </xsl:text>
          <xsl:value-of select="@id"/>
          <xsl:text>&#10;</xsl:text>
        </xsl:for-each>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
