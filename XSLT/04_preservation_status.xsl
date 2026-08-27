<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 4: Preservation Status Report

  This one computes something that is not stored directly in the XML:
  for every artifact in Poor or Critical condition, it checks whether a
  restoration project already exists for it, and flags the ones that
  don't. This is the "tracking restoration activities" / preservation
  reporting use case from the brief. The flag itself is new data derived
  by the stylesheet, not copied from a single element.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="restorationsByArtifact" match="RestorationProject" use="@artifactRef"/>

  <xsl:template match="/MuseumDatabase">
    <xsl:variable name="atRisk" select="Artifacts/Artifact[condition = 'Poor' or condition = 'Critical']"/>
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Preservation Status Report</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          .summary { background: #efe6d8; padding: 0.8rem 1.2rem; border-radius: 6px; margin-bottom: 1.2rem; }
          table { border-collapse: collapse; width: 100%; }
          th, td { text-align: left; padding: 0.45rem 0.7rem; border-bottom: 1px solid #ddd3c4; font-size: 0.92rem; }
          th { background: #efe6d8; }
          .critical { color: #a3271e; font-weight: bold; }
          .poor { color: #b06a15; }
          .covered { color: #2f6b2f; }
          .uncovered { color: #a3271e; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Preservation Status Report</h1>
        <div class="summary">
          <p><xsl:value-of select="count($atRisk)"/> artifacts require preservation attention
             (<xsl:value-of select="count($atRisk[condition='Critical'])"/> Critical,
              <xsl:value-of select="count($atRisk[condition='Poor'])"/> Poor).</p>
          <p><xsl:value-of select="count($atRisk[key('restorationsByArtifact', @id)])"/> already have a restoration project on record;
             <xsl:value-of select="count($atRisk[not(key('restorationsByArtifact', @id))])"/> do not.</p>
        </div>
        <table>
          <tr><th>ID</th><th>Name</th><th>Condition</th><th>Restoration Status</th></tr>
          <xsl:apply-templates select="$atRisk">
            <xsl:sort select="condition" order="ascending"/>
            <xsl:sort select="name"/>
          </xsl:apply-templates>
        </table>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Artifact">
    <xsl:variable name="restoration" select="key('restorationsByArtifact', @id)"/>
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="name"/></td>
      <td>
        <xsl:attribute name="class"><xsl:value-of select="translate(condition, 'PC', 'pc')"/></xsl:attribute>
        <xsl:value-of select="condition"/>
      </td>
      <td>
        <xsl:choose>
          <xsl:when test="$restoration">
            <span class="covered">On record (<xsl:value-of select="$restoration/status"/>, <xsl:value-of select="$restoration/@id"/>)</span>
          </xsl:when>
          <xsl:otherwise>
            <span class="uncovered">No restoration project recorded</span>
          </xsl:otherwise>
        </xsl:choose>
      </td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
