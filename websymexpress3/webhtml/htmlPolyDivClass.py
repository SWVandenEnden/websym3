#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Html page for maintain and processing table polydiv
"""

import sys
import json

from html import escape

from websymexpress3.webhtml  import htmlClass
from websymexpress3.database import dbPolyDivClass
from websymexpress3.webjson  import jsonApplicationClass


class HtmlPolyDivClass:
  """
  Html page for maintain and processing table polydiv
  """
  def __init__(self, inSettingsClass, inCgiClass, inDbPolyDivClass ):
    self.settings    = inSettingsClass
    self.cgi         = inCgiClass
    self.dbPolyDiv   = inDbPolyDivClass

  def jsonDataDelete(self, key):
    """
    Get the delete json and process (delete) the request in the database
    """
    data   = {}
    status = None
    try:
      dataRecord = self.dbPolyDiv.deletePolyDivDetails( key ) # pylint: disable=unused-variable
      data = {
        "message" : "Record deleted"
      }
    except OSError as err:
      data = {
        "error" : "OS error: " + str( err )
      }
      status = "error"

    except Exception as err: # pylint: disable=broad-exception-caught
      data = {
         "error" : str( err )
      }
      status = "error"

    jsonString = json.dumps(data)
    jsonClass  = jsonApplicationClass.JsonApplicationClass()

    if status == "error" :
      jsonClass.setHeaderVar( 'Status', '400 Bad Request')

    jsonClass.setJsonString( jsonString )

    return jsonClass


  def jsonDataSave(self, options):
    """
    Get the save json (create & update) and process them into the database
    """
    data   = {}
    status = None
    try:
      jsonString = self.cgi.getBodyAsString()

      sys.stderr.write( "jsonDataSave: " + jsonString  + "\n"  )

      jsonData = json.loads(jsonString)

      dataRecord = dbPolyDivClass.RecordPolyDiv()
      dataRecord.name        = jsonData[ 'name'        ]
      # dataRecord.description = jsonData[ 'description' ]
      dataRecord.htmlDisplay = None
      dataRecord.formula1    = jsonData[ 'formula1'   ]
      dataRecord.formula2    = jsonData[ 'formula2'   ]
      dataRecord.variable    = jsonData[ 'variable'   ]

      dataRecord = self.dbPolyDiv.savePolyDivDetails( dataRecord )

      if options == "calc":
        dataRecord = self.dbPolyDiv.calcPolyDivDetails( dataRecord.name )

      data = {
        "name"        : dataRecord.name        ,
        # "description" : dataRecord.description ,
        "htmlDisplay" : dataRecord.htmlDisplay ,
        "formula1"     : dataRecord.formula1   ,
        "formula2"     : dataRecord.formula2   ,
        "variable"     : dataRecord.variable
      }
    except OSError as err:
      data = {
        "error" : "OS error: " + str( err )
      }
      status = "error"

    except Exception as err: # pylint: disable=broad-exception-caught
      data = {
         "error" : str( err )
      }
      status = "error"

    jsonString = json.dumps(data)
    jsonClass  = jsonApplicationClass.JsonApplicationClass()

    if status == "error" :
      jsonClass.setHeaderVar( 'Status', '400 Bad Request')

    jsonClass.setJsonString( jsonString )

    return jsonClass


  def jsonDataPage(self, key):
    """
    Get the json request to get data for a given key
    """
    jsonClass  = jsonApplicationClass.JsonApplicationClass()
    dataRecord = self.dbPolyDiv.getPolyDivDetails( key )

    # this go to the outside world. no auto copy all fields
    data = {
      "name"        : dataRecord.name        ,
      "description" : dataRecord.description ,
      "htmlDisplay" : dataRecord.htmlDisplay ,
      "formula1"    : dataRecord.formula1    ,
      "formula2"    : dataRecord.formula2    ,
      "variable"    : dataRecord.variable
    }

    jsonString = json.dumps(data)

    jsonClass.setJsonString( jsonString )

    return jsonClass


  def htmlPage(self):
    """
    Create the maintain html page
    """

    def AddInputDiv():
      html.addBody( '<div class="inputFormulaContainer">' )

      # input code and description
      html.addBody( '<div class="inputFormulaHeader">' )
      html.addBody( '<label for="inputFieldCode" class="labelWidth">Code</label>' )
      html.addBody( '<input id="inputFieldCode" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      # input extra information
      html.addBody( '<div class="inputFormula">' )
      html.addBody( '<textarea id="inputFieldFormula1" class="inputText"></textarea>' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputFormula">' )
      html.addBody( '<textarea id="inputFieldFormula2" class="inputText"></textarea>' )
      html.addBody( '</div>' )

      # input parameters steps, baseValue and diffVar

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldVariable" class="labelWidth">Variable</label>' )
      html.addBody( '<input id="inputFieldVariable" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )



      # footer input = save, calc and delete buttons
      html.addBody( '<div class="inputFormulaFooter">' )
      html.addBody( '<button type="button" id="buttonSave"     class="buttonVericalCenter">Save</button> ' )
      html.addBody( '<button type="button" id="buttonSaveCalc" class="buttonVericalCenter">Calculate</button> ' )
      html.addBody( '<div class="buttonRight">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>' )  # filler for resize div
      html.addBody( '<button type="button" id="buttonDelete" class="buttonVericalCenter buttonRight">Delete</button> ' )
      html.addBody( '</div>' )

      html.addBody( '</div>' ) # div input container

    # start html build
    html = htmlClass.HtmlClass( self.settings )
    html.addVersionAndCssCommonLink()
    html.addHtmlHeadTitleAndPageHeader( "Polynomial division" )
    html.addFlexCss()

    html.addCssLink(        '../style/polydivPage.css'     )
    html.addJavascriptLink( '../javascript/polydivPage.js' )

    # flex container
    html.addBody( '<div class="divPageContainer">' )

    # list of all the entries
    listNames = self.dbPolyDiv.listPolyDivs()

    html.addBody( '<div class="inputSelect resizer">' )
    html.addBody( '<select name="selectMathPolyDiv" id="selectMathPolyDiv" size="20">' )
    for name in listNames :
      html.addBody( '  <option value="' + escape(name) + '" title="' + escape(name) + '">' + escape(name) + '</option>' )
    html.addBody( '</select>' )
    html.addBody( '</div>' )

    # right div for input data and display result
    html.addBody( '<div class="divRight">' )

    # data input
    html.addBody( '<div class="inputForm resizer">' )
    AddInputDiv()
    html.addBody( '</div>' )

    # iframe for display result = html page
    html.addBody( '<div class="inputIFrame resizer">' )
    html.addBody( '  <iframe id="iframeDisplay" class="resized" src="about:blank"></iframe>')
    html.addBody( '</div>' )

    html.addBody( '</div>' ) # divRight

    html.addBody( '</div>' )
    # https://stackoverflow.com/questions/20351138/html-and-css-2-divs-on-left-1-independent-div-on-right

    return html
