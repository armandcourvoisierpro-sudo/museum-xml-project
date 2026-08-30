<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 8: Exhibition Press Feed (XML to XML)

  Reformats exhibitions into a short syndication feed for the press
  office / museum website, again in a different vocabulary from our
  own database (PressFeed/Show instead of Exhibitions/Exhibition), with
  a computed teaser line built from the featured-artifact count rather
  than copied from a single field. This is the second of the two
  "exploitation in another XML format" scenarios from the brief.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

  <xsl:key name="curatorById" match="Curator" use="@id"/>

  <xsl:template match="/DATA">
    <PressFeed generatedFor="press-office-and-website">
      <xsl:apply-templates select="Exhibitions/Exhibition">
        <xsl:sort select="startDate"/>
      </xsl:apply-templates>
    </PressFeed>
  </xsl:template>

  <xsl:template match="Exhibition">
    <xsl:variable name="curator" select="key('curatorById', @curatorRef)"/>
    <Show ref="{@id}">
      <Headline><xsl:value-of select="title"/></Headline>
      <Venue><xsl:value-of select="location"/></Venue>
      <RunDates><xsl:value-of select="startDate"/> - <xsl:value-of select="endDate"/></RunDates>
      <Curator><xsl:value-of select="$curator/name"/></Curator>
      <Teaser>
        <xsl:choose>
          <xsl:when test="description"><xsl:value-of select="description"/></xsl:when>
          <xsl:otherwise>Featuring <xsl:value-of select="count(FeaturedArtifact)"/> objects from the collection.</xsl:otherwise>
        </xsl:choose>
      </Teaser>
    </Show>
  </xsl:template>

</xsl:stylesheet>
