<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 2: Exhibition Schedule

  Chronological listing of exhibitions (past, current, upcoming) with
  their curator, location and featured artifacts. Covers the "managing
  exhibition schedules" use case from the project brief.

  Exhibitions are sorted by startDate. FeaturedArtifact/@artifactRef is
  resolved to the real artifact name/type through xsl:key rather than
  just printing the raw ID reference.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="artifactById" match="Artifact" use="@id"/>
  <xsl:key name="curatorById" match="Curator" use="@id"/>

  <xsl:template match="/MuseumDatabase">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Exhibition Schedule</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          .exhibition { border: 1px solid #ddd3c4; border-radius: 6px; padding: 1rem 1.2rem; margin-bottom: 1.2rem; background: #fff; }
          .exhibition h2 { margin: 0 0 0.2rem 0; color: #7a5230; }
          .dates { font-weight: bold; color: #5a5248; }
          .location { color: #5a5248; }
          .desc { margin-top: 0.5rem; }
          ul.featured { margin: 0.5rem 0 0 0; padding-left: 1.2rem; }
          ul.featured li { font-size: 0.92rem; }
        </style>
      </head>
      <body>
        <h1>Exhibition Schedule</h1>
        <xsl:apply-templates select="Exhibitions/Exhibition">
          <xsl:sort select="startDate"/>
        </xsl:apply-templates>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Exhibition">
    <xsl:variable name="curator" select="key('curatorById', @curatorRef)"/>
    <div class="exhibition">
      <h2><xsl:value-of select="title"/></h2>
      <p class="dates"><xsl:value-of select="startDate"/> to <xsl:value-of select="endDate"/></p>
      <p class="location"><xsl:value-of select="location"/> &#8226; Curated by <xsl:value-of select="$curator/name"/></p>
      <xsl:if test="description">
        <p class="desc"><xsl:value-of select="description"/></p>
      </xsl:if>
      <p>Featured artifacts (<xsl:value-of select="count(FeaturedArtifact)"/>):</p>
      <ul class="featured">
        <xsl:apply-templates select="FeaturedArtifact"/>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="FeaturedArtifact">
    <xsl:variable name="artifact" select="key('artifactById', @artifactRef)"/>
    <li><xsl:value-of select="$artifact/name"/> (<xsl:value-of select="$artifact/type"/>)</li>
  </xsl:template>

</xsl:stylesheet>
