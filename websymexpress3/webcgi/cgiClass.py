#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CGI definition: https://www.ietf.org/rfc/rfc3875
"""
#
# cgi definition: https://www.ietf.org/rfc/rfc3875
#
# Python source code:  https://www.python.org/
#

import sys
import os
import urllib.parse # https://stackoverflow.com/questions/8136788/decode-escaped-characters-in-url

class CgiClass():
  """
  Simple cgi class
  """

  def __init__(self ,httpHandler = None):
    self.cgiEnv       = {}
    self._bodyData    = None
    self._httpHandler = httpHandler  # http.server.SimpleHTTPRequestHandler

    if self._httpHandler != None:
      self.cgiEnv[ 'REQUEST_METHOD' ] = self._httpHandler.command

      urlpath, _, queryparam = self._httpHandler.path.partition( '?' )

      self.cgiEnv[ 'PATH_INFO'    ] = urlpath
      self.cgiEnv[ 'QUERY_STRING' ] = queryparam
    else:
      self.cgiEnv[ 'QUERY_STRING' ] = os.environ.get('QUERY_STRING')
      if self.cgiEnv[ 'QUERY_STRING' ] == None:
        self.cgiEnv[ 'QUERY_STRING' ] = ""

      self.cgiEnv[ 'REQUEST_METHOD' ] = os.environ.get( 'REQUEST_METHOD' )

    # https://stackoverflow.com/questions/12739911/how-to-split-a-string-within-a-list-to-create-key-value-pairs-in-python
    if len( self.cgiEnv[ 'QUERY_STRING' ] ) > 0:
      urlItems       = self.cgiEnv[ 'QUERY_STRING' ].split('&')
      self.urlParams = dict(s.split('=',1) for s in urlItems)
    else:
      self.urlParams = {}

  # get the http method (GET/POST/... )
  def getMethod( self ):
    """
    Get the action (method) of the call
    """
    return self.cgiEnv[ 'REQUEST_METHOD' ]

  def getBodyAsString( self ):
    """
    Get the body as a string, if not body is found give None back
    """
    if self._httpHandler != None:
      if self._bodyData == None :
        try:
          contentLen     = int( self._httpHandler.headers.get('Content-Length') )
          self._bodyData = str( self._httpHandler.rfile.read(contentLen), 'utf-8' )
        except: # pylint:disable=bare-except
          self._bodyData = ""

    else:
      # read all the body (stdin) and return it as a string
      # https://stackoverflow.com/questions/10718572/post-json-to-python-cgi
      if self._bodyData == None :
        self._bodyData = sys.stdin.read()
        if self._bodyData == None :
          self._bodyData = ""
    return self._bodyData

  # get url parameter, if not exist return empty string
  def getUrlParam( self, paramName ):
    """
    Get the url value of the given name. If not found give an empty string back ("")
    """
    if paramName in self.urlParams:
      paramValue = self.urlParams[ paramName ]
      paramValue = urllib.parse.unquote(paramValue, encoding='utf-8', errors='replace')
    else:
      paramValue = ""
    return paramValue

  def writeString( self, dataString ):
    """
    Write string as body
    """
    if self._httpHandler != None:

      if hasattr( dataString, "setHttpHandler" ):
        dataString.setHttpHandler( self._httpHandler )
        dataString.httpHandlerHeader()

      self._httpHandler.wfile.write( str( dataString ).encode('utf-8'))

    else:
      # stdout
      print( dataString )
