#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Html page for maintain and processing table formula
"""
import json

from html import escape

from websymexpress3.webhtml  import htmlClass
from websymexpress3.database import dbFormulaClass
from websymexpress3.webjson  import jsonApplicationClass


class HtmlFormulaClass:
  """
  Html page for maintain and processing table formula
  """
  def __init__(self, inSettingsClass, inCgiClass, inDbFormulaClass ):
    self.settings  = inSettingsClass
    self.cgi       = inCgiClass
    self.dbFormula = inDbFormulaClass

  def jsonDataDelete(self, key):
    """
    Get the delete json and process (delete) the request in the database
    """
    data   = {}
    status = None
    try:
      dataRecord = self.dbFormula.deleteFormualDetails( key ) # pylint: disable=unused-variable

      data = {
        "message"        : "Record deleted"
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
      jsonData   = json.loads(jsonString)

      dataRecord = dbFormulaClass.RecordFormula()
      dataRecord.name          = jsonData[ 'name'         ]
      dataRecord.formula       = jsonData[ 'formula'      ]
      dataRecord.htmlDisplay   = None
      dataRecord.optimizeType  = jsonData[ 'optimizeType' ] # the optimize type
      dataRecord.calcValue     = jsonData[ 'calcValue'    ] # Calc the real value of the formula
      dataRecord.replaceValue  = jsonData[ 'replaceValue' ]
      dataRecord.optimizeList  = jsonData[ 'optimizeList' ] # Array of optimze actions for optimizeType OptimizeCustom
      dataRecord.varList       = jsonData[ 'varList'      ] # Dictionary of variables (varname, value)

      dataRecord = self.dbFormula.saveFormualDetails( dataRecord )

      if options == "calc":
        dataRecord = self.dbFormula.calcFormualDetails( dataRecord.name )

      data = {
        "name"        : dataRecord.name        ,
        "formula"     : dataRecord.formula     ,
        "htmlDisplay" : dataRecord.htmlDisplay ,
        "optimizeType": dataRecord.optimizeType,
        "calcValue"   : dataRecord.calcValue   ,
        "replaceValue": dataRecord.replaceValue,
        "optimizeList": dataRecord.optimizeList,
        "varList"     : dataRecord.varList

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
    Get the json request to get formula data for a given key
    """
    jsonClass  = jsonApplicationClass.JsonApplicationClass()
    dataRecord = self.dbFormula.getFormulaDetails( key )

    # this go to the outside world. no auto copy all fields
    data = {
      "name"        : dataRecord.name        ,
      "formula"     : dataRecord.formula     ,
      "htmlDisplay" : dataRecord.htmlDisplay ,
      "optimizeType": dataRecord.optimizeType,
      "calcValue"   : dataRecord.calcValue   ,
      "replaceValue": dataRecord.replaceValue,
      "optimizeList": dataRecord.optimizeList,
      "varList"     : dataRecord.varList
    }

    jsonString = json.dumps(data)

    jsonClass.setJsonString( jsonString )

    return jsonClass


  def mathInputPage(self):
    """
    Create the maintain html page
    """

    def AddInputFormulaDiv():

      html.addBody( '<div class="inputFormulaContainer">' )

      # input code and description
      html.addBody( '<div class="inputFormulaHeader">' )
      html.addBody( '<label for="inputFieldCode" class="labelWidth">Code</label>' )
      html.addBody( '<input id="inputFieldCode" class="inputWidth" type="text" value="">' )
      html.addBody( '</div>' )

      # pulldown menu variables and functions
      html.addBody( '<div class="inputFormulaPullDownMenu">' )

      html.addBody( '<div class="dropdown">' )
      html.addBody( '  <button onclick="fncOpenDropDownMenu(' + "'menuVariables'" + ')" class="dropbtn">Fixed variables</button>' )
      html.addBody( '  <div id="menuVariables" class="dropdown-content">' )

      arrVariables = self.dbFormula.getVariables()
      for objOptimze in arrVariables :
        html.addBody( '<a href="#" onclick="fncAddText(' + "'" + objOptimze[ 'code' ] + "'" + ')">' + objOptimze[ 'code' ] + ' = ' + escape( objOptimze[ 'description' ] ) + '</a>' )

      html.addBody( '  </div>' )
      html.addBody( '</div> ' )

      html.addBody( '<div class="dropdown">' )
      html.addBody( '  <button onclick="fncOpenDropDownMenu(' + "'menuFunctions'" + ')" class="dropbtn">Functions</button>' )
      html.addBody( '  <div id="menuFunctions" class="dropdown-content">' )
      arrVariables = self.dbFormula.getFunctions()
      for objOptimze in arrVariables :
        html.addBody( '<a href="#" onclick="fncAddText(' + "'" + objOptimze[ 'code' ] + "'" + ')">' + escape( objOptimze[ 'description' ] ) + '</a>' )

      html.addBody( '  </div>' )
      html.addBody( '</div> ' )
      html.addBody( '</div>' )

      # input area formula (as text)
      html.addBody( '<div class="inputFormulaContent">' )
      html.addBody( '<textarea id="inputFieldFormula" class="inputFormulaText"></textarea>' )
      html.addBody( '</div>' )

      # options section, html-table is used for all the options
      html.addBody( '<div class="inputFormulaOptions">' )

      html.addBody( '<table>' )
      html.addBody( '<tr>' )

      html.addBody( '<td class="optBigSelectActionHide">' )
      html.addBody( '<label>Optimization</label>' )
      html.addBody( '</td>' )

      # . optimization type
      html.addBody( '<td class="optBigSelectActionHide">'  )
      html.addBody( '<select id="inputFieldCalcType" name="inputFieldCalcType">' )
      arrOptimize = self.dbFormula.getOptimzeTypes()
      for objOptimze in arrOptimize :
        html.addBody( '<option value="' + objOptimze[ 'code' ] + '">' + escape( objOptimze[ 'description' ] ) + '</option>' )
      html.addBody( '</select>' )
      html.addBody( '</td>' )

      # . add/change variable
      html.addBody( '<td rowspan="4" class="tdButtonSelectVariable optBigSelectActionHide" >' )

      html.addBody( '<button type="button" id="buttonSelectVariableAdd"    >&gt;</button> ' )
      html.addBody( '<br>' )
      html.addBody( '<button type="button" id="buttonSelectVariableRemove" >&lt;</button> ' )

      html.addBody( '</td>' )

      # . list of variables
      html.addBody( '<td rowspan="4" class="optBigSelectActionHide">' )
      html.addBody( '<select id="selectVariable" name="selectVariable" size="4" class="widthSelectOptimzeCustom height100">' )
      html.addBody( '</select>' )
      html.addBody( '</td>' )

      # . list of all optimization actions
      html.addBody( '<td rowspan="4" class=optBigSelectActionExpand">' )
      html.addBody( '<select id="inputFieldOptimzeCustom" name="inputFieldOptimzeCustom" size="4" class="widthSelectOptimzeCustom height100">' )
      arrCustom = self.dbFormula.getOptimzeCustoms()
      for objOptimze in arrCustom :
        html.addBody( '<option value="' + objOptimze[ 'code' ] + '" title="' + escape( objOptimze[ 'description' ] ) + '">' + escape( objOptimze[ 'code' ] + ' - ' + objOptimze[ 'description' ] ) + '</option>' )
      html.addBody( '</select>' )
      html.addBody( '</td>' )

      # . buttons to add/remove optimization action
      html.addBody( '<td rowspan="4" class="tdButtonSelectOptimzeCustom">' )
      html.addBody( '<button type="button" id="buttonInputFieldAddCustom"    >&gt;</button> ' )
      html.addBody( '<br>' )
      html.addBody( '<button type="button" id="buttonInputFieldRemoveCustom" >&lt;</button> ' )
      html.addBody( '</td>' )

      # . list of selected optimization actions
      html.addBody( '<td rowspan="4" class=optBigSelectActionExpand">' )
      html.addBody( '<select id="inputFieldOptimzeSelected" name="inputFieldOptimzeSelected" size="4" class="widthSelectOptimzeCustom height100">' )
      html.addBody( '</select>' )
      html.addBody( '</td>' )

      # . button to move selected optimization actions up/down
      html.addBody( '<td rowspan="4" class="tdButtonSelectOptimzeCustom" >' )

      html.addBody('<input type="checkbox" id="checkBoxInputFieldBigCustom" name="inputFormulaBigAction" value="big" title="Make the selection big">' )
      html.addBody( '<br>' )
      html.addBody( '<button type="button" id="buttonInputFieldUpCustom"    >&uarr;</button> ' )
      html.addBody( '<br>' )
      html.addBody( '<button type="button" id="buttonInputFieldDownCustom" >&darr;</button> ' )
      html.addBody( '</td>' )

      html.addBody( '</tr>' )
      html.addBody( '<tr class="optBigSelectActionHide">'  )

      # empty
      html.addBody( '<td></td>' )

      # check boxes (calculate real values and replace variables)
      html.addBody( '<td>' )
      html.addBody('<input type="checkbox" id="inputFormulaCalc" name="inputFormulaCalc" value="Calc">' )
      html.addBody('<label for="inputFormulaCalc">Calc</label>' )
      html.addBody('<input type="checkbox" id="inputFormulaReplace" name="inputFormulaReplace" value="Replace">' )
      html.addBody('<label for="inputFormulaCalc">Replace</label>' )
      html.addBody( '</td>' )

      html.addBody( '</tr>' )

      # input variable
      html.addBody( '<tr class="optBigSelectActionHide">'  )

      html.addBody( '<td>' )
      html.addBody('<label for="inputFormulaVarName">Variable</label>' )
      html.addBody( '</td>' )

      html.addBody( '<td>' )
      html.addBody( '<input id="inputFormulaVarName" name="inputFormulaVarName" type="text" value="">' )
      html.addBody( '</td>' )

      html.addBody( '</tr>' )

      # input value (of variable)
      html.addBody( '<tr class="optBigSelectActionHide">'  )

      html.addBody( '<td>' )
      html.addBody('<label for="inputFormulaVarValue">Value</label>' )
      html.addBody( '</td>' )

      html.addBody( '<td>' )
      html.addBody( '<input id="inputFormulaVarValue" name="inputFormulaVarValue" type="text" value="">' )
      html.addBody( '</td>' )

      html.addBody( '</tr>' )

      # end table for all the options
      html.addBody( '</table>' )
      html.addBody( '</div>' ) # inputFormulaOptions

      # footer buttons, save, calculate and delete
      html.addBody( '<div class="inputFormulaFooter optBigSelectActionHide">' )
      html.addBody( '<button type="button" id="buttonSave" class="buttonVericalCenter">Save</button> ' )
      html.addBody( '<button type="button" id="buttonSaveCalc" class="buttonVericalCenter">Calculate</button> ' )
      html.addBody( '<div class="buttonRight">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>' )  # filler for resize div
      html.addBody( '<button type="button" id="buttonDelete" class="buttonVericalCenter buttonRight">Delete</button> ' )
      html.addBody( '</div>' )

      html.addBody( '</div>' ) # container input fields


    # start build html
    html = htmlClass.HtmlClass( self.settings )

    html.addVersionAndCssCommonLink()
    html.addHtmlHeadTitleAndPageHeader()
    html.addFlexCss()

    html.addCssLink(        '../style/mathInputPage.css'     )
    html.addJavascriptLink( '../javascript/mathInputPage.js' )

    # flex container
    html.addBody( '<div class="divPageContainer">' )

    # list of formulas
    listFormulas = self.dbFormula.listFomrulas()
    html.addBody( '<div class="inputSelect resizer">' )
    html.addBody( '<select name="selectMathFormula" id="selectMathFormula" size="20">' )
    for nameFormula in listFormulas :
      html.addBody( '  <option value="' + escape(nameFormula) + '" title="' + escape(nameFormula) + '">' + escape(nameFormula) + '</option>' )
    html.addBody( '</select>' )
    html.addBody( '</div>' )

    # right div
    html.addBody( '<div class="divRight">' )

    # input data
    html.addBody( '<div class="inputForm resizer">' )
    AddInputFormulaDiv()
    html.addBody( '</div>' )

    # output result = html page in iframe
    html.addBody( '<div class="inputIFrame resizer">' )
    # https://stackoverflow.com/questions/8117761/how-can-i-make-an-iframe-resizable
    html.addBody( '  <iframe id="iframeDisplayFormula" class="resized" src="about:blank"></iframe>')
    html.addBody( '</div>' )


    html.addBody( '</div>' ) # divRight

    html.addBody( '</div>' ) # flex container

    # indeling met divs
    # https://stackoverflow.com/questions/20351138/html-and-css-2-divs-on-left-1-independent-div-on-right

    return html
