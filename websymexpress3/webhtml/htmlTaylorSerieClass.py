#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Html page for maintain and processing table taylorserie
"""

import sys
import json

from html import escape

from websymexpress3.webhtml  import htmlClass
from websymexpress3.database import dbTaylorSerieClass
from websymexpress3.webjson  import jsonApplicationClass


class HtmlTaylorSerieClass:
  """
  Html page for maintain and processing table taylorserie
  """
  def __init__(self, inSettingsClass, inCgiClass, inDbTaylorSerieClass ):
    self.settings      = inSettingsClass
    self.cgi           = inCgiClass
    self.dbTaylorSerie = inDbTaylorSerieClass

  def jsonDataDelete(self, key):
    """
    Get the delete json and process (delete) the request in the database
    """
    data   = {}
    status = None
    try:
      dataRecord = self.dbTaylorSerie.deleteTaylorSerieDetails( key ) # pylint: disable=unused-variable
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

      dataRecord = dbTaylorSerieClass.RecordTaylorSerie()
      dataRecord.name        = jsonData[ 'name'        ]
      # dataRecord.description = jsonData[ 'description' ]
      dataRecord.htmlDisplay = None
      dataRecord.formula     = jsonData[ 'formula'   ]
      dataRecord.steps       = jsonData[ 'steps'     ]
      dataRecord.baseValue   = jsonData[ 'baseValue' ]
      dataRecord.diffVar     = jsonData[ 'diffVar'   ]

      dataRecord = self.dbTaylorSerie.saveTaylorSerieDetails( dataRecord )

      if options == "calc":
        dataRecord = self.dbTaylorSerie.calcTaylorSerieDetails( dataRecord.name )

      data = {
        "name"        : dataRecord.name        ,
        # "description" : dataRecord.description ,
        "htmlDisplay" : dataRecord.htmlDisplay ,
        "formula"     : dataRecord.formula     ,
        "steps"       : dataRecord.steps       ,
        "baseValue"   : dataRecord.baseValue   ,
        "diffVar"     : dataRecord.diffVar
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
    Get the json request to get third power data for a given key
    """
    jsonClass  = jsonApplicationClass.JsonApplicationClass()
    dataRecord = self.dbTaylorSerie.getTaylorSerieDetails( key )

    # this go to the outside world. no auto copy all fields
    data = {
      "name"        : dataRecord.name        ,
      "description" : dataRecord.description ,
      "htmlDisplay" : dataRecord.htmlDisplay ,
      "formula"     : dataRecord.formula     ,
      "steps"       : dataRecord.steps       ,
      "baseValue"   : dataRecord.baseValue   ,
      "diffVar"     : dataRecord.diffVar
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
      html.addBody( '<textarea id="inputFieldFormula" class="inputText"></textarea>' )
      html.addBody( '</div>' )

      # input parameters steps, baseValue and diffVar

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldSteps" class="labelWidth">Steps</label>' )
      html.addBody( '<input id="inputFieldSteps" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldBaseValue" class="labelWidth">Point</label>' )
      html.addBody( '<input id="inputFieldBaseValue" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldDiffVar" class="labelWidth">Variable</label>' )
      html.addBody( '<input id="inputFieldDiffVar" class="inputWidth" type="text" value="">' )
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
    html.addHtmlHeadTitleAndPageHeader()
    html.addFlexCss()

    html.addCssLink(        '../style/taylorSeriePage.css'     )
    html.addJavascriptLink( '../javascript/taylorSeriePage.js' )

    # flex container
    html.addBody( '<div class="divPageContainer">' )

    # list of all the entries
    listNames = self.dbTaylorSerie.listTaylorSeries()

    html.addBody( '<div class="inputSelect resizer">' )
    html.addBody( '<select name="selectMathTaylorSerie" id="selectMathTaylorSerie" size="20">' )
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
