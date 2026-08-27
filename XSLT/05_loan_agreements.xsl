<?xml version="1.0" encoding="UTF-8"?>
<!--
  Scenario 5: Loan Agreements Report

  Groups the loan agreements by status (Active, Pending, Overdue,
  Returned, Cancelled) so staff can see at a glance what is currently
  out, what is overdue, and what has been returned. Covers the
  "tracking loans" / "loan agreements" use case from the brief.

  Uses Muenchian grouping (a key on the status text, then picking the
  first Loan per key) instead of looping over a fixed list of statuses,
  so a new status value would still get its own group automatically.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:key name="loanByStatus" match="Loan" use="status"/>
  <xsl:key name="artifactById" match="Artifact" use="@id"/>

  <xsl:template match="/MuseumDatabase">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Loan Agreements Report</title>
        <style>
          body { font-family: Georgia, "Times New Roman", serif; margin: 2rem; color: #2b2620; background: #faf7f2; }
          h1 { border-bottom: 3px solid #7a5230; padding-bottom: 0.4rem; }
          h2 { color: #7a5230; margin-top: 1.6rem; }
          table { border-collapse: collapse; width: 100%; }
          th, td { text-align: left; padding: 0.45rem 0.7rem; border-bottom: 1px solid #ddd3c4; font-size: 0.92rem; }
          th { background: #efe6d8; }
          .Overdue { color: #a3271e; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Loan Agreements Report</h1>
        <xsl:for-each select="Loans/Loan[generate-id() = generate-id(key('loanByStatus', status)[1])]">
          <xsl:sort select="status"/>
          <xsl:variable name="statusName" select="status"/>
          <h2><xsl:value-of select="$statusName"/> (<xsl:value-of select="count(key('loanByStatus', $statusName))"/>)</h2>
          <table>
            <tr><th>Loan ID</th><th>Artifact</th><th>Institution</th><th>Start</th><th>End</th><th>Insurance Value</th></tr>
            <xsl:apply-templates select="key('loanByStatus', $statusName)">
              <xsl:sort select="loanStartDate"/>
            </xsl:apply-templates>
          </table>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="Loan">
    <xsl:variable name="artifact" select="key('artifactById', @artifactRef)"/>
    <tr>
      <xsl:if test="status = 'Overdue'"><xsl:attribute name="class">Overdue</xsl:attribute></xsl:if>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="$artifact/name"/></td>
      <td><xsl:value-of select="borrowingInstitution"/></td>
      <td><xsl:value-of select="loanStartDate"/></td>
      <td><xsl:value-of select="loanEndDate"/></td>
      <td>
        <xsl:choose>
          <xsl:when test="insuranceValue"><xsl:value-of select="insuranceValue"/></xsl:when>
          <xsl:otherwise>not recorded</xsl:otherwise>
        </xsl:choose>
      </td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
