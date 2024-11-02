#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A html class to generate a html file
"""

import os
import time
import email.utils

from html    import escape
from pathlib import Path

class HtmlClass():
  """
  A html class to generate a html file
  """
  # pylint:disable=too-many-instance-attributes
  def __init__(self, settings = None):
    self._settings                 = settings
    self._httpHandler              = None   # http.server.SimpleHTTPRequestHandler , see cgiClass
    self._isTemplate               = False  # body contains templates inclusive header <head></head>
    self._replaceTokens            = False  # replace token in the html string

    self.tokenDocType              = '<!doctype html>'
    self.tokenHtmlStart            = '<html lang="en">'
    self.tokenHtmlEnd              = '</html>'
    self.tokenHtmlHeadStart        = '<head>'
    self.tokenHtmlHeadEnd          = '</head>'
    self.tokenHtmlBodyStart        = '<body>'
    self.tokenHtmlBodyEnd          = '</body>'
    self.tokenHtmlCssStart         = '<style>'
    self.tokenHtmlCssEnd           = '</style>'
    self.tokenHtmlJavascriptStart  = '<script>'
    self.tokenHtmlJavascriptEnd    = '</script>'

    self.tokenHtmlNewLine   = "\n"

    self.body           = []
    self.head           = []
    self.css            = []
    self.javascript     = []  # javascript in the head section
    self.javascriptBody = []  # javascript in the body section

    self.cssLink        = []
    self.javascriptLink = []

    self.headerVars     = {}

    #
    # html defaults
    #
    self.setHeaderVar( 'Content-Type', 'text/html;charset=utf-8')
    self.setHeaderVar( 'Status'      , '200 Ok')  # rfc 3875 6.3.3

    self.setHeaderVar( 'Last-modified', email.utils.formatdate(time.time(), usegmt=True) )

    self.addHead( '<meta charset="utf-8">' ) # always urf-8
    self.addHead( '<meta name="viewport" content="width=device-width, initial-scale=1">' )
    self.addHead( '<link rel="icon" href="/favicon.ico" >') # by new favicon add ?v=2, see https://stackoverflow.com/questions/2208933/how-do-i-force-a-favicon-refresh


  def setHeaderVar( self, varName, data ):
    """
    Add a html header variable
    """
    self.headerVars[ varName ] = data

  def addBody( self, text ):
    """
    Add text and or html code too the body
    """
    self.body.append( text )

  def addHead( self, text ):
    """
    Add a header line
    """
    self.head.append( text )

  def addCss( self, text ):
    """
    Add css code
    """
    self.css.append( text )

  def addCssLink( self, text ):
    """
    Add a css link
    """
    self.cssLink.append( text )

  def addJavascript( self, text ):
    """
    Add javascript code for in the header
    """
    self.javascript.append( text )

  def addJavascriptBody( self, text ):
    """
    Add javascript code for in the body
    """
    self.javascriptBody.append( text )

  def addJavascriptLink( self, text ):
    """
    Add a javascript link
    """
    self.javascriptLink.append( text )

  #
  # ---------- flex -------------------------
  #
  def addFlexCss( self ):
    """
    Add flex css file
    """
    self.addCssLink( '../style/flexpage.css' )


  #
  # --------- webserver handling (Python webserver) ------------------
  #
  def setHttpHandler( self, httpHandler ):
    """
    Set the httprequesthandler (http.server.BaseHTTPRequestHandler).
    It indicates the Python http server is used, Otherwise cgi handling will be used.
    """
    self._httpHandler = httpHandler # see cgiClass

  #
  # --------- template handling ------------------
  #
  def setReplaceTokens( self, replaceTokens ):
    """
    Replace the token in the html output
    """
    self._replaceTokens = replaceTokens

  def setTemplateHandling( self, isTemplate ):
    """
    Indicate this is a http template. Only the http header section en the body is used.
    Other sections (examply style, javascript etc) are ignored
    """
    self._isTemplate = isTemplate

  def readTemplate( self, templateName ):
    """
    Read template and give string back
    """
    htmlString = Path( os.path.join( self._settings.templateDirectory, templateName ) ).read_text( encoding="utf-8" )
    return htmlString

  def setTemplate( self, templateName ):
    """
    Read template and set it in the body, mark class as template
    """
    self.addBody( self.readTemplate( templateName ) )
    self.setTemplateHandling( True )
    self.setReplaceTokens( True )

  def replaceTokens( self, htmlString ):
    """
    Replace the token in the given string and give the result back.
    Tokens:
    - {{title}}                : Title of program
    - {{versioninformation}}   : Version information (div)
    - {{pageheader}}           : Page header (h1)
    """

    ### TODO addToken -> dictionary of key/value for replacement

    htmlString = htmlString.replace( "{{title}}"             , escape( self._settings.currentProgramName ) )
    htmlString = htmlString.replace( "{{versioninformation}}",         self.getVersionHtmlString()         )
    htmlString = htmlString.replace( "{{pageheader}}"        ,         self.getHtmlPageHeaderString()      )

    return htmlString


  #
  # --------- default css links ------------------
  #
  def addCssCommonLink( self ):
    """
    Add standard/common css style
    """
    self.addCssLink( '../style/common.css' )

  #
  # --------- version methods ------------------
  #
  def getVersionHtmlString( self ):
    """
    Give the html string back for the version information
    """
    dataStr = ""
    dataStr += '<div class="versioninfo">'
    dataStr += '<a href="' + self._settings.startUrl + '">Version: ' + self._settings.version + "</a>"
    dataStr += " | "
    dataStr += '<span class="menu">'
    dataStr += '<a href="' + self._settings.startUrl + '">Menu</a>'
    dataStr += '</span>'
    dataStr += '</div>'
    return dataStr

  def addVersionHtml( self ):
    """
    Add the html version div to the body
    """
    self.addBody( self.getVersionHtmlString() )

  def addVersionAndCssCommonLink( self ):
    """
    Add the version and the css common link
    """
    self.addCssCommonLink()
    self.addVersionHtml()

  #
  # --------- title methods ------------------
  #
  def addHtmlHeadTitle( self, title = None ):
    """
    Add html title
    """
    if title == None:
      title = self._settings.currentProgramName
    self.addHead( '<title>' + escape( title ) +  '</title>' )

  def getHtmlPageHeaderString( self, title = None ):
    """
    Give html page title string back
    """
    if title == None:
      title = self._settings.currentProgramName

    htmlStr = '<h1 class="center pageHeader">' + escape( title ) + '</h1>'
    return htmlStr

  def addHtmlPageHeader( self, title = None ):
    """
    Add html page header
    """
    htmlStr = self.getHtmlPageHeaderString( title )
    self.addBody( htmlStr )

  def addHtmlHeadTitleAndPageHeader( self, title = None ):
    """
    Add html title and page header
    """
    self.addHtmlHeadTitle(  title )
    self.addHtmlPageHeader( title )

  #
  # --------- output header(s) ------------------
  #
  def getHtmlHeaderString(self):
    """
    Get the html header string
    """
    htmlText = ""
    # header vars
    for key, headVar in self.headerVars.items() :
      htmlText += key + ': ' + headVar + "\r\n"

    htmlText += "\r\n"
    return htmlText


  def httpHandlerHeader( self ):
    """
    Do the http header output for the Python http.server
    """
    if self._httpHandler == None:
      return

    # first search for status
    statusValue = self.headerVars[ "Status" ]
    statusValue = statusValue.partition( ' ' )
    self._httpHandler.send_response( int( statusValue[ 0 ] ) )

    # output header
    for key, headVar in self.headerVars.items() :
      if key == "Status":
        continue
      self._httpHandler.send_header( key, headVar )

    # end header
    self._httpHandler.end_headers()


  #
  # --------- output html (string) ------------------
  #
  def getHtml( self ):
    """
    Get (generate) the html page (text)
    """
    # print( "start getHtml" )

    htmlText = ""
    if self._httpHandler == None:
      htmlText += self.getHtmlHeaderString()

    if self._isTemplate != True:
      # start html
      htmlText += self.tokenDocType   + self.tokenHtmlNewLine
      htmlText += self.tokenHtmlStart + self.tokenHtmlNewLine

      # head start
      htmlText += self.tokenHtmlHeadStart + self.tokenHtmlNewLine

      # head data
      for cData in self.head :
        htmlText += cData + self.tokenHtmlNewLine

      # css link
      for cData in self.cssLink:
        htmlText +=  '<link rel="stylesheet" href="' + cData + '">' + self.tokenHtmlNewLine

      # javascript link
      for cData in self.javascriptLink:
        htmlText +=  '<script src="' + cData + '"></script>' + self.tokenHtmlNewLine

      # css
      if len( self.css ) > 0:
        htmlText += self.tokenHtmlCssStart + self.tokenHtmlNewLine
        for cData in self.css:
          htmlText += cData + self.tokenHtmlNewLine
        htmlText += self.tokenHtmlCssEnd + self.tokenHtmlNewLine

      # javascript
      if len( self.javascript ) > 0:
        htmlText += self.tokenHtmlJavascriptStart + self.tokenHtmlNewLine
        for cData in self.javascript:
          htmlText += cData + self.tokenHtmlNewLine
        htmlText += self.tokenHtmlJavascriptEnd + self.tokenHtmlNewLine

      # head end
      htmlText += self.tokenHtmlHeadEnd + self.tokenHtmlNewLine

      # body
      htmlText += self.tokenHtmlBodyStart + self.tokenHtmlNewLine

      # javascript body
      if len( self.javascriptBody ) > 0:
        htmlText += self.tokenHtmlJavascriptStart + self.tokenHtmlNewLine
        for cData in self.javascriptBody:
          htmlText += cData + self.tokenHtmlNewLine
        htmlText += self.tokenHtmlJavascriptEnd + self.tokenHtmlNewLine

    # body
    for cData in self.body :
      htmlText += cData + self.tokenHtmlNewLine

    if self._isTemplate != True:
      htmlText += self.tokenHtmlBodyEnd + self.tokenHtmlNewLine

      # html end
      htmlText += self.tokenHtmlEnd + self.tokenHtmlNewLine

    if self._replaceTokens == True:
      htmlText = self.replaceTokens( htmlText )

    return htmlText

  def __str__( self ):
    """
    Same as getHtml()
    """
    return self.getHtml()
