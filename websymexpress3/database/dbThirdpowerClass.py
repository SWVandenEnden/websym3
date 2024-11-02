#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database handling for table third power
"""
import json
import os

from pathlib  import Path
from datetime import datetime

import symexpress3
import cubicequation

#
# Record definition
#
class RecordThirdpower: # pylint: disable=too-few-public-methods
  """
  Data record for table third power
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.description      = ""    # description
    self.a                = ""    # formula for variable a
    self.b                = ""
    self.c                = ""
    self.d                = ""
    self.htmlDisplay      = ""    # the html file (no link) of the solutions
    self.calcValue        = False # Calc the real value of the solutions

  # special method too check all data types of all the fields...
  def checkDataType(self):
    """
    Check all the fields datatype
    """
    if isinstance( self.name, str ) != True:
      raise NameError( f'Field "name" is not of type string ({type(self.name)})' )

    if self.description != None and isinstance( self.description, str ) != True:
      raise NameError( f'Field "description" is not of type string ({type(self.description)})' )

    if self.a != None and isinstance( self.a, str ) != True:
      raise NameError( f'Field "a" is not of type string ({type(self.a)})' )

    if self.b != None and isinstance( self.b, str ) != True:
      raise NameError( f'Field "b" is not of type string ({type(self.b)})' )

    if self.c != None and isinstance( self.c, str ) != True:
      raise NameError( f'Field "c" is not of type string ({type(self.c)})' )

    if self.d != None and isinstance( self.d, str ) != True:
      raise NameError( f'Field "d" is not of type string ({type(self.d)})' )

    if self.htmlDisplay != None and isinstance( self.htmlDisplay, str ) != True:
      raise NameError( f'Field "htmlDisplay" is not of type string ({type(self.htmlDisplay)})' )

    if self.calcValue != None and isinstance( self.calcValue, bool ) != True:
      raise NameError( f'Field "calcValue" is not of type boolean ({type(self.calcValue)})' )

    # return

#
# Database handling
#
class DbThirdpowerClass():
  """
  Database handling for table third power
  """
  def __init__(self, settClass):
    self.settings       = settClass
    self._tblThirdpower = os.path.join( self.settings.dbDirecotry, self.settings.tblThirdpower )

  def listThirdpowers(self):
    """
    Get a list of all the third powers in the database.
    It give a list of third power codes back.
    """
    dirList = os.listdir( self._tblThirdpower )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given sub dirname
    """
    dirName = self._tblThirdpower + os.sep + subDirName
    dirName = os.path.normpath( dirName )
    testDir = os.path.basename( dirName )

    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName}"' )

    dirName += os.sep

    return dirName


  def getThirdpowerDetails( self, thirdpowerCode ):
    """
    Get the record (RecordThirdpower) from the given third power code
    """
    recThirdpower = RecordThirdpower()

    dirName = self.getDirName( thirdpowerCode )
    if os.path.isdir( dirName ):
      recThirdpower.name = thirdpowerCode

      fileName = dirName + "description.txt"
      if os.path.isfile( fileName ):
        recThirdpower.description = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "a.txt"
      if os.path.isfile( fileName ):
        recThirdpower.a = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "b.txt"
      if os.path.isfile( fileName ):
        recThirdpower.b = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "c.txt"
      if os.path.isfile( fileName ):
        recThirdpower.c = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "d.txt"
      if os.path.isfile( fileName ):
        recThirdpower.d = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "htmlDisplay.html"
      if os.path.isfile( fileName ):
        recThirdpower.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      recThirdpower.calcValue = optionsJson[ 'calcValue'    ]

    return recThirdpower

  def deleteThirdpowerDetails( self, key ):
    """
    Delete the given third power from the database
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

    fileName = dirName + "description.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "a.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "b.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "c.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "d.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "htmlDisplay.html"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcThirdpowerDetails( self, key ):
    """
    Process the data from the given third power code and put it back in the database.
    It create the html file for the third power.
    """
    recThirdpower = self.getThirdpowerDetails( key )

    dirName  = self.getDirName( recThirdpower.name )
    fileName = dirName + "htmlDisplay.html"
    output   = symexpress3.SymToHtml( fileName, recThirdpower.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      calc            = cubicequation.CubicEquation()
      calc.htmlOutput = output
      calc.a          = recThirdpower.a
      calc.b          = recThirdpower.b
      calc.c          = recThirdpower.c
      calc.d          = recThirdpower.d
      calc.realCalc   = recThirdpower.calcValue

      calc.calcSolutions()

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recThirdpower = self.getThirdpowerDetails( key )

    return recThirdpower


  def saveThirdpowerDetails( self, recThirdpower ):
    """
    Save the given third power data (RecordThirdpower) into the database
    """

    def CheckVar( name, value ):
      if len( value ) > 2048:
        raise NameError( f'Field "{name}" is longer then 2048 ({len(value)}) characters' )

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
        oFrm = None # pylint: disable=unused-variable
        try:
          oFrm = symexpress3.SymFormulaParser( value )
        except Exception: # as err:
          # pylint: disable=raise-missing-from
          raise NameError( f'Field "{name}" is not a number or a formula: "{value}"' )

    # checks
    if recThirdpower.name == None:
      raise NameError('Key field name must be given')

    recThirdpower.checkDataType()  # check data types first

    recThirdpower.name.strip()
    if recThirdpower.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recThirdpower.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recThirdpower.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recThirdpower.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    CheckVar( "a", recThirdpower.a )
    CheckVar( "b", recThirdpower.b )
    CheckVar( "c", recThirdpower.c )
    CheckVar( "d", recThirdpower.d )

    if recThirdpower.description != None and len( recThirdpower.description ) > 24000:
      raise NameError('Field "description" may exceed 24000 (20kb) characters')

    if recThirdpower.htmlDisplay != None:
      if len( recThirdpower.htmlDisplay ) > 20000000: # 20Mb
        raise NameError('Field "htmlDisplay" may exceed 20000000 (20Mb) characters')
      if recThirdpower.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    # update files
    dirName = self.getDirName( recThirdpower.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recThirdpower.description != None:
      fileName = dirName + "description.txt"
      Path( fileName ).write_text( recThirdpower.description, encoding="utf-8" )

    if recThirdpower.a != None:
      fileName = dirName + "a.txt"
      Path( fileName ).write_text( recThirdpower.a, encoding="utf-8" )

    if recThirdpower.b != None:
      fileName = dirName + "b.txt"
      Path( fileName ).write_text( recThirdpower.b, encoding="utf-8" )

    if recThirdpower.c != None:
      fileName = dirName + "c.txt"
      Path( fileName ).write_text( recThirdpower.c, encoding="utf-8" )

    if recThirdpower.d != None:
      fileName = dirName + "d.txt"
      Path( fileName ).write_text( recThirdpower.d, encoding="utf-8" )

    if recThirdpower.htmlDisplay != None:
      fileName = dirName + "htmlDisplay.html"
      Path( fileName ).write_text( recThirdpower.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    if 'calcValue' not in optionsJson:
      optionsJson[ 'calcValue'    ] = False

    if recThirdpower.calcValue != None:
      optionsJson[ 'calcValue' ] = recThirdpower.calcValue

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getThirdpowerDetails( recThirdpower.name )
