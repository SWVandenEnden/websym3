#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database handling for table taylor serie
"""
import json
import os

from pathlib  import Path
from datetime import datetime

import symexpress3
import sym3taylorserie

#
# Record definition
#
class RecordTaylorSerie: # pylint: disable=too-few-public-methods
  """
  Data record for table taylor serie
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.description      = ""    # description
    self.formula          = ""    # sym3 formula in string format
    self.steps            = 20    # max number of iterations
    self.baseValue        = 0     # the base value of the Taylor series
    self.diffVar          = 'x'   # the differentiate variable
    self.htmlDisplay      = ""    # the html file (no link) of the solutions

  # special method too check all data types of all the fields...
  def checkDataType(self):
    """
    Check all the fields datatype
    """
    if isinstance( self.name, str ) != True:
      raise NameError( f'Field "name" is not of type string ({type(self.name)})' )

    if self.description != None and isinstance( self.description, str ) != True:
      raise NameError( f'Field "description" is not of type string ({type(self.description)})' )

    if self.formula != None and isinstance( self.formula, str ) != True:
      raise NameError( f'Field "formula" is not of type string ({type(self.formula)})' )

    if self.steps == "":
      self.steps = None

    if self.baseValue == "":
      self.baseValue = None

    if self.diffVar == "":
      self.diffVar = None

    if self.steps != None and isinstance( self.steps, int ) != True:
      raise NameError( f'Field "steps" is not of type int ({type(self.steps)})' )

    if self.baseValue != None and isinstance( self.baseValue, int ) != True:
      raise NameError( f'Field "baseValue" is not of type int ({type(self.baseValue)})' )

    if self.diffVar != None and isinstance( self.diffVar, str ) != True:
      raise NameError( f'Field "diffVar" is not of type string ({type(self.diffVar)})' )

    if self.htmlDisplay != None and isinstance( self.htmlDisplay, str ) != True:
      raise NameError( f'Field "htmlDisplay" is not of type string ({type(self.htmlDisplay)})' )


    # return

#
# Database handling
#
class DbTaylorSerieClass():
  """
  Database handling for table taylor serie
  """
  def __init__(self, settClass):
    self.settings       = settClass
    self._tblTaylorSerie = os.path.join( self.settings.dbDirecotry, self.settings.tblTaylorSerie )

  def listTaylorSeries(self):
    """
    Get a list of all the taylor series in the database.
    It give a list of taylor series codes back.
    """
    dirList = os.listdir( self._tblTaylorSerie )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given sub dirname
    """
    dirName = self._tblTaylorSerie + os.sep + subDirName
    dirName = os.path.normpath( dirName )
    testDir = os.path.basename( dirName )

    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName}"' )

    dirName += os.sep

    return dirName


  def getTaylorSerieDetails( self, taylorserieCode ):
    """
    Get the record (RecordTaylorSerie) from the given taylorserie code
    """
    recTaylorSerie = RecordTaylorSerie()

    dirName = self.getDirName( taylorserieCode )
    if os.path.isdir( dirName ):
      recTaylorSerie.name = taylorserieCode

      fileName = dirName + "description.txt"
      if os.path.isfile( fileName ):
        recTaylorSerie.description = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "formula.txt"
      if os.path.isfile( fileName ):
        recTaylorSerie.formula = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "htmlDisplay.html"
      if os.path.isfile( fileName ):
        recTaylorSerie.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      # pylint: disable=multiple-statements
      if 'steps'     not in optionsJson: optionsJson[ 'steps'     ] = 20
      if 'baseValue' not in optionsJson: optionsJson[ 'baseValue' ] = 0
      if 'diffVar'   not in optionsJson: optionsJson[ 'diffVar'   ] = 'x'

      recTaylorSerie.steps     = optionsJson[ 'steps'     ]
      recTaylorSerie.baseValue = optionsJson[ 'baseValue' ]
      recTaylorSerie.diffVar   = optionsJson[ 'diffVar'   ]

    return recTaylorSerie

  def deleteTaylorSerieDetails( self, key ):
    """
    Delete the given taylor serie from the database
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

    fileName = dirName + "formula.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "htmlDisplay.html"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcTaylorSerieDetails( self, key ):
    """
    Process the data from the given taylor serie code and put it back in the database.
    It create the html file for the taylor serie.
    """
    recTaylorSerie = self.getTaylorSerieDetails( key )

    dirName  = self.getDirName( recTaylorSerie.name )
    fileName = dirName + "htmlDisplay.html"
    output   = symexpress3.SymToHtml( fileName, recTaylorSerie.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      calc            = sym3taylorserie.Sym3TaylorSerie()
      calc.htmlOutput = output
      calc.formula    = recTaylorSerie.formula
      calc.steps      = recTaylorSerie.steps
      calc.baseValue  = recTaylorSerie.baseValue
      calc.diffVar    = recTaylorSerie.diffVar

      calc.calcTaylorSerie()

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recTaylorSerie = self.getTaylorSerieDetails( key )

    return recTaylorSerie


  def saveTaylorSerieDetails( self, recTaylorSerie ):
    """
    Save the given taylorserie data (RecordTaylorSerie) into the database
    """

    # checks
    if recTaylorSerie.name == None:
      raise NameError('Key field name must be given')

    recTaylorSerie.checkDataType()  # check data types first

    recTaylorSerie.name.strip()
    if recTaylorSerie.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recTaylorSerie.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recTaylorSerie.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recTaylorSerie.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    if recTaylorSerie.description != None and len( recTaylorSerie.description ) > 24000:
      raise NameError('Field "description" may exceed 24000 (20kb) characters')

    if recTaylorSerie.htmlDisplay != None:
      if len( recTaylorSerie.htmlDisplay ) > 20000000: # 20Mb
        raise NameError('Field "htmlDisplay" may exceed 20000000 (20Mb) characters')
      if recTaylorSerie.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    # update files
    dirName = self.getDirName( recTaylorSerie.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recTaylorSerie.description != None:
      fileName = dirName + "description.txt"
      Path( fileName ).write_text( recTaylorSerie.description, encoding="utf-8" )

    if recTaylorSerie.formula != None:
      fileName = dirName + "formula.txt"
      Path( fileName ).write_text( recTaylorSerie.formula, encoding="utf-8" )

    if recTaylorSerie.htmlDisplay != None:
      fileName = dirName + "htmlDisplay.html"
      Path( fileName ).write_text( recTaylorSerie.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    # pylint: disable=multiple-statements
    if 'steps'     not in optionsJson: optionsJson[ 'steps'     ] = 20
    if 'baseValue' not in optionsJson: optionsJson[ 'baseValue' ] = 0
    if 'diffVar'   not in optionsJson: optionsJson[ 'diffVar'   ] = 'x'

    if recTaylorSerie.steps     != None:  optionsJson[ 'steps'     ] = recTaylorSerie.steps
    if recTaylorSerie.baseValue != None:  optionsJson[ 'baseValue' ] = recTaylorSerie.baseValue
    if recTaylorSerie.diffVar   != None:  optionsJson[ 'diffVar'   ] = recTaylorSerie.diffVar

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getTaylorSerieDetails( recTaylorSerie.name )
