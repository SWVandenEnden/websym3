#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class to produce a json output page
"""


class JsonApplicationClass():
  """
  Class to produce a json output page
  """
  def __init__(self):
    self._httpHandler     = None  # http.server.SimpleHTTPRequestHandler , see cgiClass

    self.tokenHtmlNewLine = "\n"

    self.headerVars       = {}
    self.jsonString       = "{}"

    self.setHeaderVar( 'Content-Type', 'application/json')
    self.setHeaderVar( 'Status'      , '200 Ok')  # rfc 3875 6.3.3

  def setHttpHandler( self, httpHandler ):
    """
    Set the httprequesthandler (http.server.BaseHTTPRequestHandler).
    It indicates the Python http server is used, Otherwise cgi handling will be used.
    """
    self._httpHandler = httpHandler # see cgiClass

  def setHeaderVar( self, varName, data ):
    """
    Set a header variable
    """
    self.headerVars[ varName ] = data

  def setJsonString (self, jsonString ):
    """
    Set the output json string
    """
    self.jsonString = jsonString

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

  def getJsonApplcation( self ):
    """
    Get the json output page
    """
    htmlText = ""
    if self._httpHandler == None:
      # header vars
      for key, data in self.headerVars.items() :
        htmlText += key + ': ' + data + "\r\n"

      htmlText += "\r\n"

    # json data
    htmlText += self.jsonString

    return htmlText

  def __str__( self ):
    """
    Same as getJsonApplcation
    """
    return self.getJsonApplcation()
