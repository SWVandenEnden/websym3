#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database handling for table resultant
"""
import json
import os

from pathlib  import Path
from datetime import datetime

import symexpress3
import sym3resultant

#
# Record definition
#
class RecordResultant: # pylint: disable=too-few-public-methods
  """
  Data record for table resultant
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.description      = ""    # description
    self.formula1         = ""    # sym3 formula in string format
    self.formula2         = ""    # sym3 formula in string format
    self.variable         = 'x'   # the power variable in the formula
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

    if self.formula1 != None and isinstance( self.formula1, str ) != True:
      raise NameError( f'Field "formula1" is not of type string ({type(self.formula1)})' )

    if self.formula2 != None and isinstance( self.formula2, str ) != True:
      raise NameError( f'Field "formula2" is not of type string ({type(self.formula2)})' )

    if self.variable == "":
      self.variable = None

    if self.variable != None and isinstance( self.variable, str ) != True:
      raise NameError( f'Field "variable" is not of type string ({type(self.variable)})' )

    if self.htmlDisplay != None and isinstance( self.htmlDisplay, str ) != True:
      raise NameError( f'Field "htmlDisplay" is not of type string ({type(self.htmlDisplay)})' )


    # return

#
# Database handling
#
class DbResultantClass():
  """
  Database handling for table resultant
  """
  def __init__(self, settClass):
    self.settings      = settClass
    self._tblResultant = os.path.join( self.settings.dbDirecotry, self.settings.tblResultant )

  def listResultants(self):
    """
    Get a list of all the resultant in the database.
    It give a list of resultant codes back.
    """
    dirList = os.listdir( self._tblResultant )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given sub dirname
    """
    dirName = self._tblResultant + os.sep + subDirName
    dirName = os.path.normpath( dirName )
    testDir = os.path.basename( dirName )

    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName}"' )

    dirName += os.sep

    return dirName


  def getResultantDetails( self, resultantCode ):
    """
    Get the record (RecordResultant) from the given resultant code
    """
    recResultant = RecordResultant()

    dirName = self.getDirName( resultantCode )
    if os.path.isdir( dirName ):
      recResultant.name = resultantCode

      fileName = dirName + "description.txt"
      if os.path.isfile( fileName ):
        recResultant.description = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "formula1.txt"
      if os.path.isfile( fileName ):
        recResultant.formula1 = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "formula2.txt"
      if os.path.isfile( fileName ):
        recResultant.formula2 = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "htmlDisplay.html"
      if os.path.isfile( fileName ):
        recResultant.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      # pylint: disable=multiple-statements
      if 'variable'  not in optionsJson: optionsJson[ 'variable'  ] = 'x'

      recResultant.variable = optionsJson[ 'variable' ]

    return recResultant

  def deleteResultantDetails( self, key ):
    """
    Delete the given resultant from the database
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

    fileName = dirName + "formula1.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "formula2.txt"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "htmlDisplay.html"
    if os.path.exists( fileName ):
      os.remove( fileName )

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcResultantDetails( self, key ):
    """
    Process the data from the given resultant code and put it back in the database.
    It create the html file for the resultant
    """
    recResultant = self.getResultantDetails( key )

    dirName  = self.getDirName( recResultant.name )
    fileName = dirName + "htmlDisplay.html"
    output   = symexpress3.SymToHtml( fileName, recResultant.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      calc            = sym3resultant.Sym3Resultant()
      calc.htmlOutput = output
      calc.formula1   = recResultant.formula1
      calc.formula2   = recResultant.formula2
      calc.variable   = recResultant.variable

      calc.calcResultant()

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recResultant = self.getResultantDetails( key )

    return recResultant


  def saveResultantDetails( self, recResultant ):
    """
    Save the given resultant data (RecordResultant) into the database
    """

    # checks
    if recResultant.name == None:
      raise NameError('Key field name must be given')

    recResultant.checkDataType()  # check data types first

    recResultant.name.strip()
    if recResultant.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recResultant.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recResultant.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recResultant.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    if recResultant.description != None and len( recResultant.description ) > 24000:
      raise NameError('Field "description" may exceed 24000 (20kb) characters')

    if recResultant.htmlDisplay != None:
      if len( recResultant.htmlDisplay ) > 20000000: # 20Mb
        raise NameError('Field "htmlDisplay" may exceed 20000000 (20Mb) characters')
      if recResultant.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    # update files
    dirName = self.getDirName( recResultant.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recResultant.description != None:
      fileName = dirName + "description.txt"
      Path( fileName ).write_text( recResultant.description, encoding="utf-8" )

    if recResultant.formula1 != None:
      fileName = dirName + "formula1.txt"
      Path( fileName ).write_text( recResultant.formula1, encoding="utf-8" )

    if recResultant.formula2 != None:
      fileName = dirName + "formula2.txt"
      Path( fileName ).write_text( recResultant.formula2, encoding="utf-8" )

    if recResultant.htmlDisplay != None:
      fileName = dirName + "htmlDisplay.html"
      Path( fileName ).write_text( recResultant.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    # pylint: disable=multiple-statements
    if 'variable'   not in optionsJson: optionsJson[ 'variable'   ] = 'x'

    if recResultant.variable   != None:  optionsJson[ 'variable'   ] = recResultant.variable

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getResultantDetails( recResultant.name )
