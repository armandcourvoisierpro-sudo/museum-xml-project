<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 1: Collection Inventory

  For each Collection in the museum, list its artifacts (name, type,
  condition, creation year) plus the curator responsible for the
  collection. Answers the "browse collections and see what is in them"
  use case from the project brief (collection inventories).

  Artifacts are looked up with xsl:key on Artifact/@collectionRef
  instead of a nested for-each with an XPath filter, so each artifact
  is only visited once per matching collection.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="artifactsByCollection" match="Artifact" use="@collectionRef"/>
  <xsl:key name="curatorById" match="Curator" use="@id"/>

  <xsl:template match="/MuseumDatabase">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Collection Inventory</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          .collection { margin-bottom: 2.5rem; }
          .collection h2 { color: #7a5230; margin-bottom: 0.1rem; }
          .collection .theme { font-style: italic; color: #5a5248; margin-top: 0; }
          .collection .curator { font-size: 0.9rem; color: #5a5248; }
          table { border-collapse: collapse; width: 100%; margin-top: 0.6rem; }
          th, td { text-align: left; padding: 0.4rem 0.6rem; border-bottom: 1px solid #ddd3c4; font-size: 0.92rem; }
          th { background: #efe6d8; }
          .empty { color: #888; font-style: italic; }
        </style>
      </head>
      <body>
        <h1>Collection Inventory</h1>
        <p><xsl:value-of select="count(Collections/Collection)"/> collections, <xsl:value-of select="count(Artifacts/Artifact)"/> artifacts total.</p>
        <xsl:apply-templates select="Collections/Collection">
          <xsl:sort select="name"/>
        </xsl:apply-templates>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Collection">
    <xsl:variable name="curator" select="key('curatorById', @curatorRef)"/>
    <div class="collection">
      <h2><xsl:value-of select="name"/></h2>
      <xsl:if test="theme">
        <p class="theme"><xsl:value-of select="theme"/></p>
      </xsl:if>
      <p class="curator">Curator: <xsl:value-of select="$curator/name"/> (<xsl:value-of select="$curator/department"/>)</p>
      <xsl:variable name="items" select="key('artifactsByCollection', @id)"/>
      <xsl:choose>
        <xsl:when test="count($items) = 0">
          <p class="empty">No artifacts currently catalogued in this collection.</p>
        </xsl:when>
        <xsl:otherwise>
          <table>
            <tr><th>ID</th><th>Name</th><th>Type</th><th>Year</th><th>Condition</th></tr>
            <xsl:apply-templates select="$items">
              <xsl:sort select="name"/>
            </xsl:apply-templates>
          </table>
        </xsl:otherwise>
      </xsl:choose>
    </div>
  </xsl:template>

  <xsl:template match="Artifact">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="name"/></td>
      <td><xsl:value-of select="type"/></td>
      <td>
        <xsl:choose>
          <xsl:when test="creationYear"><xsl:value-of select="creationYear"/></xsl:when>
          <xsl:otherwise>unknown</xsl:otherwise>
        </xsl:choose>
      </td>
      <td><xsl:value-of select="condition"/></td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
