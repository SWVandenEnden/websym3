#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The start HTML output of WebSymExpress3
"""
#
# https://docs.python.org/3/library/cgi.html
# https://peps.python.org/pep-0594/#cgi
# https://httpd.apache.org/docs/2.4/howto/cgi.html
# https://www.ietf.org/rfc/rfc3875

import os
import sys

from html import escape

import symexpress3
import cubicequation
import quarticequation
import sym3taylorserie
import sym3resultant
import sym3tschirnhaus

from websymexpress3.webcgi   import cgiClass       # https://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django
from websymexpress3          import settingsClass

from websymexpress3.database import dbFormulaClass
from websymexpress3.database import dbResultantClass
from websymexpress3.database import dbTaylorSerieClass
from websymexpress3.database import dbThirdpowerClass
from websymexpress3.database import dbFourthpowerClass
from websymexpress3.database import dbTschirnhausClass
from websymexpress3.database import dbGraphClass

from websymexpress3.webhtml  import htmlClass
from websymexpress3.webhtml  import htmlFormulaClass
from websymexpress3.webhtml  import htmlResultantClass
from websymexpress3.webhtml  import htmlTaylorSerieClass
from websymexpress3.webhtml  import htmlThirdpowerClass
from websymexpress3.webhtml  import htmlFourthpowerClass
from websymexpress3.webhtml  import htmlTschirnhausClass
from websymexpress3.webhtml  import htmlGraphClass

def HtmlOutput( httpHandler = None, config = None  ):
  """
  Main entry point for WebSymExpress3
  HTML output generator. Is called from ..\\websym3.py WebSymexpress3RequestHandler()  (search for websymexpress3.HtmlOutput)
  """
  # it's always utf-8
  sys.stdout.reconfigure(encoding='utf-8')

  cgi             = cgiClass.CgiClass(             httpHandler )
  settings        = settingsClass.SettingsClass(   config      )
  dbFormula       = dbFormulaClass.DbFormulaClass(             settings )
  dbResultant     = dbResultantClass.DbResultantClass(         settings )
  dbTaylorSerie   = dbTaylorSerieClass.DbTaylorSerieClass(     settings )
  dbThirdpower    = dbThirdpowerClass.DbThirdpowerClass(       settings )
  dbFourthpower   = dbFourthpowerClass.DbFourthpowerClass(     settings )
  dbTschirnhaus   = dbTschirnhausClass.DbTschirnhausClass(     settings )
  dbGraph         = dbGraphClass.DbGraphClass(                 settings )
  htmlFormula     = htmlFormulaClass.HtmlFormulaClass(         settings, cgi, dbFormula     )
  htmlResultant   = htmlResultantClass.HtmlResultantClass(     settings, cgi, dbResultant   )
  htmlTaylorSerie = htmlTaylorSerieClass.HtmlTaylorSerieClass( settings, cgi, dbTaylorSerie )
  htmlThirdpower  = htmlThirdpowerClass.HtmlThirdpowerClass(   settings, cgi, dbThirdpower  )
  htmlFourthpower = htmlFourthpowerClass.HtmlFourthpowerClass( settings, cgi, dbFourthpower )
  htmlTschirnhaus = htmlTschirnhausClass.HtmlTschirnhausClass( settings, cgi, dbTschirnhaus )
  htmlGraph       = htmlGraphClass.HtmlGraphClass(             settings, cgi, dbGraph       )

  proglist = {}
  proglist[ "mathInput"   ] = {}
  proglist[ "mathInput"   ][ "name" ] = "Math expression"
  proglist[ "taylorSerie" ] = {}
  proglist[ "taylorSerie" ][ "name" ] = "Taylor serie"
  proglist[ "thirdPower"  ] = {}
  proglist[ "thirdPower"  ][ "name" ] = "Cubic equation"
  proglist[ "fourthPower" ] = {}
  proglist[ "fourthPower" ][ "name" ] = "Quartic equation"
  proglist[ "resultant"   ] = {}
  proglist[ "resultant"   ][ "name" ] = "Resultant"
  proglist[ "tschirnhaus" ] = {}
  proglist[ "tschirnhaus" ][ "name" ] = "Tschirnhaus transformation"
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
  match prog:
    case "infoPage"             : outputPage = InfoHtmlPage(cgi, settings)

    case "mathInput"            : outputPage = htmlFormula.mathInputPage()
    case "formulaJsonData"      : outputPage = htmlFormula.jsonDataPage(   key     )
    case "formulaJsonSave"      : outputPage = htmlFormula.jsonDataSave(   options )
    case "formulaJsonDelete"    : outputPage = htmlFormula.jsonDataDelete( key     )

    case "thirdPower"           : outputPage = htmlThirdpower.htmlPage()
    case "thirdpowerJsonData"   : outputPage = htmlThirdpower.jsonDataPage(   key     )
    case "thirdpowerJsonSave"   : outputPage = htmlThirdpower.jsonDataSave(   options )
    case "thirdpowerJsonDelete" : outputPage = htmlThirdpower.jsonDataDelete( key     )

    case "resultant"            : outputPage = htmlResultant.htmlPage()
    case "resultantJsonData"    : outputPage = htmlResultant.jsonDataPage(   key     )
    case "resultantJsonSave"    : outputPage = htmlResultant.jsonDataSave(   options )
    case "resultantJsonDelete"  : outputPage = htmlResultant.jsonDataDelete( key     )

    case "taylorSerie"          : outputPage = htmlTaylorSerie.htmlPage()
    case "taylorSerieJsonData"  : outputPage = htmlTaylorSerie.jsonDataPage(   key     )
    case "taylorSerieJsonSave"  : outputPage = htmlTaylorSerie.jsonDataSave(   options )
    case "taylorSerieJsonDelete": outputPage = htmlTaylorSerie.jsonDataDelete( key     )

    case "fourthPower"          : outputPage = htmlFourthpower.htmlPage()
    case "fourthpowerJsonData"  : outputPage = htmlFourthpower.jsonDataPage(   key     )
    case "fourthpowerJsonSave"  : outputPage = htmlFourthpower.jsonDataSave(   options )
    case "fourthpowerJsonDelete": outputPage = htmlFourthpower.jsonDataDelete( key     )

    case "tschirnhaus"          : outputPage = htmlTschirnhaus.htmlPage()
    case "tschirnhausJsonData"  : outputPage = htmlTschirnhaus.jsonDataPage(   key     )
    case "tschirnhausJsonSave"  : outputPage = htmlTschirnhaus.jsonDataSave(   options )
    case "tschirnhausJsonDelete": outputPage = htmlTschirnhaus.jsonDataDelete( key     )

    case "graph"                : outputPage = htmlGraph.mathGraphPage()
    case "graphJsonList"        : outputPage = htmlGraph.jsonDataList()
    case "graphJsonData"        : outputPage = htmlGraph.jsonDataPage(   key     )
    case "graphJsonSave"        : outputPage = htmlGraph.jsonDataSave(   options )
    case "graphJsonDelete"      : outputPage = htmlGraph.jsonDataDelete( key     )

    case "exit" :
      # exist/stop application
      # https://stackoverflow.com/questions/35571440/when-is-keyboardinterrupt-raised-in-python
      setattr(httpHandler.server, '_BaseServer__shutdown_request', True)

    case _:
      outputPage = StartHtmlPage( cgi, proglist, settings )

  cgi.writeString( outputPage )
  # return ""


def InfoHtmlPage(cgi, settings):
  """
  Generate the html information page
  """
  def _addVersion( html, title, version ):
    html.addBody('<tr>')

    html.addBody('<td>')
    html.addBody( escape( title ) )
    html.addBody('</td>')

    html.addBody('<td>&nbsp;&nbsp;</td>')

    html.addBody('<td>')
    html.addBody( escape( version ) )
    html.addBody('</td>')

    html.addBody('</tr>')

  html = htmlClass.HtmlClass( settings )
  html.addVersionAndCssCommonLink()
  html.addHtmlHeadTitleAndPageHeader()

  html.addCss( '.width100 {' )
  html.addCss( '  width: 100%;' )
  html.addCss( '}' )

  html.addCss( '.bold {' )
  html.addCss( '  font-weight: bold;' )
  html.addCss( '}' )

  html.addBody( '<h2 class="center">Versions</h2>')

  html.addBody( '<table>' )
  _addVersion( html, 'websym3'        , settings.version            )
  _addVersion( html, 'symexpress3'    , symexpress3.__version__     )
  _addVersion( html, 'cubicequation'  , cubicequation.__version__   )
  _addVersion( html, 'quarticequation', quarticequation.__version__ )
  _addVersion( html, 'sym3taylorserie', sym3taylorserie.__version__ )
  _addVersion( html, 'sym3resultant'  , sym3resultant.__version__   )
  _addVersion( html, 'sym3tschirnhaus', sym3tschirnhaus.__version__ )

  html.addBody( '</table>' )


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
