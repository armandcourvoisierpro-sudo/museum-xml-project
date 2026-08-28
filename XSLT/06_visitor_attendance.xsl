<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 6: Visitor Attendance Report

  For each exhibition, computes total visit count and a breakdown by
  ticket type directly from the Visit records (nothing here is stored
  as a single field; it's all counted at transform time. Exhibitions
  are ranked busiest-first. Covers "generating reports on ... visitor
  attendance" from the brief.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="visitsByExhibition" match="Visit" use="@exhibitionRef"/>

  <xsl:template match="/MuseumDatabase">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Visitor Attendance Report</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          table { border-collapse: collapse; width: 100%; }
          th, td { text-align: left; padding: 0.45rem 0.7rem; border-bottom: 1px solid #ddd3c4; font-size: 0.92rem; }
          th { background: #efe6d8; }
          .bar { display: inline-block; height: 0.7rem; background: #7a5230; vertical-align: middle; margin-right: 0.4rem; }
          .totals { margin-top: 1.4rem; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Visitor Attendance Report</h1>
        <p>Exhibitions ranked by total recorded visits, busiest first.</p>
        <table>
          <tr><th>Exhibition</th><th>Total Visits</th><th>Standard</th><th>Student</th><th>Senior</th><th>Free</th><th>Group</th></tr>
          <xsl:apply-templates select="Exhibitions/Exhibition">
            <xsl:sort select="count(key('visitsByExhibition', @id))" data-type="number" order="descending"/>
          </xsl:apply-templates>
        </table>
        <p class="totals">Total visits recorded across all exhibitions: <xsl:value-of select="count(Visits/Visit)"/></p>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Exhibition">
    <xsl:variable name="visits" select="key('visitsByExhibition', @id)"/>
    <tr>
      <td><xsl:value-of select="title"/></td>
      <td>
        <span class="bar">
          <xsl:attribute name="style">width: <xsl:value-of select="count($visits) * 4"/>px;</xsl:attribute>
        </span>
        <xsl:value-of select="count($visits)"/>
      </td>
      <td><xsl:value-of select="count($visits[ticketType='Standard'])"/></td>
      <td><xsl:value-of select="count($visits[ticketType='Student'])"/></td>
      <td><xsl:value-of select="count($visits[ticketType='Senior'])"/></td>
      <td><xsl:value-of select="count($visits[ticketType='Free'])"/></td>
      <td><xsl:value-of select="count($visits[ticketType='Group'])"/></td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
