<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/MuseumDataset">
    <MuseumDataset>
      <xsl:apply-templates select="Artifacts"/>
      <xsl:apply-templates select="Exhibitions"/>
      <xsl:apply-templates select="Curators"/>
    </MuseumDataset>
  </xsl:template>

  <xsl:template match="Artifacts">
    <Artifacts>
      <xsl:apply-templates select="Artifact"/>
    </Artifacts>
  </xsl:template>

  <xsl:template match="Artifact">
    <Artifact id="{@id}">
      <title><xsl:value-of select="title"/></title>
      <artistRef><xsl:value-of select="artistRef"/></artistRef>
      <creationDate><xsl:value-of select="creationDate"/></creationDate>
      <acquisitionDate><xsl:value-of select="acquisitionDate"/></acquisitionDate>
    </Artifact>
  </xsl:template>
</xsl:stylesheet>
