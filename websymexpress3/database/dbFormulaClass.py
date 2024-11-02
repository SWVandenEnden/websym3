#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database handling for table formula
"""
import json
import os
import collections

from pathlib  import Path
from datetime import datetime

import symexpress3
import symexpress3.symtables

#
# Record definition formula
#
class RecordFormula:  # pylint: disable=too-few-public-methods
  """
  Data record for table formula
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.formula          = ""    # the formula (symexpress3)
    self.htmlDisplay      = ""    # the html file (no link) of the formula
    self.optimizeType     = ""    # the optimize type
    self.calcValue        = False # Calc the real value of the formula
    self.replaceValue     = False # Replace the variables
    self.optimizeList     = []    # Array of optimize actions for optimizeType OptimizeCustom
    self.varList          = {}    # Dictionary of variable

  # special method too check all data types of all the fields...
  def checkDataType(self):
    """
    Check all the fields datatype
    """
    if isinstance( self.name, str ) != True:
      raise NameError( f'Field "name" is not of type string ({type(self.name)})' )

    if self.formula != None and isinstance( self.formula, str ) != True:
      raise NameError( f'Field "formula" is not of type string ({type(self.formula)})' )

    if self.htmlDisplay != None and isinstance( self.htmlDisplay, str ) != True:
      raise NameError( f'Field "htmlDisplay" is not of type string ({type(self.htmlDisplay)})' )

    if self.optimizeType != None and isinstance( self.optimizeType, str ) != True:
      raise NameError( f'Field "optimizeType" is not of type string ({type(self.optimizeType)})' )

    if self.calcValue != None and isinstance( self.calcValue, bool ) != True:
      raise NameError( f'Field "calcValue" is not of type boolean ({type(self.calcValue)})' )

    if self.replaceValue != None and isinstance( self.replaceValue, bool ) != True:
      raise NameError( f'Field "replaceValue" is not of type boolean ({type(self.replaceValue)})' )

    if self.optimizeList != None :
      if isinstance( self.optimizeList, list ) != True:
        raise NameError( f'Field "optimizeList" is not of type list ({type(self.optimizeList)})' )

      for key in self.optimizeList:
        if isinstance( key, str ) != True:
          raise NameError( f'Field "optimizeList" not all the values are string ({type(key)})' )

    if self.varList != None:
      if isinstance( self.varList, dict ) != True:
        raise NameError( f'Field "varList" is not of type dict ({type(self.varList)})' )

      for key, value in self.varList.items():
        if isinstance( key, str ) != True:
          raise NameError( f'Field "varList" variable name must be a string ({type(key)})' )

        if isinstance( value, str ) != True:
          raise NameError( f'Field "varList" the value by variable "{key}" is not a string ({type(value)})' )

    # return

#
# Database handling
#
class DbFormulaClass():
  """
  Database handling for table formula
  """
  def __init__(self, setClass):
    self.settings          = setClass
    self._tblFormula       = os.path.join( self.settings.dbDirecotry, self.settings.tblFormula )
    self._arrOptimzeTypes  = None
    self._arrOptimzeCustom = None
    self._arrVariables     = None
    self._arrFunctions     = None

  def checkCodeInList( self, arr, code ):
    """
    Control of the given code exist in the given array
    """
    if arr == None:
      return False

    for obj in arr :
      if obj[ 'code' ] == code:
        return True

    return False

  def addToArray( self, arr, code, desc ):
    """
    Add code and description as object to the given array
    """
    objData = {
      "code"        : code ,
      "description" : desc
    }
    arr.append( objData )

  def getFunctions(self):
    """
    Get the all the functions and give the array back.
    Array contains objects with 2 fields, "code" and "description"
    """
    if self._arrFunctions == None:
      self._arrFunctions = []

      for key in sorted( symexpress3.symtables.functionTable ):
        value   = symexpress3.symtables.functionTable[ key ]
        cSyntax = value.syntax
        if cSyntax == None:
          continue

        self.addToArray( self._arrFunctions, value.syntax, value.syntaxExplain )

    return self._arrFunctions

  def getVariables(self):
    """
    Get the all the variables and give the array back.
    Array contains objects with 2 fields, "code" and "description"
    """
    if self._arrOptimzeTypes == None :
      self._arrVariables = []

      dictAct = collections.OrderedDict(sorted( symexpress3.GetFixedVariables().items() ))
      for key, value in dictAct.items():
        self.addToArray( self._arrVariables, key, value )

    return self._arrVariables

  def getOptimzeTypes(self):
    """
    Get the all the optimize options and give the array back.
    Array contains objects with 2 fields, "code" and "description"
    """
    if self._arrOptimzeTypes == None :
      self._arrOptimzeTypes = []
      self.addToArray( self._arrOptimzeTypes, 'OptimizeNormal'  , 'Normal optimization'   )
      self.addToArray( self._arrOptimzeTypes, 'OptimizeExtended', 'Extended optimization' )
      self.addToArray( self._arrOptimzeTypes, 'OptimizeNone'    , 'None'                  )
      self.addToArray( self._arrOptimzeTypes, 'OptimizeCustom'  , 'Custom'                )

    return self._arrOptimzeTypes

  def getOptimzeCustoms(self):
    """
    Get the custom optimize options and give the array back.
    Array contains objects with 2 fields, "code" and "description"
    """
    if self._arrOptimzeCustom == None :
      self._arrOptimzeCustom = []

      self.addToArray( self._arrOptimzeCustom, 'optimizeNormal'   , 'Normal optimization'    )
      self.addToArray( self._arrOptimzeCustom, 'optimizeExtended' , 'Extended optimization'  )
      self.addToArray( self._arrOptimzeCustom, 'none'             , 'Optimize expression'    )

      dictAct = collections.OrderedDict(sorted( symexpress3.GetAllOptimizeActions().items() ))
      for key, value in dictAct.items():
        self.addToArray( self._arrOptimzeCustom, key, value )

    return self._arrOptimzeCustom

  def listFomrulas(self):
    """
    Get a list of all the formulas in the database.
    It give a list of formula-codes back.
    """
    # give a list of all the available formula codes
    dirList = os.listdir( self._tblFormula )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given subdirname
    """
    dirName = self._tblFormula + os.sep + subDirName
    dirName = os.path.normpath( dirName )

    testDir = os.path.basename( dirName )

    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName }"' )

    dirName += os.sep

    return dirName


  def getFormulaDetails( self, formulaCode ):
    """
    Get the record (RecordFormula) from the given formula code
    """
    recFormula = RecordFormula()

    # get all the details of a formula
    dirName = self.getDirName( formulaCode )
    if os.path.isdir( dirName ):
      recFormula.name = formulaCode
      fileName = dirName + "formula.txt"
      if os.path.isfile( fileName ):
        recFormula.formula = Path( fileName ).read_text( encoding="utf-8" )
      fileName = dirName + "formula.html"
      if os.path.isfile( fileName ):
        recFormula.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      if 'optimizeType' not in optionsJson:
        optionsJson[ 'optimizeType' ] = 'OptimizeNormal'

      if 'calcValue' not in optionsJson:
        optionsJson[ 'calcValue'    ] = False

      if 'replaceValue' not in optionsJson:
        optionsJson[ 'replaceValue' ] = False

      if 'optimizeList' not in optionsJson:
        optionsJson[ 'optimizeList' ] = []

      if 'varList' not in optionsJson:
        optionsJson[ 'varList'      ] = {}

      recFormula.optimizeType = optionsJson[ 'optimizeType' ]
      recFormula.calcValue    = optionsJson[ 'calcValue'    ]
      recFormula.replaceValue = optionsJson[ 'replaceValue' ]
      recFormula.optimizeList = optionsJson[ 'optimizeList' ]
      recFormula.varList      = optionsJson[ 'varList'      ]

    return recFormula

  def deleteFormualDetails( self, key ):
    """
    Delete the given formula from the database
    """
    key.strip()
    if key.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if (len( key ) < 3 or len( key ) > 62):
      raise NameError('Record not found.')
    if key[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    dirName = self.getDirName( key )

    if os.path.isdir( dirName ) != True :
      raise NameError('Record not found')

    fileName = dirName + "formula.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "formula.html"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcFormualDetails( self, key ):
    """
    Process the data from the given formula code and put it back in the database.
    It create the html file for the formula.
    """
    recFormula = self.getFormulaDetails( key )
    dirName    = self.getDirName( recFormula.name )
    fileName   = dirName + "formula.html"
    output     = symexpress3.SymToHtml( fileName, recFormula.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      infoStr = str( recFormula.optimizeType )
      if recFormula.calcValue == True:
        infoStr += ' (Calculate real value)'
      output.writeLine( infoStr )
      output.writeLine( 'Expression: ' + recFormula.formula )

      if recFormula.replaceValue == True:
        dictVars = recFormula.varList.copy()

      if recFormula.calcValue == True:
        # make all the values numeric
        for keyList, valueList in recFormula.varList.items():
          try:
            numValue = float( valueList )
            recFormula.varList[ keyList ] = numValue
          except ValueError:
            oFrm = None
            try:
              oFrm = symexpress3.SymFormulaParser( valueList )
            except Exception : # as err:
              # pylint: disable=raise-missing-from
              raise NameError( f'Field "varList" variable {keyList} is not a number or a formula: "{valueList}"' )

            # it must be evaluate to a number
            try:
              numValue = oFrm.getValue( None )
            except Exception: # as err:
              # pylint: disable=raise-missing-from
              raise NameError( f'Field "varList" variable {keyList} with formula {valueList} do not evaluate to a number' )

            recFormula.varList[ keyList ] = numValue

        output.writeVariables( recFormula.varList )

      extraOptions = []
      oFrm = symexpress3.SymFormulaParser( recFormula.formula )

      if recFormula.replaceValue == True:
        output.writeSymExpress( oFrm, 'Before replace variables' )
        output.writeVariables( dictVars )
        oFrm.replaceVariable( dictVars )
        output.writeSymExpress( oFrm, 'Replaced variables' )
        output.writeLine( f'Replaced expression: {oFrm}' )
        output.writeLine( ' ' )


      if recFormula.calcValue == True:
        extraOptions.append( 'calculation' )

      if recFormula.optimizeType == 'OptimizeNormal':
        oFrm.optimizeNormal( output, None, extraOptions, recFormula.varList )

      if recFormula.optimizeType == 'OptimizeExtended':
        oFrm.optimizeExtended( output, None, extraOptions, recFormula.varList )

      elif recFormula.optimizeType == 'OptimizeNone':
        if recFormula.calcValue == True:
          dValue = oFrm.getValue( recFormula.varList )
          output.writeLine( f'Calculated: {str( dValue )}' )

      if recFormula.optimizeType == 'OptimizeCustom':
        output.writeLine( ' ' )
        for cAction in recFormula.optimizeList:
          if cAction == 'optimizeNormal':
            oFrm.optimizeNormal( output, None, extraOptions, recFormula.varList )

          elif cAction == 'optimizeExtended' :
            oFrm.optimizeExtended( output, None, extraOptions, recFormula.varList )

          elif cAction == 'none':
            output.writeLine( f'Action: {cAction}' )
            oFrm.optimize( None )
            output.writeSymExpress( oFrm )
            output.writeLine( str( oFrm ))

            if recFormula.calcValue == True:
              dValue = oFrm.getValue( recFormula.varList )
              output.writeLine( f'Calculated: {str( dValue )}' )
          else:
            output.writeLine( f'Action: {cAction}' )
            oFrm.optimize( cAction )
            output.writeSymExpress( oFrm )
            output.writeLine( str( oFrm ))

            if recFormula.calcValue == True:
              dValue = oFrm.getValue( recFormula.varList )
              output.writeLine( f'Calculated: {str( dValue )}' )

          output.writeLine( ' ' )

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recFormula = self.getFormulaDetails( key )

    return recFormula


  def saveFormualDetails( self, recFormula ):
    """
    Save the given formula data (RecordFormula) into the database
    """
    if recFormula.name == None:
      raise NameError('Key field name must be given')

    recFormula.checkDataType()  # check data types first

    recFormula.name.strip()
    if recFormula.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recFormula.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recFormula.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recFormula.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    if recFormula.formula != None:
      if len( recFormula.formula ) > 24000:
        raise NameError('Field "formula" may exceed 24000 (24Kb) characters')

      # parse formula to see if it is correct
      oFrm = symexpress3.SymFormulaParser( recFormula.formula )

    if recFormula.htmlDisplay != None:
      if len( recFormula.htmlDisplay ) > 2000000: # 2Mb
        raise NameError('Field "htmlDisplay" may exceed 2000000 (2Mb) characters')
      if recFormula.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    # update file formual.txt
    # update file formual.html
    dirName = self.getDirName( recFormula.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recFormula.formula != None:
      fileName = dirName + "formula.txt"
      Path( fileName ).write_text( recFormula.formula, encoding="utf-8" )

    if recFormula.htmlDisplay != None:
      fileName = dirName + "formula.html"
      Path( fileName ).write_text( recFormula.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    if 'optimizeType' not in optionsJson:
      optionsJson[ 'optimizeType' ] = 'OptimizeNormal'

    if 'calcValue' not in optionsJson:
      optionsJson[ 'calcValue'    ] = False

    if 'replaceValue' not in optionsJson:
      optionsJson[ 'replaceValue' ] = False

    if 'optimizeList' not in optionsJson:
      optionsJson[ 'optimizeList' ] = []

    if 'varList' not in optionsJson:
      optionsJson[ 'varList'      ] = {}

    if recFormula.optimizeType != None:
      arrList = self.getOptimzeTypes()
      if self.checkCodeInList( arrList, recFormula.optimizeType ) == True:
        optionsJson[ 'optimizeType' ] = recFormula.optimizeType
      else:
        raise NameError( f'Field "optimizeType" has unknown type: {recFormula.optimizeType}' )

    if recFormula.calcValue != None:
      optionsJson[ 'calcValue' ] = recFormula.calcValue

    if recFormula.replaceValue != None:
      optionsJson[ 'replaceValue' ] = recFormula.replaceValue

    if recFormula.optimizeList != None:
      arrList = self.getOptimzeCustoms()

      for key in recFormula.optimizeList:
        if self.checkCodeInList( arrList, key ) != True:
          raise NameError( f'Field "optimizeList" has unknown type: {key}' )

      optionsJson[ 'optimizeList' ] = recFormula.optimizeList

    if recFormula.varList != None:
      # Check correct variable name and value (must be a string)
      for varName, value in recFormula.varList.items():
        # check varname
        if varName.isprintable() != True :
          raise NameError('Field "varList", variable name may only contain printable characters')
        if len( varName ) < 1 :
          raise NameError('Field "varList" variable name must at least 1 character long')
        if " " in varName :
          raise NameError( f'Field "varList" variable name may not contain spaces: "{varName}"')

        # check value
        check = False
        try:
          # first check if it is a number
          numValue = float( value ) # pylint: disable=unused-variable
          check    = True
        except ValueError:
          pass

        if check == False:
          # check if it is a formula
          oFrm = None
          try:
            oFrm = symexpress3.SymFormulaParser( value )
          except Exception: # as err:
            # pylint: disable=raise-missing-from
            raise NameError( f'Field "varList" variable {varName} is not a number or a formula: "{value}"' )

          # it must be evalue to a number
          try:
            oFrm.getValue( None )
          except Exception: # as err:
            # pylint: disable=raise-missing-from
            raise NameError( f'Field "varList" variable {varName} with formula {value} do not evaluate to a number' )

      optionsJson[ 'varList' ] = recFormula.varList


    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getFormulaDetails(  recFormula.name )
