#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Web user interface for symexpress3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import os
import os.path
import http.server
import webbrowser
import urllib.parse
import configparser
# import time
# import email.utils

from pathlib import Path

import websymexpress3

# ---------- Version information ---------------
__version__     = "0.0.6"

__author__      = "Gien van den Enden"
__copyright__   = "Copyright 2024, Gien van den Enden"
__credits__     = [ ]
__license__     = "GPL"

__maintainer__  = "Gien van den Enden"
__email__       = "swvandenenden@gmail.com"
__status__      = "Development"


# ---------- Global vars ---------------

GlobalHttpd  = None     # http.server.ThreadingHTTPServer
GlobalConfig = None     # configparser.ConfigParser

GlobalDebug  = False


# ---------- Program ---------------

def DisplayHelp():
  """
  Display help
  """
  print( "Start the user (web) interface for symexpress3" )
  print( " " )
  print( "usage: python websym3 [options]" )
  print( "options: " )
  print( "  -h               : Help" )
  print( "  -p <number>      : Port number web server" )
  print( "  -u <url>         : Automatic open url" )
  print( "  -a <True/False>  : Enable/disable automatic open url" )
  print( "  -c <filename>    : Configuration file" )
  print( " " )
  print( "Example: " )
  print( 'python websym3 -p 9090' )
  print( " " )
  print( "Configuration file, default is websym3.ini" )
  print( "Syntax: " )
  print( " " )
  print( "[Path]" )
  print( "data=<directory>         # Directory user data, default <root>/data"        )
  print( "javascript=<directory>   # Directory javascript files, default <root>/javascript" )
  print( "style=<directory>        # Directory css style files, default <root>/style"  )
  print( "template=<directory>     # Directory template files, default <root>/template"   )
  print( " " )
  print( "[Server]" )
  print( "port=<number>            # Port number web server, default 8003" )
  print( " " )
  print( "[Start]" )
  print( "url=<url>                # Automatic open url, default http://localhost:{port}/math/index.html" )
  print( "autoopenurl=<True/False> # Enable or disable automatic start url, default True" )
  print( " " )


# https://docs.python.org/3/library/configparser.html
def ReadConfiguration( argv = None ):
  """
  Read the configuration file and set the defaults
  """
  config = configparser.ConfigParser()

  dirRoot = os.path.dirname(os.path.realpath(__file__))

  # initials
  config[ "Path" ] = {}
  config[ "Path" ][ "root"       ] = dirRoot
  config[ "Path" ][ "data"       ] = os.path.join( dirRoot , "data"       )
  config[ "Path" ][ "javascript" ] = os.path.join( dirRoot , "javascript" )
  config[ "Path" ][ "style"      ] = os.path.join( dirRoot , "style"      )
  config[ "Path" ][ "template"   ] = os.path.join( dirRoot , "template"   )
  config[ "Path" ][ "favicon"    ] = os.path.join( dirRoot , "favicon"    )

  config[ "Server" ] = {}
  config[ "Server" ][ "port" ] = "8003"

  config[ "Start" ] = {}
  config[ "Start" ]["url"         ] = "http://localhost:{port}/math/index.html"
  config[ "Start" ]["autoopenurl" ] = "True"
  config[ "Start" ]["starturl"    ] = "/math/index.html"  # used in the application to show a link to the start page

  # Process argv
  hashArg = {}
  if argv != None:
    mode    = ""
    for iCnt in range( 1, len( argv ) ) :
      cArg = argv[ iCnt ]

      if mode != "":
        hashArg[ mode ] = cArg
        mode = ""
        continue

      if cArg == "-p":  # port number
        mode = "port"
        continue

      if cArg == "-u": # start url
        hashArg[ "autoopenurl" ] = True  # if url given the automatic start it
        mode = "url"
        continue

      if cArg == "-a": # auto start url`
        mode = "autoopenurl"
        continue

      if cArg == "-c":  # name ini file`
        mode = "inifilename"
        continue

      if cArg == "-h":
        DisplayHelp()
        return None

      raise NameError( f"Unknown option {cArg}, use -h for help" )



  # read configuration
  if "initfilename" in hashArg:
    configFileName = hashArg[ "initfilename" ]
    if not os.path.isfile(configFileName):
      raise NameError( f"Configuration file {configFileName} not found" )

  else:
    configFileName = os.path.join( dirRoot, "websym3.ini" )

  print( f"Configuration file: {configFileName}" )
  config.read( configFileName )


  # after init read set the commandline arguments
  # pylint:disable=multiple-statements
  if "port"        in hashArg: config[ "Server" ][ "port"        ] = hashArg[ "port"        ]
  if "url"         in hashArg: config[ "Start"  ][ "url"         ] = hashArg[ "url"         ]
  if "autoopenurl" in hashArg: config[ "Start"  ][ "autoopenurl" ] = hashArg[ "autoopenurl" ]

  # with open( configFileName, 'w') as configfile:
  #   config.write(configfile)


  # user/ini-file cannot set this
  config[ "Version" ] = {}
  config[ "Version" ][ "version" ] = __version__

  return config

def CheckConfiguration():
  """
  Check if the configuration is valid
  """
  # read settings, it check it self
  setting = websymexpress3.settingsClass.SettingsClass( GlobalConfig )

  setting.checkCreateDirs()

  return True

#
# https://docs.python.org/3/library/http.server.html
#
# use SimpleHTTPRequestHandler as base for the file handling methods
#
class WebSymexpress3RequestHandler(http.server.SimpleHTTPRequestHandler):
  """
  Http request handler form symexpress3 web interface
  """
  def _defaultError( self ):
    self.send_error( 404, "Unknown file or directory, try /math/index.html" )


  def _request( self ):
    try:

      if GlobalDebug == True:
        print( f"Start request: {self.path}")

      urlpath, _, _ = self.path.partition( '?' )
      urlpath = urllib.parse.unquote(urlpath)

      if urlpath == '/favicon.ico':
        dirPath  = GlobalConfig[ "Path" ]["favicon"]
        ctype    = "image/x-icon"
        filePath = os.path.join( dirPath, "favicon.ico" )
        datatxt  = Path( filePath ).read_bytes()

        self.send_response( 200 )
        self.send_header( "Content-type", ctype)
        self.send_header( "Content-Length", str(  len(datatxt)  ) )

        # dateHeader = email.utils.formatdate(time.time(), usegmt=True)

        # self.send_header( 'Last-modified', dateHeader )
        # self.send_header( 'date'         , dateHeader )  already set by webserver

        # dateHeader = email.utils.formatdate(time.time() + 100, usegmt=True)
        # self.send_header( 'Expires', dateHeader )

        # self.send_header( 'Etag', "e20241006" )

        self.end_headers()

        self.wfile.write( datatxt)
        return


      arrPath = urlpath.split( '/' )
      if len( arrPath ) <= 2 or len( arrPath ) > 4:
        # redirect
        # https://stackoverflow.com/questions/2506932/how-do-i-redirect-a-request-to-a-different-url-in-python
        self.send_response(301)
        self.send_header('Location', "/math/index.html" )
        self.end_headers()
        return

      # javascript and style file handling
      if arrPath[1] in ("javascript", "style" ):
        if self.command != 'GET':
          self.send_error( 404, f"Only GET supported for /{arrPath[1]}/{arrPath[2]}" )
          return

        dirPath  = GlobalConfig[ "Path" ][ arrPath[1] ]
        filePath = os.path.join( dirPath, arrPath[2] )

        if GlobalDebug == True:
          print( f"Filepath: {filePath}" )

        if not os.path.isfile(filePath):
          self.send_error( 404, f"File not found: {arrPath[1]}/{arrPath[2]}" )

        ctype   = self.guess_type(filePath)
        datatxt = Path( filePath ).read_text( 'utf-8' )

        self.send_response( 200 )
        self.send_header( "Content-type", ctype)
        self.send_header( "Content-Length", str(  len(datatxt.encode('utf-8'))  ) )
        self.end_headers()

        self.wfile.write( datatxt.encode('utf-8'))

        return

      # the symexpress3 web interface handling
      if arrPath[1] == "math" :
        if not arrPath[2] in ( "index.html", "index.htm", "index.py" ):
          self._defaultError()
          return

        websymexpress3.HtmlOutput( self, GlobalConfig )
        return

      self._defaultError()
      return

    except Exception as exceptAll: # pylint: disable=broad-exception-caught
      self.send_error( 500, f"Interal error: {exceptAll}" )

    finally:
      if GlobalDebug == True:
        print( f"End request : {self.path}" )

  # pylint:disable=multiple-statements,invalid-name,missing-function-docstring
  def do_GET(   self): self._request()
  def do_POST(  self): self._request()
  def do_PUT(   self): self._request()
  def do_DELETE(self): self._request()


# =================================================
# Main
# =================================================

# read settings
GlobalConfig = ReadConfiguration(sys.argv)
if GlobalConfig == None:
  sys.exit()

# check settings
if CheckConfiguration() != True:
  sys.exit()


# Start http server
server_address = ('', int( GlobalConfig[ 'Server' ]['port'] ) )
GlobalHttpd    = http.server.ThreadingHTTPServer(server_address,WebSymexpress3RequestHandler )


# open start url
if GlobalConfig[ 'Start' ]['autoopenurl'] in ( 'True', 'true', 'Yes', 'yes', 'T', 't', '1' ):
  webbrowser.open_new_tab( GlobalConfig[ 'Start' ]['url'].replace( '{port}', GlobalConfig[ 'Server' ]['port'] ) )


print( "Command line options: python websym3.py -h ")
print( f"Starting httpd server port: {GlobalConfig[ 'Server' ]['port']}")

# wait for ever (or keyboard interrupt)
try:
  GlobalHttpd.serve_forever()
except KeyboardInterrupt:
  pass

print( "Http stop" )
