#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database handling for table fourth power
"""
import json
import os

from pathlib  import Path
from datetime import datetime

import symexpress3
import quarticequation

#
# Record definition
#
class RecordFourthpower: # pylint: disable=too-few-public-methods
  """
  Data record for table fourth power
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.description      = ""    # description
    self.a                = ""    # formula for variable a
    self.b                = ""
    self.c                = ""
    self.d                = ""
    self.e                = ""
    self.htmlDisplay      = ""    # the html file (no link) of the solutions
    self.calcValue        = False # Calc the real value of the formula

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

    if self.e != None and isinstance( self.e, str ) != True:
      raise NameError( f'Field "e" is not of type string ({type(self.e)})' )

    if self.htmlDisplay != None and isinstance( self.htmlDisplay, str ) != True:
      raise NameError( f'Field "htmlDisplay" is not of type string ({type(self.htmlDisplay)})' )

    if self.calcValue != None and isinstance( self.calcValue, bool ) != True:
      raise NameError( f'Field "calcValue" is not of type boolean ({type(self.calcValue)})' )

    # return

#
# Database handling
#
class DbFourthpowerClass():
  """
  Database handling for table fourth power
  """
  def __init__(self, settClass):
    self.settings          = settClass
    self._tblFourthpower   = os.path.join( self.settings.dbDirecotry, self.settings.tblFourthpower )

  def listFourthpowers(self):
    """
    Get a list of all the fourth powers in the database.
    It give a list of fourth power-codes back.
    """
    dirList = os.listdir( self._tblFourthpower )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given subdirname
    """
    dirName = self._tblFourthpower + os.sep + subDirName
    dirName = os.path.normpath( dirName )

    testDir = os.path.basename( dirName )
    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName}"' )

    dirName += os.sep

    return dirName


  def getFourthpowerDetails( self, fourthpowerCode ):
    """
    Get the record (RecordFourthpower) from the given fourth power code
    """

    recFourthpower = RecordFourthpower()

    # get all the details of a fourth power
    dirName = self.getDirName( fourthpowerCode )
    if os.path.isdir( dirName ):
      recFourthpower.name = fourthpowerCode

      fileName = dirName + "description.txt"
      if os.path.isfile( fileName ):
        recFourthpower.description = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "a.txt"
      if os.path.isfile( fileName ):
        recFourthpower.a = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "b.txt"
      if os.path.isfile( fileName ):
        recFourthpower.b = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "c.txt"
      if os.path.isfile( fileName ):
        recFourthpower.c = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "d.txt"
      if os.path.isfile( fileName ):
        recFourthpower.d = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "e.txt"
      if os.path.isfile( fileName ):
        recFourthpower.e = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "htmlDisplay.html"
      if os.path.isfile( fileName ):
        recFourthpower.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      recFourthpower.calcValue    = optionsJson[ 'calcValue'    ]

    return recFourthpower

  def deleteFourthpowerDetails( self, key ):
    """
    Delete the given fourth power from the database
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

    fileName = dirName + "e.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "htmlDisplay.html"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcFourthpowerDetails( self, key ):
    """
    Process the data from the given fourth power code and put it back in the database.
    It create the html file for the fourth power
    """
    recFourthpower = self.getFourthpowerDetails( key )
    dirName        = self.getDirName( recFourthpower.name )
    fileName       = dirName + "htmlDisplay.html"
    output         = symexpress3.SymToHtml( fileName, recFourthpower.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      calc            = quarticequation.QuarticEquation()
      calc.htmlOutput = output
      calc.a          = recFourthpower.a
      calc.b          = recFourthpower.b
      calc.c          = recFourthpower.c
      calc.d          = recFourthpower.d
      calc.e          = recFourthpower.e
      calc.realCalc   = recFourthpower.calcValue

      calc.calcSolutions()

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recFourthpower = self.getFourthpowerDetails( key )

    return recFourthpower


  def saveFourthpowerDetails( self, recFourthpower ):
    """
    Save the given fourth power data (RecordFourthpower) into the database
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
    if recFourthpower.name == None:
      raise NameError('Key field name must be given')

    recFourthpower.checkDataType()  # check data types first

    recFourthpower.name.strip()
    if recFourthpower.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recFourthpower.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recFourthpower.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recFourthpower.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    CheckVar( "a", recFourthpower.a )
    CheckVar( "b", recFourthpower.b )
    CheckVar( "c", recFourthpower.c )
    CheckVar( "d", recFourthpower.d )
    CheckVar( "e", recFourthpower.e )

    if recFourthpower.description != None and len( recFourthpower.description ) > 24000:
      raise NameError('Field "description" may exceed 24000 (20kb) characters')

    if recFourthpower.htmlDisplay != None:
      if len( recFourthpower.htmlDisplay ) > 20000000: # 20Mb
        raise NameError('Field "htmlDisplay" may exceed 20000000 (20Mb) characters')
      if recFourthpower.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    dirName = self.getDirName( recFourthpower.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recFourthpower.description != None:
      fileName = dirName + "description.txt"
      Path( fileName ).write_text( recFourthpower.description, encoding="utf-8" )

    if recFourthpower.a != None:
      fileName = dirName + "a.txt"
      Path( fileName ).write_text( recFourthpower.a, encoding="utf-8" )

    if recFourthpower.b != None:
      fileName = dirName + "b.txt"
      Path( fileName ).write_text( recFourthpower.b, encoding="utf-8" )

    if recFourthpower.c != None:
      fileName = dirName + "c.txt"
      Path( fileName ).write_text( recFourthpower.c, encoding="utf-8" )

    if recFourthpower.d != None:
      fileName = dirName + "d.txt"
      Path( fileName ).write_text( recFourthpower.d, encoding="utf-8" )

    if recFourthpower.e != None:
      fileName = dirName + "e.txt"
      Path( fileName ).write_text( recFourthpower.e, encoding="utf-8" )

    if recFourthpower.htmlDisplay != None:
      fileName = dirName + "htmlDisplay.html"
      Path( fileName ).write_text( recFourthpower.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    if 'calcValue' not in optionsJson:
      optionsJson[ 'calcValue' ] = False

    if recFourthpower.calcValue != None:
      optionsJson[ 'calcValue' ] = recFourthpower.calcValue

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )


    # read the record again and return it
    return self.getFourthpowerDetails( recFourthpower.name )
