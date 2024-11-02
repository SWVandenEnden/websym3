#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database handling for table graph
"""
import json
import os

from pathlib  import Path

import symexpress3
import symexpress3.symtables

#
# Record definition
#
class RecordGraph:  # pylint: disable=too-few-public-methods
  """
  Data record for table graph
  """
  def __init__(self):
    self.name             = ""    # name of the graph
    self.formula          = ""    # the formula (symexpress3)
    self.varCalc          = ""    # step variable
    self.varStep          = 0.0   # step variable increase factor
    self.xFrom            = 0     # x start
    self.xTo              = 0     # x to
    self.xStep            = 0     # step factor x
    self.yFrom            = 0     # y from
    self.yTo              = 0     # y to
    self.yStep            = 0     # step factor y

    self.colorGraphLine   = ""
    self.colorGraphAxe    = ""
    self.colorGraphNumber = ""
    self.colorGraphGrid   = ""

    self.showGraphAxe     = True
    self.showGraphNumber  = True
    self.showGraphGrid    = True

    self.fixedVars        = {}    # Dictionary of fixed var, key = varname
    self.calcedValues     = []    # auto filled in calcGraph()


  # special method too check all data types of all the fields...
  def checkDataType(self):
    """
    Check all the fields datatype
    """
    if isinstance( self.name, str ) != True:
      raise NameError( f'Field "name" is not of type string ({type(self.name)})' )

    if self.formula != None and isinstance( self.formula, str ) != True:
      raise NameError( f'Field "formula" is not of type string ({type(self.formula)})' )

    if self.varCalc != None and isinstance( self.varCalc, str ) != True:
      raise NameError( f'Field "varCalc" is not of type string ({type(self.varCalc)})' )

    if self.varStep != None and isinstance( self.varStep, (int,float) ) != True:
      raise NameError( f'Field "varStep" is not a number ({type(self.varStep)})' )

    if self.xFrom != None and isinstance( self.xFrom, (int,float) ) != True:
      raise NameError( f'Field "xFrom" is not a number ({type(self.xFrom)})' )

    if self.xTo != None and isinstance( self.xTo, (int,float) ) != True:
      raise NameError( f'Field "xTo" is not a number ({type(self.xTo)})' )

    if self.xStep != None and isinstance( self.xStep, (int,float) ) != True:
      raise NameError( f'Field "xStep" is not a number ({type(self.xStep)})' )

    if self.yFrom != None and isinstance( self.yFrom, (int,float) ) != True:
      raise NameError( f'Field "yFrom" is not a number ({type(self.yFrom)})' )

    if self.yTo != None and isinstance( self.yTo, (int,float) ) != True:
      raise NameError( f'Field "yTo" is not a number ({type(self.yTo)})' )

    if self.yStep != None and isinstance( self.yStep, (int,float) ) != True:
      raise NameError( f'Field "yStep" is not a number ({type(self.yStep)})' )

    if self.colorGraphLine != None and isinstance( self.colorGraphLine, str ) != True:
      raise NameError( f'Field "colorGraphLine" is not of type string ({type(self.colorGraphLine)})' )

    if self.colorGraphAxe != None and isinstance( self.colorGraphAxe, str ) != True:
      raise NameError( f'Field "colorGraphAxe" is not of type string ({type(self.colorGraphAxe)})' )

    if self.colorGraphNumber != None and isinstance( self.colorGraphNumber, str ) != True:
      raise NameError( f'Field "colorGraphNumber" is not of type string ({type(self.colorGraphNumber)})' )

    if self.colorGraphGrid != None and isinstance( self.colorGraphGrid, str ) != True:
      raise NameError( f'Field "colorGraphGrid" is not of type string ({type(self.colorGraphGrid)})' )

    if self.showGraphAxe != None and isinstance( self.showGraphAxe, bool ) != True:
      raise NameError( f'Field "showGraphAxe" is not of type bool ({type(self.showGraphAxe)})' )

    if self.showGraphNumber != None and isinstance( self.showGraphNumber, bool ) != True:
      raise NameError( f'Field "showGraphNumber" is not of type bool ({type(self.showGraphNumber)})' )

    if self.showGraphGrid != None and isinstance( self.showGraphGrid, bool ) != True:
      raise NameError( f'Field "showGraphGrid" is not of type bool ({type(self.showGraphGrid)})' )

    if self.fixedVars != None:
      if isinstance( self.fixedVars, dict ) != True:
        raise NameError( f'Field "fixedVars" is not of type dict ({type(self.fixedVars)})' )

      for key, value in self.fixedVars.items():
        if isinstance( key, str ) != True:
          raise NameError( f'Field "fixedVars" variable name must be a string ({type(key)})' )

        if isinstance( value, (int,float,str) ) != True:
          raise NameError( f'Field "varList" the value by variable "{key}" is not a string, int or float ({type(value)})' )

    # return

#
# Database handling
#
class DbGraphClass():
  """
  Database handling for table graph
  """
  def __init__(self, setClass):
    self.settings  = setClass
    self._tblGraph = os.path.join( self.settings.dbDirecotry, self.settings.tblGraph )

  def listGraphs(self):
    """
    Get a list of all the graphs in the database.
    It give a list of graph-codes back.
    """
    dirList = os.listdir( self._tblGraph )
    dirList.sort()
    return dirList


  def getDirName( self, subDirName ):
    """
    Give the complete directory of the given subdirname
    """
    dirName = self._tblGraph + os.sep + subDirName
    dirName = os.path.normpath( dirName )

    testDir = os.path.basename( dirName )
    if testDir != subDirName:
      raise NameError( f'Field "name" contains invalid characters: "{subDirName }"' )

    dirName += os.sep

    return dirName

  def _optionsDefault( self, optionsJson ):
    if 'varCalc' not in optionsJson:
      optionsJson[ 'varCalc' ] = 'x'

    if 'varStep' not in optionsJson:
      optionsJson[ 'varStep'    ] = 1

    if 'xFrom' not in optionsJson:
      optionsJson[ 'xFrom' ] = -10

    if 'xTo' not in optionsJson:
      optionsJson[ 'xTo' ] = 10

    if 'xStep' not in optionsJson:
      optionsJson[ 'xStep' ] = 1

    if 'yFrom' not in optionsJson:
      optionsJson[ 'yFrom' ] = -10

    if 'yTo' not in optionsJson:
      optionsJson[ 'yTo' ] = 10

    if 'yStep' not in optionsJson:
      optionsJson[ 'yStep' ] = 1

    if 'colorGraphLine' not in optionsJson:
      optionsJson[ 'colorGraphLine' ] = "#000000"

    if 'colorGraphAxe' not in optionsJson:
      optionsJson[ 'colorGraphAxe' ] = "#000000"

    if 'colorGraphNumber' not in optionsJson:
      optionsJson[ 'colorGraphNumber' ] = "#000000"

    if 'colorGraphGrid' not in optionsJson:
      optionsJson[ 'colorGraphGrid' ] = "#000000"

    if 'showGraphAxe' not in optionsJson:
      optionsJson[ 'showGraphAxe' ] = True

    if 'showGraphNumber' not in optionsJson:
      optionsJson[ 'showGraphNumber' ] = True

    if 'showGraphGrid' not in optionsJson:
      optionsJson[ 'showGraphGrid' ] = True


    if 'fixedVars' not in optionsJson:
      optionsJson[ 'fixedVars'      ] = {}


  def getGraphDetails( self, graphCode ):
    """
    Get the record (RecordGraph) from the given graph code
    """
    recGraph = RecordGraph()

    # get all the details
    dirName = self.getDirName( graphCode )
    if os.path.isdir( dirName ):
      recGraph.name = graphCode
      fileName = dirName + "formula.txt"
      if os.path.isfile( fileName ):
        recGraph.formula = Path( fileName ).read_text( encoding="utf-8" )

      fileName = dirName + "options.json"
      optionsJson = {}
      if os.path.isfile( fileName ):
        jsonString  = Path( fileName ).read_text( encoding="utf-8" )
        optionsJson = json.loads(jsonString)

      self._optionsDefault( optionsJson )

      recGraph.varCalc          = optionsJson[ 'varCalc'    ]
      recGraph.varStep          = optionsJson[ 'varStep'    ]
      recGraph.xFrom            = optionsJson[ 'xFrom'      ]
      recGraph.xTo              = optionsJson[ 'xTo'        ]
      recGraph.xStep            = optionsJson[ 'xStep'      ]
      recGraph.yFrom            = optionsJson[ 'yFrom'      ]
      recGraph.yTo              = optionsJson[ 'yTo'        ]
      recGraph.yStep            = optionsJson[ 'yStep'      ]

      recGraph.colorGraphLine   = optionsJson[ 'colorGraphLine'   ]
      recGraph.colorGraphAxe    = optionsJson[ 'colorGraphAxe'    ]
      recGraph.colorGraphNumber = optionsJson[ 'colorGraphNumber' ]
      recGraph.colorGraphGrid   = optionsJson[ 'colorGraphGrid'   ]

      recGraph.showGraphAxe     = optionsJson[ 'showGraphAxe'     ]
      recGraph.showGraphNumber  = optionsJson[ 'showGraphNumber'  ]
      recGraph.showGraphGrid    = optionsJson[ 'showGraphGrid'    ]

      recGraph.fixedVars        = optionsJson[ 'fixedVars'  ]

    return recGraph

  def deleteGraphDetails( self, key ):
    """
    Delete the given graph from the database
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

    fileName = dirName + "options.json"
    if os.path.exists( fileName ):
      os.remove( fileName )

    os.rmdir(dirName)

  def calcGraph( self, key ):
    """
    Calculate/Create the graph data
    """
    recGraph = self.getGraphDetails( key )
    dictVars = {}

    # walk fixed vars
    varName  = ""
    try:
      for varName, fixedValue in recGraph.fixedVars.items():
        oExpress = symexpress3.SymFormulaParser( fixedValue )
        realVal  = oExpress.getValue()

        dictVars[ varName ] = realVal

    except Exception as err:
      # pylint:disable=raise-missing-from
      raise NameError( f'calcGraph fixedvar {varName} error:{ repr( err )}')

    # the variable that is changing
    varName = recGraph.varCalc

    oExpress = symexpress3.SymFormulaParser( recGraph.formula )

    varAll = oExpress.getVariables()
    if varName not in varAll:
      raise NameError( f"Variable '{varName}' not found the the formula"  )

    arrResult = []

    maxNumber = 3000 # maximum number of points to calculate
    xStart    = recGraph.xFrom - recGraph.varStep
    while xStart < recGraph.xTo and maxNumber > 0:
      maxNumber -= 1
      xStart    += recGraph.varStep

      dictVars[ varName ] = xStart

      yValue = oExpress.getValue( dictVars )

      oValue = {}
      oValue[ 're' ] = xStart
      oValue[ 'im' ] = 0

      oData = {}
      oData[ 'x' ] = oValue
      oData[ 'y' ] = []

      # value object: { re: number, im: number }
      # array of objects
      # { x: value,
      #   y: array of values[ ]
      # }
      if isinstance( yValue, list ):
        for numVal in yValue:
          oValue = {}
          oValue[ 're' ] = 0
          oValue[ 'im' ] = 0

          if isinstance( numVal, complex ):
            oValue[ 're' ] = numVal.real
            oValue[ 'im' ] = numVal.imag
          else:
            oValue[ 're' ] = numVal
            oValue[ 'im' ] = 0

          oData[ 'y' ].append( oValue )
      else:
        oValue = {}
        oValue[ 're' ] = 0
        oValue[ 'im' ] = 0

        if isinstance( yValue, complex ):
          oValue[ 're' ] = yValue.real
          oValue[ 'im' ] = yValue.imag
        else:
          oValue[ 're' ] = yValue
          oValue[ 'im' ] = 0

        oData[ 'y' ].append( oValue )

      arrResult.append( oData )

    recGraph.calcedValues = arrResult

    return recGraph


  def saveGraphDetails( self, recGraph ):
    """
    Save the given graph data (RecordGraph) into the database
    """
    if recGraph.name == None:
      raise NameError('Key field name must be given')

    recGraph.checkDataType()  # check data types first

    recGraph.name.strip()
    if recGraph.name.isprintable() != True :
      raise NameError('Field "name" may only contain printable characters')
    if len( recGraph.name ) < 3 :
      raise NameError('Field "name" must at least 3 characters long')
    if len( recGraph.name ) > 62 :

      raise NameError('Field "name" may exceed 62 characters')
    if recGraph.name[ 0 ].isalpha() != True :
      raise NameError('Field "name" first character must be a letter')

    if recGraph.formula != None:
      if len( recGraph.formula ) > 24000:
        raise NameError('Field "formula" may not exceed 24000 (24Kb) characters')
      # parse formula to see if it is correct
      _ = symexpress3.SymFormulaParser( recGraph.formula )

    # create directory if not exist
    dirName = self.getDirName( recGraph.name )
    if os.path.isdir( dirName ) != True :
      os.makedirs(dirName)

    if recGraph.formula != None:
      fileName = dirName + "formula.txt"
      Path( fileName ).write_text( recGraph.formula, encoding="utf-8" )

    fileName = dirName + "options.json"
    optionsJson = {}
    if os.path.isfile( fileName ):
      jsonString  = Path( fileName ).read_text( encoding="utf-8" )
      optionsJson = json.loads(jsonString)

    self._optionsDefault( optionsJson )

    if recGraph.varCalc != None:
      optionsJson[ 'varCalc' ] = recGraph.varCalc

    if recGraph.varStep != None:
      optionsJson[ 'varStep' ] = recGraph.varStep

    if recGraph.xFrom != None:
      optionsJson[ 'xFrom' ] = recGraph.xFrom

    if recGraph.xTo != None:
      optionsJson[ 'xTo' ] = recGraph.xTo

    if recGraph.xStep != None:
      optionsJson[ 'xStep' ] = recGraph.xStep

    if recGraph.yFrom != None:
      optionsJson[ 'yFrom' ] = recGraph.yFrom

    if recGraph.xTo != None:
      optionsJson[ 'yTo' ] = recGraph.yTo

    if recGraph.xStep != None:
      optionsJson[ 'yStep' ] = recGraph.yStep

    if recGraph.colorGraphLine != None:
      optionsJson[ 'colorGraphLine' ] = recGraph.colorGraphLine

    if recGraph.colorGraphAxe != None:
      optionsJson[ 'colorGraphAxe' ] = recGraph.colorGraphAxe

    if recGraph.colorGraphNumber != None:
      optionsJson[ 'colorGraphNumber' ] = recGraph.colorGraphNumber

    if recGraph.colorGraphGrid != None:
      optionsJson[ 'colorGraphGrid' ] = recGraph.colorGraphGrid

    if recGraph.fixedVars != None:
      optionsJson[ 'fixedVars'  ] = recGraph.fixedVars

    if recGraph.showGraphAxe != None:
      optionsJson[ 'showGraphAxe'  ] = recGraph.showGraphAxe

    if recGraph.showGraphNumber != None:
      optionsJson[ 'showGraphNumber'  ] = recGraph.showGraphNumber

    if recGraph.showGraphGrid != None:
      optionsJson[ 'showGraphGrid'  ] = recGraph.showGraphGrid


    # ok some checking
    if recGraph.varCalc == "":
      raise NameError( 'Field "varCalc" may not be empty' )

    if recGraph.varStep <= 0:
      raise NameError( f'Field "varStep" must be greater then zero ({recGraph.varStep})' )

    if recGraph.xFrom >= recGraph.xTo :
      raise NameError( f'Field "xFrom" ({recGraph.xFrom}) must be greater then "xTo ({recGraph.xTo}) ' )

    if recGraph.xStep <= 0:
      raise NameError( f'Field "xStep" must be greater then zero ({recGraph.xStep})' )

    if recGraph.yFrom >= recGraph.yTo :
      raise NameError( f'Field "yFrom" ({recGraph.yFrom}) must be greater then "yTo ({recGraph.yTo}) ' )

    if recGraph.yStep <= 0:
      raise NameError( f'Field "yStep" must be greater then zero ({recGraph.yStep})' )


    if len(recGraph.colorGraphLine) < 3 or len(recGraph.colorGraphLine) > 12:
      raise NameError( 'Field "colorGraphLine" must greater then 3 and lesser then 12' )

    if len(recGraph.colorGraphAxe) < 3 or len(recGraph.colorGraphAxe) > 12:
      raise NameError( 'Field "colorGraphAxe" must greater then 3 and lesser then 12' )

    if len(recGraph.colorGraphNumber) < 3 or len(recGraph.colorGraphNumber) > 12:
      raise NameError( 'Field "colorGraphNumber" must greater then 3 and lesser then 12' )

    if len(recGraph.colorGraphGrid) < 3 or len(recGraph.colorGraphGrid) > 12:
      raise NameError( 'Field "colorGraphGrid" must greater then 3 and lesser then 12' )


    for key, value in recGraph.fixedVars.items():
      try:
        symexpress3.ConvertToSymexpress3String( value )
      except Exception as exceptAll:
        # pylint: disable=raise-missing-from
        raise NameError( f"Fixed var '{key}' has invalid value '{value}', error: {str(exceptAll)}" )

    jsonString = json.dumps(optionsJson)
    Path( fileName ).write_text( jsonString, encoding="utf-8" )

    # read the record again and return it
    return self.getGraphDetails(  recGraph.name )
