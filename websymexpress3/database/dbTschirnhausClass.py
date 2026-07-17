#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database handling for table tschirnhaus
"""
import json
import os

from pathlib  import Path
from datetime import datetime

import symexpress3
import sym3tschirnhaus

#
# Record definition
#
class RecordTschirnhaus: # pylint: disable=too-few-public-methods
  """
  Data record for table tschirnhaus
  """
  def __init__(self):
    self.name             = ""    # name of the formula
    self.description      = ""    # description
    self.formula          = ""    # sym3 formula in string format
    self.variable         = 'x'   # the power variable in the formula
    self.eliminatePowers  = None  # max numbers of powers to eliminate
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

    if self.eliminatePowers != None and self.eliminatePowers == 0:
      self.eliminatePowers = None

    if self.eliminatePowers != None and self.eliminatePowers < 0:
      self.eliminatePowers = None

    if self.eliminatePowers != None and self.eliminatePowers > 3:
      self.eliminatePowers = 3

    if self.eliminatePowers != None and isinstance( self.eliminatePowers, int ) != True:
      raise NameError( f'Field "eliminatePowers" is not of type int ({type(self.eliminatePowers)})' )

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
class DbTschirnhausClass():
  """
  Database handling for table tschirnhaus
  """
  def __init__(self, settClass):
    self.settings      = settClass
    self._tblTschirnhaus = os.path.join( self.settings.dbDirecotry, self.settings.tblTschirnhaus )

  def listTschirnhauss(self):
    """
    Get a list of all the tschirnhaus in the database.
    It give a list of tschirnhaus codes back.
    """
    dirList = os.listdir( self._tblTschirnhaus )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given sub dirname
    """
    dirName = self._tblTschirnhaus + os.sep + subDirName
    dirName = os.path.normpath( dirName )
    testDir = os.path.basename( dirName )

    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName}"' )

    dirName += os.sep

    return dirName


  def getTschirnhausDetails( self, tschirnhausCode ):
    """
    Get the record (RecordTschirnhaus) from the given tschirnhaus code
    """
    recTschirnhaus = RecordTschirnhaus()

    dirName = self.getDirName( tschirnhausCode )
    if os.path.isdir( dirName ):
      recTschirnhaus.name = tschirnhausCode

      fileName = dirName + "description.txt"
      if os.path.isfile( fileName ):
        recTschirnhaus.description = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "formula.txt"
      if os.path.isfile( fileName ):
        recTschirnhaus.formula = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "htmlDisplay.html"
      if os.path.isfile( fileName ):
        recTschirnhaus.htmlDisplay = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      # pylint: disable=multiple-statements
      if 'variable'        not in optionsJson: optionsJson[ 'variable'        ] = 'x'
      if 'eliminatePowers' not in optionsJson: optionsJson[ 'eliminatePowers' ] = 3

      recTschirnhaus.variable        = optionsJson[ 'variable'        ]
      recTschirnhaus.eliminatePowers = optionsJson[ 'eliminatePowers' ]

    return recTschirnhaus

  def deleteTschirnhausDetails( self, key ):
    """
    Delete the given tschirnhaus from the database
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

  def calcTschirnhausDetails( self, key ):
    """
    Process the data from the given tschirnhaus code and put it back in the database.
    It create the html file for the tschirnhaus
    """
    recTschirnhaus = self.getTschirnhausDetails( key )

    dirName  = self.getDirName( recTschirnhaus.name )
    fileName = dirName + "htmlDisplay.html"
    output   = symexpress3.SymToHtml( fileName, recTschirnhaus.name )

    try:
      curDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
      output.writeLine( key + " (" + curDateTime + ")" )

      calc                 = sym3tschirnhaus.Sym3Tschirnhaus()
      calc.htmlOutput      = output
      calc.startFormula    = recTschirnhaus.formula
      calc.variable        = recTschirnhaus.variable
      calc.eliminatePowers = recTschirnhaus.eliminatePowers

      calc.calcTschirnhausTransformation()

    except Exception as err: # pylint: disable=broad-exception-caught
      output.writeLine( ' ' )
      output.writeLine( f'Error: {str(err)}' )

    output.closeFile()
    output = None

    recTschirnhaus = self.getTschirnhausDetails( key )

    return recTschirnhaus


  def saveTschirnhausDetails( self, recTschirnhaus ):
    """
    Save the given tschirnhaus data (RecordTschirnhaus) into the database
    """

    # checks
    if recTschirnhaus.name == None:
      raise NameError('Key field name must be given')

    recTschirnhaus.checkDataType()  # check data types first

    recTschirnhaus.name.strip()
    if recTschirnhaus.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recTschirnhaus.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recTschirnhaus.name ) > 62 :
      raise NameError('Field "name" may exceed 62 characters')
    if recTschirnhaus.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    if recTschirnhaus.description != None and len( recTschirnhaus.description ) > 24000:
      raise NameError('Field "description" may exceed 24000 (20kb) characters')

    if recTschirnhaus.htmlDisplay != None:
      if len( recTschirnhaus.htmlDisplay ) > 20000000: # 20Mb
        raise NameError('Field "htmlDisplay" may exceed 20000000 (20Mb) characters')
      if recTschirnhaus.htmlDisplay.isprintable() != True :
        raise NameError('Field "htmlDisplay" may only contain printable characters')

    # create directory if not exist
    # update files
    dirName = self.getDirName( recTschirnhaus.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recTschirnhaus.description != None:
      fileName = dirName + "description.txt"
      Path( fileName ).write_text( recTschirnhaus.description, encoding="utf-8" )

    if recTschirnhaus.formula != None:
      fileName = dirName + "formula.txt"
      Path( fileName ).write_text( recTschirnhaus.formula, encoding="utf-8" )

    if recTschirnhaus.htmlDisplay != None:
      fileName = dirName + "htmlDisplay.html"
      Path( fileName ).write_text( recTschirnhaus.htmlDisplay, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    # pylint: disable=multiple-statements
    if 'variable'        not in optionsJson: optionsJson[ 'variable'        ] = 'x'
    if 'eliminatePowers' not in optionsJson: optionsJson[ 'eliminatePowers' ] = 3

    if recTschirnhaus.variable        != None:  optionsJson[ 'variable'        ] = recTschirnhaus.variable
    if recTschirnhaus.eliminatePowers != None:  optionsJson[ 'eliminatePowers' ] = recTschirnhaus.eliminatePowers

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getTschirnhausDetails( recTschirnhaus.name )
