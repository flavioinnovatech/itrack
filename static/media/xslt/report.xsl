<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/document">
  <html>
  <head><title>Relat&#243;rio</title></head>
  <body>
  <h2>Relat&#243;rio <img src="/media/img/printer.gif" onclick="window.print();" style="cursor:pointer;" width="16" height="16"/></h2>
  <table border="0" cellspacing="0" cellpadding="0">
  <xsl:apply-templates/>    
  </table>
  </body>
  </html>
</xsl:template>

<xsl:template match="row">
  <tr>
  <xsl:apply-templates select="field"/>
  </tr>
</xsl:template>

<xsl:template match="head">
  <tr>
  <xsl:apply-templates select="coltitle"/>
  </tr>
</xsl:template>

<xsl:template match="field">
  <td style="white-space:nowrap;border:solid 1px #000;padding-left:5px;padding-right:5px;">
  <xsl:value-of select="."/>
  </td>
</xsl:template>

<xsl:template match="coltitle">
  <td style="white-space:nowrap;background-color:#888;color:#fff;border:solid 1px #000;padding:5px;">
  <xsl:value-of select="."/>
  </td>
</xsl:template>

</xsl:stylesheet>

