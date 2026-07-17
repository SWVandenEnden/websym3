#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting class for WebSymExpress3
"""
import os
import logging
import logging.config

class SettingsClass():
  """
  Settings class
  """
  def __init__(self , config = None):
    self._config         = config         # configparser.ConfigParser
    self._tblFormula     = "formulas"     # see checkCreateDirs()
    self._tblTschirnhaus = "tschirnhaus"
    self._tblResultant   = "resultant"
    self._tblTaylorSerie = "taylorserie"
    self._tblThirdpower  = "thirdpower"
    self._tblFourthpower = "fourthpower"
    self._tblPolyDiv     = "polydiv"
    self._tblGraph       = "graph"
    self._dbDir          = "tobefilled"
    self._version        = "0.0.0"
    self._templateDir    = ""
    self._starturl       = "/math/index.html"
    self._curProgCode    = "" # current program code
    self._curProgName    = "" # current program name
    self._logger         = None

    if self._config != None:
      self._dbDir        = config[ 'Path'  ]  [ 'data'     ]
      self._templateDir  = config[ 'Path'    ][ 'template' ]
      self._starturl     = config[ 'Start'   ][ 'starturl' ]
      self._version      = config[ 'Version' ][ 'version'  ]

      # start Python logging module
      if config[ 'Logging' ][ 'enabled'  ] == 'True':
        self._logger = logging.getLogger()
        if config[ 'Logging' ][ 'configfile' ] != '' :
          logging.config.fileConfig( config[ 'Logging' ][ 'configfile' ] )

        self._logger.info( "Logging started")
    else:
      self._dbDir        = os.path.join( os.getcwd(), 'data'     )
      self._templateDir  = os.path.join( os.getcwd(), 'template' )

  @property
  def getConfiguration(self):
    """
    Get the configuration (configparser.ConfigParser)
    """
    return self._config


  @property
  def currentProgramName(self):
    """
    The current program name/description
    """
    return self._curProgName

  @currentProgramName.setter
  def currentProgramName(self, val):
    self._curProgName = val


  @property
  def currentProgramCode(self):
    """
    The current program code
    """
    return self._curProgCode

  @currentProgramCode.setter
  def currentProgramCode(self, val):
    self._curProgCode = val


  @property
  def log(self):
    """
    The Python logger handle, None = no logger
    """
    return self._logger

  @log.setter
  def log(self, val):
    self._logger = val


  @property
  def startUrl(self):
    """
    Home page application
    """
    return self._starturl

  @startUrl.setter
  def startUrl(self, val):
    self._starturl = val

  @property
  def version(self):
    """
    Version of WebSymExpress3
    """
    return self._version

  @version.setter
  def version(self, val):
    self._version = val

  @property
  def dbDirecotry(self):
    """
    Database directory
    """
    return self._dbDir

  @dbDirecotry.setter
  def dbDirecotry(self, value):
    self._dbDir = value


  @property
  def templateDirectory(self):
    """
    Template directory
    """
    return self._templateDir

  @templateDirectory.setter
  def templateDirectory(self, value):
    self._templateDir = value



  @property
  def tblFormula(self):
    """
   Physic name of formula table
    """
    return self._tblFormula

  @tblFormula.setter
  def tblFormula(self, value):
    self._tblFormula = value


  @property
  def tblResultant(self):
    """
    Physic name of the resultant table
    """
    return self._tblResultant

  @tblResultant.setter
  def tblResultant(self, value):
    self._tblResultant = value

  @property
  def tblPolyDiv(self):
    """
    Physic name of the polynomial division table
    """
    return self._tblPolyDiv

  @tblPolyDiv.setter
  def tblPolyDiv(self, value):
    self._tblPolyDiv = value


  @property
  def tblTschirnhaus(self):
    """
    Physic name of the tschirnhaus table
    """
    return self._tblTschirnhaus

  @tblTschirnhaus.setter
  def tblTschirnhaus(self, value):
    self._tblTschirnhaus = value


  @property
  def tblTaylorSerie(self):
    """
    Physic name of the taylor serie table
    """
    return self._tblTaylorSerie

  @tblTaylorSerie.setter
  def tblTaylorSerie(self, value):
    self._tblTaylorSerie = value


  @property
  def tblThirdpower(self):
    """
    Physic name of the third power table
    """
    return self._tblThirdpower

  @tblThirdpower.setter
  def tblThirdpower(self, value):
    self._tblThirdpower = value


  @property
  def tblFourthpower(self):
    """
    Physic name of the fourth power table
    """
    return self._tblFourthpower

  @tblFourthpower.setter
  def tblFourthpower(self, value):
    self._tblFourthpower = value


  @property
  def tblGraph(self):
    """
    Physic name of the graph table
    """
    return self._tblGraph

  @tblGraph.setter
  def tblGraph(self, value):
    self._tblGraph = value


  def checkCreateDirs(self):
    """
    Check of the root directories exist.
    Create the data sub directories if not exist
    """
    def _checkCreateSub( cDir, cSub ):
      if not os.path.isdir( cDir ):
        raise NameError( f"Setting {cDir} is not a valid directory" )

      cDirSub = os.path.join( cDir, cSub )
      if os.path.isfile( cDirSub ):
        raise NameError( f"Setting {cSub} point to a file {cDirSub} insteed of a directory" )

      if os.path.isdir( cDirSub ):
        return

      # does not exist try to create a directory
      os.makedirs( cDirSub )


    if not os.path.isdir( self._dbDir ):
      raise NameError( f"Setting dbDir {self._dbDir} is not a valid directory" )

    if not os.path.isdir( self._templateDir ):
      raise NameError( f"Setting templateDir {self._templateDir} is not a valid directory" )

    _checkCreateSub( self._dbDir, self._tblFormula     )
    _checkCreateSub( self._dbDir, self._tblThirdpower  )
    _checkCreateSub( self._dbDir, self._tblFourthpower )
    _checkCreateSub( self._dbDir, self._tblGraph       )
    _checkCreateSub( self._dbDir, self._tblTaylorSerie )
    _checkCreateSub( self._dbDir, self._tblResultant   )
    _checkCreateSub( self._dbDir, self._tblTschirnhaus )
    _checkCreateSub( self._dbDir, self._tblPolyDiv     )
