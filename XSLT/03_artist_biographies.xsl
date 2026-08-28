<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 3: Artist Biographies

  One page per artist, showing their biography alongside the list of
  works the museum holds by them. Covers the "artist biographies" use
  case from the project brief. Artists with no catalogued work yet are
  still listed (with a note), since an artist record can exist before
  any artifact is attributed to them.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="artifactsByArtist" match="Artifact" use="@artistRef"/>

  <xsl:template match="/MuseumDatabase">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Artist Biographies</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          .artist { margin-bottom: 1.8rem; }
          .artist h2 { margin-bottom: 0.1rem; color: #7a5230; }
          .meta { color: #5a5248; font-size: 0.9rem; margin: 0.1rem 0 0.4rem 0; }
          .bio { margin: 0.3rem 0; }
          ul.works { margin: 0.3rem 0 0 0; padding-left: 1.2rem; }
          .no-works { color: #888; font-style: italic; }
        </style>
      </head>
      <body>
        <h1>Artist Biographies</h1>
        <xsl:apply-templates select="Artists/Artist">
          <xsl:sort select="name"/>
        </xsl:apply-templates>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Artist">
    <xsl:variable name="works" select="key('artifactsByArtist', @id)"/>
    <div class="artist">
      <h2><xsl:value-of select="name"/></h2>
      <p class="meta">
        <xsl:if test="nationality"><xsl:value-of select="nationality"/><xsl:text> &#8226; </xsl:text></xsl:if>
        <xsl:choose>
          <xsl:when test="birthYear or deathYear">
            <xsl:choose><xsl:when test="birthYear"><xsl:value-of select="birthYear"/></xsl:when><xsl:otherwise>?</xsl:otherwise></xsl:choose>
            <xsl:text> - </xsl:text>
            <xsl:choose><xsl:when test="deathYear"><xsl:value-of select="deathYear"/></xsl:when><xsl:otherwise>?</xsl:otherwise></xsl:choose>
          </xsl:when>
          <xsl:otherwise>dates unknown</xsl:otherwise>
        </xsl:choose>
      </p>
      <xsl:if test="biography">
        <p class="bio"><xsl:value-of select="biography"/></p>
      </xsl:if>
      <xsl:choose>
        <xsl:when test="count($works) = 0">
          <p class="no-works">No artifacts currently attributed to this artist in the collection.</p>
        </xsl:when>
        <xsl:otherwise>
          <p>Works in the collection (<xsl:value-of select="count($works)"/>):</p>
          <ul class="works">
            <xsl:apply-templates select="$works">
              <xsl:sort select="creationYear"/>
            </xsl:apply-templates>
          </ul>
        </xsl:otherwise>
      </xsl:choose>
    </div>
  </xsl:template>

  <xsl:template match="Artifact">
    <li>
      <xsl:value-of select="name"/>
      <xsl:if test="creationYear"> (<xsl:value-of select="creationYear"/>)</xsl:if>
    </li>
  </xsl:template>

</xsl:stylesheet>
