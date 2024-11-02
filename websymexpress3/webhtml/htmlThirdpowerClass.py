#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Html page for maintain and processing table third power (cubic equation)
"""

import sys
import json

from html import escape

from websymexpress3.webhtml  import htmlClass
from websymexpress3.database import dbThirdpowerClass
from websymexpress3.webjson  import jsonApplicationClass


class HtmlThirdpowerClass:
  """
  Html page for maintain and processing table third power
  """
  def __init__(self, inSettingsClass, inCgiClass, inDbThirdpowerClass ):
    self.settings     = inSettingsClass
    self.cgi          = inCgiClass
    self.dbThirdpower = inDbThirdpowerClass

  def jsonDataDelete(self, key):
    """
    Get the delete json and process (delete) the request in the database
    """
    data   = {}
    status = None
    try:
      dataRecord = self.dbThirdpower.deleteThirdpowerDetails( key ) # pylint: disable=unused-variable
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

      dataRecord = dbThirdpowerClass.RecordThirdpower()
      dataRecord.name        = jsonData[ 'name'        ]
      dataRecord.description = jsonData[ 'description' ]
      dataRecord.htmlDisplay = None
      dataRecord.a           = jsonData[ 'a' ]
      dataRecord.b           = jsonData[ 'b' ]
      dataRecord.c           = jsonData[ 'c' ]
      dataRecord.d           = jsonData[ 'd' ]
      dataRecord.calcValue   = jsonData[ 'calcValue' ] # Calc the real value of the formula

      dataRecord = self.dbThirdpower.saveThirdpowerDetails( dataRecord )

      if options == "calc":
        dataRecord = self.dbThirdpower.calcThirdpowerDetails( dataRecord.name )

      data = {
        "name"        : dataRecord.name        ,
        "description" : dataRecord.description ,
        "htmlDisplay" : dataRecord.htmlDisplay ,
        "a"           : dataRecord.a           ,
        "b"           : dataRecord.b           ,
        "c"           : dataRecord.c           ,
        "d"           : dataRecord.d           ,
        "calcValue"   : dataRecord.calcValue
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
    dataRecord = self.dbThirdpower.getThirdpowerDetails( key )

    # this go to the outside world. no auto copy all fields
    data = {
      "name"        : dataRecord.name        ,
      "description" : dataRecord.description ,
      "htmlDisplay" : dataRecord.htmlDisplay ,
      "a"           : dataRecord.a           ,
      "b"           : dataRecord.b           ,
      "c"           : dataRecord.c           ,
      "d"           : dataRecord.d           ,
      "calcValue"   : dataRecord.calcValue
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
      html.addBody( '<label for="inputFieldCode labelWidth">Code</label>' )
      html.addBody( '<input id="inputFieldCode" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      # input extra information
      html.addBody( '<div class="inputDescription">' )
      html.addBody( '<textarea id="inputFieldDescription" class="inputText"></textarea>' )
      html.addBody( '</div>' )

      # input parameters a, b, c and d
      html.addBody( '<div class="inputField">' )
      html.addBody( 'a x^3 + b x^2 + c x + d = 0' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldA labelWidth">a</label>' )
      html.addBody( '<input id="inputFieldA" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldB labelWidth">b</label>' )
      html.addBody( '<input id="inputFieldB" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldC labelWidth">c</label>' )
      html.addBody( '<input id="inputFieldC" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      html.addBody( '<div class="inputField">' )
      html.addBody( '<label for="inputFieldD labelWidth">d</label>' )
      html.addBody( '<input id="inputFieldD" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      # toggle box to calc the real value
      html.addBody( '<div class="inputFormulaOptions">' )
      html.addBody('<input type="checkbox" id="inputFormulaCalc" name="inputFormulaCalc" value="Calc">' )
      html.addBody('<label for="inputFormulaCalc">Calculate real values</label>' )
      html.addBody( '</div>' )

      # footer input = save, calc and delete buttons
      html.addBody( '<div class="inputFormulaFooter">' )
      html.addBody( '<button type="button" id="buttonSave" class="buttonVericalCenter">Save</button> ' )
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

    html.addCssLink(        '../style/thirdPowerPage.css'     )
    html.addJavascriptLink( '../javascript/thirdPowerPage.js' )

    # flex container
    html.addBody( '<div class="divPageContainer">' )

    # list of all the entries
    listNames = self.dbThirdpower.listThirdpowers()

    html.addBody( '<div class="inputSelect resizer">' )
    html.addBody( '<select name="selectMathThirdpower" id="selectMathThirdpower" size="20">' )
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
