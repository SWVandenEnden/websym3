//
// Global vars
//
var glbTools             = {}; // all the tools in 1 object

var glbFieldInputArray   = []; // array of field names to enable/disable by db actions
var glbMaxFixedFields    = 10; // max fixed fields
var glbHtmlGraphTemplate = "";

function init() {

  glbTools.clsGlobal           = new commonGlobal( "divGraph" );
  glbTools.clsGraph            = new drawGraph( glbTools.clsGlobal );
  glbTools.dictGraph           = {}  // dictionary of graph, key = divno
  glbTools.dictLines           = {}  // dictionary of graph lines, key = divno

  glbFieldInputArray.push( "inputFieldCode_"         );
  glbFieldInputArray.push( "buttonInputSmaller_"     );
  glbFieldInputArray.push( "inputFieldCode_"         );
  glbFieldInputArray.push( "inputFieldFormula_"      );
  glbFieldInputArray.push( "inputFieldVarCalc_"      );
  glbFieldInputArray.push( "inputFieldVarStep_"      );
  glbFieldInputArray.push( "inputFieldXFrom_"        );
  glbFieldInputArray.push( "inputFieldXTo_"          );
  glbFieldInputArray.push( "inputFieldXStep_"        );
  glbFieldInputArray.push( "inputFieldYFrom_"        );
  glbFieldInputArray.push( "inputFieldYTo_"          );
  glbFieldInputArray.push( "inputFieldYStep_"        );
  glbFieldInputArray.push( "inputFieldColorGraph_"   );
  glbFieldInputArray.push( "buttonInputSave_"        );
  glbFieldInputArray.push( "buttonInputCalc_"        );

  for( iCount = 1; iCount < glbMaxFixedFields; iCount++ ) {
    glbFieldInputArray.push( "inputFieldFixedName_"  + iCount.toString() + "_" );
    glbFieldInputArray.push( "inputFieldFixedValue_" + iCount.toString() + "_" );
  }

  // create template object
  var oTemplate         = document.getElementById( "divFormula_1" );
  var htmlGraphTemplate = oTemplate.innerHTML;

  htmlGraphTemplate = htmlGraphTemplate.replaceAll( '_1"' , '_###"'  );
  htmlGraphTemplate = htmlGraphTemplate.replaceAll( "'1'" , "'###'" );

  glbHtmlGraphTemplate = htmlGraphTemplate;

  // put unique number beyond 1
  glbTools.clsGlobal.getUniqueNumber();
  glbTools.clsGlobal.getUniqueNumber();

  glbTools.dictGraph[ '1' ] = new drawGraph(     glbTools.clsGlobal );
  glbTools.dictLines[ '1' ] = new drawGraphLine( glbTools.clsGlobal, glbTools.dictGraph[ '1' ] );

  fncGraphSetDefaults( "1" );
  asyncDataList( fncListReceived );
}

// Call back function for asyncDataList,
// it fills the keys in the graph list
function fncListReceived( dataList ) {
  var iCnt   = 0  ;
  var Key    = "" ;
  var cDivNo = "" ;
  var oCode  = null;

  for ( iCnt = 0; iCnt < dataList.length; iCnt++) {
    key = dataList[ iCnt ];
    if (iCnt == 0 ) {
      cDivNo = "1";
    } else {
      cDivNo = fncAddGraphDiv();
    }
    oCode = document.getElementById( "inputFieldCode_" + cDivNo );
    oCode.value    = key;
    oCode.readOnly = true;

    // hide data fields (not read yet)
    fncButtonSmaller( cDivNo, "none" );
  }
}

// https://stackoverflow.com/questions/1573053/javascript-function-to-convert-color-names-to-hex-codes
// move to script_common.js
function getHexColor(colorStr) {
    var a = document.createElement('div');
    a.style.color = colorStr;
    var colors = window.getComputedStyle( document.body.appendChild(a) ).color.match(/\d+/g).map(function(a){ return parseInt(a,10); });
    document.body.removeChild(a);
    return (colors.length >= 3) ? '#' + (((1 << 24) + (colors[0] << 16) + (colors[1] << 8) + colors[2]).toString(16).substr(1)) : false;
}

// https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
// + percent = lighter
// - percent = darker
function shadeColor(color, percent) {

    var R = parseInt(color.substring(1,3),16);
    var G = parseInt(color.substring(3,5),16);
    var B = parseInt(color.substring(5,7),16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R<255)?R:255;
    G = (G<255)?G:255;
    B = (B<255)?B:255;

    R = Math.round(R)
    G = Math.round(G)
    B = Math.round(B)

    var RR = ((R.toString(16).length==1)?"0"+R.toString(16):R.toString(16));
    var GG = ((G.toString(16).length==1)?"0"+G.toString(16):G.toString(16));
    var BB = ((B.toString(16).length==1)?"0"+B.toString(16):B.toString(16));

    return "#"+RR+GG+BB;
}


//
// Add new graph template
// Give back the divno
//
function fncAddGraphDiv( options = null ) {

  var divNr  = glbTools.clsGlobal.getUniqueNumber();
  var newDiv = document.createElement("div");
  var cDivNo = divNr.toString();

  newDiv.id = "divFormula_" + cDivNo;

  htmlGraphTemplate = glbHtmlGraphTemplate.replaceAll( '###', cDivNo );
  newDiv.innerHTML = htmlGraphTemplate;

  var divParent = document.getElementById( "divFormula" );
  divParent.appendChild( newDiv );

  glbTools.dictGraph[ cDivNo ] = new drawGraph(     glbTools.clsGlobal );
  glbTools.dictLines[ cDivNo ] = new drawGraphLine( glbTools.clsGlobal, glbTools.dictGraph[ cDivNo ] );

  fncGraphSetDefaults( cDivNo );

  if (options == "new" ) {
   // close all the other graphs
   var listGraph = document.querySelectorAll('[id^=buttonInputSmaller_]');
   var idGraph   = '';
   var graphNo   = '';

   for( var iCnt = 0; iCnt < listGraph.length; iCnt++ ){
     idGraph = listGraph[ iCnt ].id ;
     graphNo = idGraph.replace( 'buttonInputSmaller_', '' );
     fncButtonSmaller( graphNo, "none" );
   }
   fncButtonSmaller( cDivNo, "" );

    // give focus
    var divFocus = document.getElementById( "inputFieldCode_" + cDivNo );
    divFocus.focus();
  } else {
    fncButtonSmaller( cDivNo );
  }

  return cDivNo;
}

// collapse all the input divs
function fncCollpaseAll() {
   var listGraph = document.querySelectorAll('[id^=buttonInputSmaller_]');
   var idGraph   = '';
   var graphNo   = '';

   for( var iCnt = 0; iCnt < listGraph.length; iCnt++ ){
     idGraph = listGraph[ iCnt ].id ;
     graphNo = idGraph.replace( 'buttonInputSmaller_', '' );
     fncButtonSmaller( graphNo, "none" );
   }
}

//
// open/close the graph data
// If key field (code) is read-only then the data will be read by opened graphAxeColor
// and the read only attribute will be removed
//
function fncButtonSmaller( cDivNo, forcedDisplay = null ) {
  var oDivData = document.getElementById( "divFormlaData_"      + cDivNo );
  var oButton  = document.getElementById( "buttonInputSmaller_" + cDivNo );
  var oCode    = document.getElementById( "inputFieldCode_"     + cDivNo );

  if (oDivData != null) {
    var cDisplay = "";

    if (forcedDisplay != null) {
      cDisplay = forcedDisplay;
    } else {
      if (oDivData.style.display == "none") {
        cDisplay = "";
      } else {
        cDisplay = "none";
      }
    }
    // ▲ ▼
    if (cDisplay == "none" ) {
      oButton.textContent = "▼";
    } else {
      oButton.textContent = "▲";
      if (oCode.readOnly == true) {
        oCode.readOnly = false;
        // read data
        asyncDownloadInputData( oCode.value, cDivNo );
      }
    }
    oDivData.style.display = cDisplay;
  }
}

function fieldInputDisable( cDivNo, state ) {
  var cName = ""  ;
  var oItem = null;

  for ( iCount = 0; iCount < glbFieldInputArray.length; iCount++) {
    cName = glbFieldInputArray[ iCount ] + cDivNo;
    oItem = document.getElementById( cName );
    if (oItem != null) {
      oItem.disabled  = state ;
    }
  }
}


// Set the value in field with the given id
function fncInputSetValue( cIdCode, cValue ) {
  var oField ;

  oField = document.getElementById( cIdCode );
  if (oField != null)  {
     oField.value = cValue;
  }
}

function fncInputSetCheck( cIdCode, bValue ) {
  var oField ;

  oField = document.getElementById( cIdCode );
  if (oField != null)  {
     oField.checked = bValue;
  }
}


// Get the field input value from the given id
function fncInputGetValue( cIdCode ) {
  var oField ;
  var cValue = null;

  oField = document.getElementById( cIdCode );
  if (oField != null)  {
     cValue = oField.value;
  }
  return cValue;
}

function fncInputGetCheck( cIdCode ) {
  var oField ;
  var bValue = null;

  oField = document.getElementById( cIdCode );
  if (oField != null)  {
     bValue = oField.checked;
  }
  return bValue;
}


// Get the field input value convert if into a number for the given id
// If it is not a number throw an exception where that's begin with the given description
function fncInputGetNumber( cIdCode, cDesc ) {
  var oField ;
  var cValue = null;
  var dValue = null;

  oField = document.getElementById( cIdCode );
  if (oField != null)  {
     cValue = oField.value;
  }

  if ( isNaN( cValue )  ) {
    if (cValue == null) {
      cValue = "null";
    }
    throw cDesc + ": " + cValue + " is not a number.";
    return null;
  }
  dValue = Number( cValue );

  return dValue;
}

// Get the fields of the given number and put them all in a json object`
function fncFieldGet( cDivNo ) {
   var data = {};

   data.name       = fncInputGetValue(  "inputFieldCode_"    + cDivNo, "Code"    );
   data.formula    = fncInputGetValue(  "inputFieldFormula_" + cDivNo, "Formula" );

   data.varCalc    = fncInputGetValue(  "inputFieldVarCalc_" + cDivNo, "Step variable"    );
   data.varStep    = fncInputGetNumber( "inputFieldVarStep_" + cDivNo, "Step calculation" );

   data.xFrom      = fncInputGetNumber( "inputFieldXFrom_"   + cDivNo, "X from" );
   data.xTo        = fncInputGetNumber( "inputFieldXTo_"     + cDivNo, "X to"   );
   data.xStep      = fncInputGetNumber( "inputFieldXStep_"   + cDivNo, "X step" );

   data.yFrom      = fncInputGetNumber( "inputFieldYFrom_"   + cDivNo, "Y from" );
   data.yTo        = fncInputGetNumber( "inputFieldYTo_"     + cDivNo, "Y to"   );
   data.yStep      = fncInputGetNumber( "inputFieldYStep_"   + cDivNo, "Y step" );

   data.colorGraphLine   = fncInputGetValue(  "inputFieldColorGraphLine_"    + cDivNo, "Color line"   );
   data.colorGraphAxe    = fncInputGetValue(  "inputFieldColorGraphAxe_"     + cDivNo, "Color axe"    );
   data.colorGraphNumber = fncInputGetValue(  "inputFieldColorGraphNumber_"  + cDivNo, "Color number" );
   data.colorGraphGrid   = fncInputGetValue(  "inputFieldColorGraphGrid_"    + cDivNo, "Color grid"   );

   data.showGraphAxe    = fncInputGetCheck(  "inputCheckColorGraphAxe_"     + cDivNo, "Color axe"    );
   data.showGraphNumber = fncInputGetCheck(  "inputCheckColorGraphNumber_"  + cDivNo, "Color number" );
   data.showGraphGrid   = fncInputGetCheck(  "inputCheckColorGraphGrid_"    + cDivNo, "Color grid"   );

   // collect all the fixed vars with values
   data.fixedVars = {} ;

   var iCnt       ;
   var cFieldName ;
   var oField     ;

   iCnt = 0;
   do {
     iCnt++;
     cFieldName = "inputFieldFixedName_" + iCnt.toString() + "_" + cDivNo ;
     oField     = document.getElementById( cFieldName );
     if (oField != null) {
       var oFldData = {};
       oFldData.varName  = fncInputGetValue( "inputFieldFixedName_"  + iCnt.toString() + "_" + cDivNo );
       oFldData.varValue = fncInputGetValue( "inputFieldFixedValue_" + iCnt.toString() + "_" + cDivNo );

       if ( oFldData.varName ) {
         data.fixedVars[ oFldData.varName ] = oFldData.varValue;
       }
     }
   } while( oField != null );

   return data;
}

// Set the defaults values in a given formula div
function fncGraphSetDefaults( cDivNo ) {
  fncInputSetValue( "inputFieldCode_"    + cDivNo, "" );
  fncInputSetValue( "inputFieldFormula_" + cDivNo, "" );

  fncInputSetValue( "inputFieldVarCalc_" + cDivNo, "x"   );
  fncInputSetValue( "inputFieldVarStep_" + cDivNo, "0.1" );

  fncInputSetValue( "inputFieldXFrom_"   + cDivNo, "-10" );
  fncInputSetValue( "inputFieldXTo_"     + cDivNo,  "10" );
  fncInputSetValue( "inputFieldXStep_"   + cDivNo,   "1" );

  fncInputSetValue( "inputFieldYFrom_"   + cDivNo, "-10" );
  fncInputSetValue( "inputFieldYTo_"     + cDivNo,  "10" );
  fncInputSetValue( "inputFieldYStep_"   + cDivNo,   "1" );

  fncInputSetValue( "inputFieldColorGraphLine_"   + cDivNo, getHexColor( "red"       ));
  fncInputSetValue( "inputFieldColorGraphAxe_"    + cDivNo, getHexColor( "black"     ));
  fncInputSetValue( "inputFieldColorGraphNumber_" + cDivNo, getHexColor( "lightgray" ));
  fncInputSetValue( "inputFieldColorGraphGrid_"   + cDivNo, getHexColor( "lightgray" ));

  fncInputSetCheck( "inputCheckColorGraphAxe_"    + cDivNo, true);
  fncInputSetCheck( "inputCheckColorGraphNumber_" + cDivNo, true);
  fncInputSetCheck( "inputCheckColorGraphGrid_"   + cDivNo, true);

  for( iCount = 1; iCount < glbMaxFixedFields; iCount++ ) {
    fncInputSetValue( "inputFieldFixedName_"  + iCount.toString() + "_" + cDivNo, "" );
    fncInputSetValue( "inputFieldFixedValue_" + iCount.toString() + "_" + cDivNo, "" );
  }
}


function fncFieldsUpdate( cDivNo, dataJson ) {
   fncGraphSetDefaults( cDivNo );

   if ( 'name'    in dataJson ) { fncInputSetValue( "inputFieldCode_"    + cDivNo, dataJson.name    ); }
   if ( 'formula' in dataJson ) { fncInputSetValue( "inputFieldFormula_" + cDivNo, dataJson.formula ); }
   if ( 'varCalc' in dataJson ) { fncInputSetValue( "inputFieldVarCalc_" + cDivNo, dataJson.varCalc ); }
   if ( 'varStep' in dataJson ) { fncInputSetValue( "inputFieldVarStep_" + cDivNo, dataJson.varStep ); }
   if ( 'xFrom'   in dataJson ) { fncInputSetValue( "inputFieldXFrom_"   + cDivNo, dataJson.xFrom   ); }
   if ( 'xTo'     in dataJson ) { fncInputSetValue( "inputFieldXTo_"     + cDivNo, dataJson.xTo     ); }
   if ( 'xStep'   in dataJson ) { fncInputSetValue( "inputFieldXStep_"   + cDivNo, dataJson.xStep   ); }
   if ( 'yFrom'   in dataJson ) { fncInputSetValue( "inputFieldYFrom_"   + cDivNo, dataJson.yFrom   ); }
   if ( 'yTo'     in dataJson ) { fncInputSetValue( "inputFieldYTo_"     + cDivNo, dataJson.yTo     ); }
   if ( 'yStep'   in dataJson ) { fncInputSetValue( "inputFieldYStep_"   + cDivNo, dataJson.yStep   ); }

   if ( 'colorGraphLine'   in dataJson ) { fncInputSetValue( "inputFieldColorGraphLine_"   + cDivNo, dataJson.colorGraphLine   ); }
   if ( 'colorGraphAxe'    in dataJson ) { fncInputSetValue( "inputFieldColorGraphAxe_"    + cDivNo, dataJson.colorGraphAxe    ); }
   if ( 'colorGraphNumber' in dataJson ) { fncInputSetValue( "inputFieldColorGraphNumber_" + cDivNo, dataJson.colorGraphNumber ); }
   if ( 'colorGraphGrid'   in dataJson ) { fncInputSetValue( "inputFieldColorGraphGrid_"   + cDivNo, dataJson.colorGraphGrid   ); }
   if ( 'showGraphAxe'     in dataJson ) { fncInputSetCheck( "inputCheckColorGraphAxe_"    + cDivNo, dataJson.showGraphAxe     ); }
   if ( 'showGraphNumber'  in dataJson ) { fncInputSetCheck( "inputCheckColorGraphNumber_" + cDivNo, dataJson.showGraphNumber  ); }
   if ( 'showGraphGrid'    in dataJson ) { fncInputSetCheck( "inputCheckColorGraphGrid_"   + cDivNo, dataJson.showGraphGrid    ); }

   if ( 'fixedVars' in dataJson ) {
     var iCnt = 0;
     for (var key in dataJson.fixedVars) {
       iCnt++;
       fncInputSetValue( "inputFieldFixedName_"  + iCnt.toString() + "_" + cDivNo, key );
       fncInputSetValue( "inputFieldFixedValue_" + iCnt.toString() + "_" + cDivNo, dataJson.fixedVars[ key ] );
     }
   }

   // reset graphLine
   glbTools.dictLines[ cDivNo ].deleteElement();
   glbTools.dictLines[ cDivNo ].setPoints( [] );

   if ( 'calcedValues' in dataJson ) {
     glbTools.dictLines[ cDivNo ].setPoints( dataJson.calcedValues );
   }
}

function fncGraphHide( cDivNo ) {
   glbTools.dictGraph[ cDivNo ].deleteElement();
   glbTools.dictLines[ cDivNo ].deleteElement();

   var butSmaller = document.getElementById( "buttonInputSmaller_" + cDivNo  );

   butSmaller.style.backgroundColor  = "";
}

//
// Get the data from the given key and set it in the display fields
//
async function asyncSaveInputData( cDivNo, options = "", callBackFunc = null) {
  try {
     fieldInputDisable( cDivNo, true );

     url = '?prog=graphJsonSave&options=' + options  ;

     data       = fncFieldGet( cDivNo );
     dataString = JSON.stringify(data);

     config = {
        method: 'POST',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        },
        body: dataString
     }
     response = await fetch( url, config );

     if (!response.ok) {
        dataJson = await response.json();
        dataString = dataJson[ 'error' ];
        alert( 'Error save data response: ' + response.status + "  " + dataString );
     } else {
        dataJson = await response.json();

        fncFieldsUpdate( cDivNo, dataJson );

        if (callBackFunc != null) {
          callBackFunc( cDivNo );
        }
     }
  } catch(err) {
    alert( 'Error save data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( cDivNo, false );
  }
}

function fncGraphSave( cDivNo ) {
  try {
    asyncSaveInputData( cDivNo );
  }
  catch(err) {
    window.alert("Error: " + err );
  }
}


//
// Get the list
//
async function asyncDataList( fncCallBack, options = "" ) {
  try {
     url = '?prog=graphJsonList&options=' + options  ;

     dataString = "{}";

     config = {
        method: 'POST',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        },
        body: dataString
     }
     response = await fetch( url, config );

     if (!response.ok) {
        dataJson = await response.json();
        dataString = dataJson[ 'error' ];
        alert( 'Error list data response: ' + response.status + "  " + dataString );
     } else {
        dataJson = await response.json();

        fncCallBack( dataJson );
     }
  } catch(err) {
    alert( 'Error list data ' + err );
  }
  finally {
    // nothing at the moment
  }
}

//
// (re)draw the graph
//
function fncGraphRedraw( cDivNo ) {
  try {
    data = fncFieldGet( cDivNo );

    // console.log( data );
    if ( data.xFrom >= data.xTo) {
      throw "The 'X to' value must be greater then the 'X from' value";
    }
    if ( data.xStep <= 0) {
      throw "The 'X step' must be greater then zero";
    }

    if ( data.yFrom >= data.yTo ) {
      throw "The 'Y to' value must be greater then the 'Y from' value";
    }
    if ( data.yStep <= 0 ) {
      throw "The 'Y step' must be greater then zero";
    }

    // - format graph field
    glbTools.dictGraph[ cDivNo ].setX( data.xFrom, data.xTo, data.xStep ) ;
    glbTools.dictGraph[ cDivNo ].setY( data.yFrom, data.yTo, data.yStep ) ;

    glbTools.dictGraph[ cDivNo ].setAxe(    data.colorGraphAxe    ,null,null, data.showGraphAxe    );
    glbTools.dictGraph[ cDivNo ].setNumber( data.colorGraphNumber ,null,null, data.showGraphNumber );
    glbTools.dictGraph[ cDivNo ].setGrid(   data.colorGraphGrid   ,null,null, data.showGraphGrid   );

    // redraw graph
    glbTools.dictGraph[ cDivNo ].createGraph();

    // drawLine
    glbTools.dictLines[ cDivNo ].setColor( data.colorGraphLine ) ;
    glbTools.dictLines[ cDivNo ].createGraphLine();

    var butSmaller = document.getElementById( "buttonInputSmaller_" + cDivNo  );

    butSmaller.style.backgroundColor  = data.colorGraphLine;
  }
  catch(err) {
    window.alert("Error: " + err );
  }
}

function fncGraphCalc( cDivNo ) {
  try {
    //
    // save data with option calc
    //
    asyncSaveInputData( cDivNo, "calc", fncGraphRedraw );
  }
  catch(err) {
    window.alert("Error: " + err );
  }
}


//
// Get the data from the given key and set it in the display fields
//
async function asyncDownloadInputData(key, cDivNo) {
  try {
     fieldInputDisable( cDivNo, true );

     if (key == null || key == "" ) {
        fncFieldsUpdate( cDivNo, {} );
        return;
     }

     url = '?prog=graphJsonData&key=' + key ;

     config = {
        method: 'GET',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        }
     }
     response = await fetch( url, config );

     if (!response.ok) {
        alert( 'Error read data response: ' + response.status );
     } else {
        dataJson = await response.json();

        fncFieldsUpdate( cDivNo, dataJson );
     }
  } catch(err) {
    alert( 'Error read data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( cDivNo, false );
  }
}


function fncGraphDestroy( cDivNo ) {
  try {
    var divFormula = document.getElementById( "divFormula_" + cDivNo  );
    if (divFormula != null) {

      glbTools.dictGraph[ cDivNo ].deleteElement();
      glbTools.dictLines[ cDivNo ].deleteElement();

      delete glbTools.dictGraph[ cDivNo ];
      delete glbTools.dictLines[ cDivNo ];

      divFormula.parentNode.removeChild( divFormula );
    }
  }
  catch(err) {
    window.alert("Error: " + err );
  }
}


function fncGraphDelete( cDivNo ) {
  try {
    //
    // save data with option calc
    //
    asyncDeleteInputData( cDivNo );
  }
  catch(err) {
    window.alert("Error: " + err );
  }
}


//
// Get the data from the given key and set it in the display fields
//
async function asyncDeleteInputData(cDivNo) {
  try {
     fieldInputDisable( cDivNo, true );

     data = fncFieldGet( cDivNo );

     url = '?prog=graphJsonDelete&key=' + data.name ;

     config = {
        method: 'DELETE',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        }
     }
     response = await fetch( url, config );

     if (!response.ok) {
        alert( 'Error delete data response: ' + response.status );
     } else {
       fncGraphDestroy( cDivNo );
     }
  } catch(err) {
    console.error(err);
    alert( 'Error delete data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( cDivNo, false );
  }
}
