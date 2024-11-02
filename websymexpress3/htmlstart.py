#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The start html output of WebSymExpress3
"""
#
# https://docs.python.org/3/library/cgi.html
# https://peps.python.org/pep-0594/#cgi
# https://httpd.apache.org/docs/2.4/howto/cgi.html
# https://www.ietf.org/rfc/rfc3875

import os
import sys

from html import escape

from websymexpress3.webcgi   import cgiClass       # https://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django
from websymexpress3          import settingsClass

from websymexpress3.database import dbFormulaClass
from websymexpress3.database import dbThirdpowerClass
from websymexpress3.database import dbFourthpowerClass
from websymexpress3.database import dbGraphClass

from websymexpress3.webhtml  import htmlClass
from websymexpress3.webhtml  import htmlFormulaClass
from websymexpress3.webhtml  import htmlThirdpowerClass
from websymexpress3.webhtml  import htmlFourthpowerClass
from websymexpress3.webhtml  import htmlGraphClass

def HtmlOutput( httpHandler = None, config = None  ):
  """
  Main entry point for WebSymExpress3
  Html output generator. Is called from index.py in the web directory
  """
  # it's always utf-8
  sys.stdout.reconfigure(encoding='utf-8')

  cgi             = cgiClass.CgiClass(             httpHandler )
  settings        = settingsClass.SettingsClass(   config      )
  dbFormula       = dbFormulaClass.DbFormulaClass(             settings )
  dbThirdpower    = dbThirdpowerClass.DbThirdpowerClass(       settings )
  dbFourthpower   = dbFourthpowerClass.DbFourthpowerClass(     settings )
  dbGraph         = dbGraphClass.DbGraphClass(                 settings )
  htmlFormula     = htmlFormulaClass.HtmlFormulaClass(         settings, cgi, dbFormula     )
  htmlThirdpower  = htmlThirdpowerClass.HtmlThirdpowerClass(   settings, cgi, dbThirdpower  )
  htmlFourthpower = htmlFourthpowerClass.HtmlFourthpowerClass( settings, cgi, dbFourthpower )
  htmlGraph       = htmlGraphClass.HtmlGraphClass(             settings, cgi, dbGraph       )

  proglist = {}
  proglist[ "mathInput"   ] = {}
  proglist[ "mathInput"   ][ "name" ] = "Math expression"
  proglist[ "thirdPower"  ] = {}
  proglist[ "thirdPower"  ][ "name" ] = "Cubic equation"
  proglist[ "fourthPower" ] = {}
  proglist[ "fourthPower" ][ "name" ] = "Quartic equation"
  proglist[ "graph"       ] = {}
  proglist[ "graph"       ][ "name" ] = "Graph"
  proglist[ "infoPage"    ] = {}
  proglist[ "infoPage"    ][ "name" ] = "Information"

  prog    = cgi.getUrlParam( 'prog'    )
  key     = cgi.getUrlParam( 'key'     )
  options = cgi.getUrlParam( 'options' )

  settings.currentProgramCode = prog
  if prog in proglist:
    settings.currentProgramName = proglist[ prog ][ "name" ]

  sys.stderr.write( "Prog   : " + str( prog    ) + "\n"  )
  sys.stderr.write( "Key    : " + str( key     ) + "\n"  )
  sys.stderr.write( "Options: " + str( options ) + "\n"  )


  outputPage = ""

  # pylint: disable=multiple-statements
  if   prog == "infoPage"         : outputPage = InfoHtmlPage(cgi, settings)

  elif prog == "mathInput"        : outputPage = htmlFormula.mathInputPage()
  elif prog == "formulaJsonData"  : outputPage = htmlFormula.jsonDataPage( key )
  elif prog == "formulaJsonSave"  : outputPage = htmlFormula.jsonDataSave( options )
  elif prog == "formulaJsonDelete": outputPage = htmlFormula.jsonDataDelete( key )

  elif prog == "thirdPower"          : outputPage = htmlThirdpower.htmlPage()
  elif prog == "thirdpowerJsonData"  : outputPage = htmlThirdpower.jsonDataPage( key )
  elif prog == "thirdpowerJsonSave"  : outputPage = htmlThirdpower.jsonDataSave( options )
  elif prog == "thirdpowerJsonDelete": outputPage = htmlThirdpower.jsonDataDelete( key )

  elif prog == "fourthPower"          : outputPage = htmlFourthpower.htmlPage()
  elif prog == "fourthpowerJsonData"  : outputPage = htmlFourthpower.jsonDataPage( key )
  elif prog == "fourthpowerJsonSave"  : outputPage = htmlFourthpower.jsonDataSave( options )
  elif prog == "fourthpowerJsonDelete": outputPage = htmlFourthpower.jsonDataDelete( key )

  elif prog == "graph"          : outputPage = htmlGraph.mathGraphPage()
  elif prog == "graphJsonList"  : outputPage = htmlGraph.jsonDataList()
  elif prog == "graphJsonData"  : outputPage = htmlGraph.jsonDataPage( key )
  elif prog == "graphJsonSave"  : outputPage = htmlGraph.jsonDataSave( options )
  elif prog == "graphJsonDelete": outputPage = htmlGraph.jsonDataDelete( key )

  # exist/stop application
  elif prog == "exit" :
    # https://stackoverflow.com/questions/35571440/when-is-keyboardinterrupt-raised-in-python
    setattr(httpHandler.server, '_BaseServer__shutdown_request', True)

  else:
    outputPage = StartHtmlPage( cgi, proglist, settings )

  cgi.writeString( outputPage )
  # return ""


def InfoHtmlPage(cgi, settings):
  """
  Generate the html information page
  """
  html = htmlClass.HtmlClass( settings )
  html.addVersionAndCssCommonLink()
  html.addHtmlHeadTitleAndPageHeader()

  html.addCss( '.width100 {' )
  html.addCss( '  width: 100%;' )
  html.addCss( '}' )

  html.addCss( '.bold {' )
  html.addCss( '  font-weight: bold;' )
  html.addCss( '}' )

  html.addBody( '<h2 class="center">Configuration</h2>')

  html.addBody( '<table class="width100">' )
  for key, value in settings.getConfiguration.items():
    if key == "DEFAULT":
      continue

    html.addBody('<tr class="bold">')
    html.addBody('<td>')
    html.addBody( escape( key ) )
    html.addBody('</td>')
    html.addBody('</tr>')

    for key2, value2 in value.items():
      html.addBody('<tr>')

      html.addBody('<td>')
      html.addBody( '&nbsp;&nbsp;&nbsp;' + escape( key2 ) )
      html.addBody('</td>')

      html.addBody('<td>')
      html.addBody( escape( value2 ) )
      html.addBody('</td>')

      html.addBody('</tr>')

  html.addBody( '</table>' )


  html.addBody( '<h2 class="center">Environment variables</h2>')
  html.addBody( '<table>' )

  for key, value in os.environ.items():
    html.addBody('<tr>')

    html.addBody('<td>')
    html.addBody( escape( key ) )
    html.addBody('</td>')

    html.addBody('<td>')
    html.addBody( escape( value ) )
    html.addBody('</td>')

    html.addBody('</tr>')

  html.addBody('<tr>')

  html.addBody('<td>')
  html.addBody( 'stdin' )
  html.addBody('</td>')

  html.addBody('<td>')
  html.addBody( escape( cgi.getBodyAsString() ) )
  html.addBody('</td>')

  html.addBody('</tr>')

  html.addBody( '</table>' )
  return html

# pylint: disable=unused-argument
def StartHtmlPage(cgi, progList, settings):
  """
  Generate the html start/menu page
  """
  html = htmlClass.HtmlClass( settings )

  html.addVersionAndCssCommonLink()
  html.addJavascriptLink( '../javascript/htmlstartPage.js' )

  html.addCss( 'a {' )
  html.addCss( '  text-decoration: none;' )
  html.addCss( '}' )

  html.addCss( 'table.center {' )
  html.addCss( '  margin-left:auto; ' )
  html.addCss( '  margin-right:auto;' )
  html.addCss( '  text-align: left;'  )
  html.addCss( '}' )

  html.addCss( '#tablevert {' )
  html.addCss( '  position: fixed;' )
  html.addCss( '  right   : 47%;' )
  html.addCss( '  top     : 35%;' )
  html.addCss( '  transform: translateY(-50%);' )
  html.addCss( '}' )

  html.addCss( '.titlelist {' )
  html.addCss( '  font-size: 120%;' )
  html.addCss( '}' )

  html.addHead( '<title>SymExpress3</title>' )

  html.addBody( '<table class="center" id="tablevert">' )
  html.addBody( '<tr><td class="titlelist">Symbolic Expression 3</td></tr>' )
  html.addBody( '<tr><td> <br> </td></tr>' )

  for key in progList:
    html.addBody('<tr>')

    html.addBody('<td>')

    if len( progList[ key ]["name"] ) > 0:
      html.addBody( '• <a href="?prog=' + key + '">' + escape( progList[ key ]["name"] ) + '</a>' )
    else:
      html.addBody( '&nbsp;' )
    html.addBody('</td>')

    html.addBody('</tr>')

  html.addBody('<tr>')
  html.addBody('<td>')
  html.addBody('&nbsp;')
  html.addBody('</td>')
  html.addBody('</tr>')

  html.addBody('<tr>')
  html.addBody('<td>')
  html.addBody('<a href="javascript:exitApplication();">Exit</a>')
  html.addBody('</td>')
  html.addBody('</tr>')

  html.addBody( '</table>' )

  return html
