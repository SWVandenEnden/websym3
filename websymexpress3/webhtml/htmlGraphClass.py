#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Html page for maintain and processing table graph
"""
# import sys
import json

from websymexpress3.webhtml  import htmlClass
from websymexpress3.database import dbGraphClass
from websymexpress3.webjson  import jsonApplicationClass


class HtmlGraphClass:
  """
  Html page for maintain and processing table graph
  """
  def __init__(self, inSettingsClass, inCgiClass, inDbClass ):
    self.settings  = inSettingsClass
    self.cgi       = inCgiClass
    self.db        = inDbClass

  def jsonDataDelete(self, key):
    """
    Get the delete json and process (delete) the request in the database
    """
    data   = {}
    status = None
    try:
      dataRecord = self.db.deleteGraphDetails( key ) # pylint: disable=unused-variable
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
      jsonClass.setHeaderVar( 'Status'      , '400 Bad Request')

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

      dataRecord = dbGraphClass.RecordGraph()
      dataRecord.name        = jsonData[ 'name'       ]
      dataRecord.formula     = jsonData[ 'formula'    ]
      dataRecord.varCalc     = jsonData[ 'varCalc'    ]
      dataRecord.varStep     = jsonData[ 'varStep'    ]
      dataRecord.xFrom       = jsonData[ 'xFrom'      ]
      dataRecord.xTo         = jsonData[ 'xTo'        ]
      dataRecord.xStep       = jsonData[ 'xStep'      ]
      dataRecord.yFrom       = jsonData[ 'yFrom'      ]
      dataRecord.yTo         = jsonData[ 'yTo'        ]
      dataRecord.yStep       = jsonData[ 'yStep'      ]

      dataRecord.colorGraphLine   = jsonData[ 'colorGraphLine'   ]
      dataRecord.colorGraphAxe    = jsonData[ 'colorGraphAxe'    ]
      dataRecord.colorGraphNumber = jsonData[ 'colorGraphNumber' ]
      dataRecord.colorGraphGrid   = jsonData[ 'colorGraphGrid'   ]

      dataRecord.showGraphAxe     = jsonData[ 'showGraphAxe'     ]
      dataRecord.showGraphNumber  = jsonData[ 'showGraphNumber'  ]
      dataRecord.showGraphGrid    = jsonData[ 'showGraphGrid'    ]

      dataRecord.fixedVars   = jsonData[ 'fixedVars'  ]

      dataRecord = self.db.saveGraphDetails( dataRecord )

      if options == "calc":
        dataRecord = self.db.calcGraph( dataRecord.name )

      data = {
        "name"      : dataRecord.name      ,
        "formula"   : dataRecord.formula   ,
        "varCalc"   : dataRecord.varCalc   ,
        "varStep"   : dataRecord.varStep   ,
        "xFrom"     : dataRecord.xFrom     ,
        "xTo"       : dataRecord.xTo       ,
        "xStep"     : dataRecord.xStep     ,
        "yFrom"     : dataRecord.yFrom     ,
        "yTo"       : dataRecord.yTo       ,
        "yStep"     : dataRecord.yStep     ,

        "colorGraphLine"   : dataRecord.colorGraphLine  ,
        "colorGraphAxe"    : dataRecord.colorGraphAxe   ,
        "colorGraphNumber" : dataRecord.colorGraphNumber,
        "colorGraphGrid"   : dataRecord.colorGraphGrid  ,
        "showGraphAxe"     : dataRecord.showGraphAxe    ,
        "showGraphNumber"  : dataRecord.showGraphNumber ,
        "showGraphGrid"    : dataRecord.showGraphGrid   ,

        "fixedVars"        : dataRecord.fixedVars
      }
      data[ "calcedValues" ] = dataRecord.calcedValues

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
      jsonClass.setHeaderVar( 'Status'      , '400 Bad Request')

    jsonClass.setJsonString( jsonString )

    return jsonClass

  def jsonDataPage(self, key):
    """
    Get the json request to get formula data for a given key
    """
    jsonClass = jsonApplicationClass.JsonApplicationClass()

    dataRecord = self.db.getGraphDetails( key )

    # this go to the outside world. no auto copy all fields
    data = {
      "name"      : dataRecord.name      ,
      "formula"   : dataRecord.formula   ,
      "varCalc"   : dataRecord.varCalc   ,
      "varStep"   : dataRecord.varStep   ,
      "xFrom"     : dataRecord.xFrom     ,
      "xTo"       : dataRecord.xTo       ,
      "xStep"     : dataRecord.xStep     ,
      "yFrom"     : dataRecord.yFrom     ,
      "yTo"       : dataRecord.yTo       ,
      "yStep"     : dataRecord.yStep     ,

      "colorGraphLine"   : dataRecord.colorGraphLine  ,
      "colorGraphAxe"    : dataRecord.colorGraphAxe   ,
      "colorGraphNumber" : dataRecord.colorGraphNumber,
      "colorGraphGrid"   : dataRecord.colorGraphGrid  ,
      "showGraphAxe"     : dataRecord.showGraphAxe    ,
      "showGraphNumber"  : dataRecord.showGraphNumber ,
      "showGraphGrid"    : dataRecord.showGraphGrid   ,

      "fixedVars"        : dataRecord.fixedVars
    }

    jsonString = json.dumps(data)

    jsonClass.setJsonString( jsonString )

    return jsonClass

  def jsonDataList(self):
    """
    Get the list of all the graphs
    """
    jsonClass  = jsonApplicationClass.JsonApplicationClass()
    dirList    = self.db.listGraphs() # array of all the keys
    jsonString = json.dumps(dirList)

    jsonClass.setJsonString( jsonString )

    return jsonClass


  def mathGraphPage(self):
    """
    Create the graph html page
    """
    html = htmlClass.HtmlClass( self.settings )
    html.setTemplate( "mathGraph.html" )

    return html
