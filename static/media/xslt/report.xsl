<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/document">
  <html>
  <head>
     <title>Relat&#243;rio</title>
  </head>
  <body>
  <xsl:apply-templates select="info"/>
  <table border="0" cellspacing="0" cellpadding="0">
  <xsl:apply-templates select="head"/>
  <xsl:apply-templates select="row"/>        
  </table>
  </body>
  </html>
  
</xsl:template>

<xsl:template match="info">

  <table border="0">
  <tr>
  
  <td><img src="/media/static/img/logo_wbg.png"/></td>
  
  <td style="padding-left:20px;">
  
  
  <div style="font-size:16px;">
  <span style="font-size:22px;"><xsl:value-of select="title"/></span>
  <img src="/media/img/printer.gif" onclick="window.print();" style="padding-left:20px;cursor:pointer;" width="16" height="16"/><br/>
  A partir de : <xsl:value-of select="datestart"/> <br/>
  At&#233; : <xsl:value-of select="dateend"/> <br/>
  Emitido em : <xsl:value-of select="datenow"/><br/>
  Dist&#226;ncia Percorrida* : <xsl:value-of select="totaldistance"/> km<br/>
  Motorista : <xsl:value-of select="driver"/><br/>
  </div>
  
  </td>
  </tr>
  </table><br/>
  
  
  <table border="0" width="700" style="margin-left:10px;" cellpadding="0" cellspacing="0">
  <tr>
  <td style="padding:3px;">
  Placa : <xsl:value-of select="licenseplate"/>
  </td>
  <td style="padding:3px;">
  Cor : <xsl:value-of select="color"/>
  </td>
  <td style="padding:3px;">
  Ano : <xsl:value-of select="year"/>
  </td>
  <td style="padding:3px;">
  Tipo : <xsl:value-of select="type"/>
  </td>
  </tr>
  <tr>
  
  <td style="padding:3px;">
  Modelo : <xsl:value-of select="model"/>
  </td>
  <td style="padding:3px;">
  Marca : <xsl:value-of select="brand"/>
  </td>
  <td colspan="2" style="padding:3px;">
  Chassi : <xsl:value-of select="bodyframe"/>
  </td>
  </tr>
  </table>
  
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

