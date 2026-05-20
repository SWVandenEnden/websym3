/*

*/

// init after load page
window.onload = initJavascript ;

var name_selectMathResultant    = "selectMathResultant";

var name_inputFieldCode         = "inputFieldCode"     ;
var name_inputFieldFormula1     = "inputFieldFormula1" ;
var name_inputFieldFormula2     = "inputFieldFormula2" ;
var name_inputFieldVariable     = "inputFieldVariable" ;

var name_buttonSave             = "buttonSave"       ;
var name_buttonSaveCalc         = "buttonSaveCalc"   ;
var name_buttonDelete           = "buttonDelete"     ;
var name_iframeDisplay          = "iframeDisplay"    ;


var elem_selectMathResultant    = null;

var elem_inputFieldCode         = null;
var elem_inputFieldFormula1     = null;
var elem_inputFieldFormula2     = null;
var elem_inputFieldVariable     = null;

var elem_buttonSave             = null;
var elem_buttonSaveCalc         = null;
var elem_buttonDelete           = null;
var elem_iframeDisplay          = null;

var fieldInputArray = []; // array of field handle to enable/disable by db actions

//
// init the page after loading
//
function initJavascript() {
  // set all the objects in global variables
  elem_selectMathResultant   = document.getElementById( name_selectMathResultant   );

  elem_inputFieldCode        = document.getElementById( name_inputFieldCode         );
  elem_inputFieldFormula1    = document.getElementById( name_inputFieldFormula1     );
  elem_inputFieldFormula2    = document.getElementById( name_inputFieldFormula2     );
  elem_inputFieldVariable    = document.getElementById( name_inputFieldVariable     );

  elem_buttonSave            = document.getElementById( name_buttonSave             );
  elem_buttonSaveCalc        = document.getElementById( name_buttonSaveCalc         );
  elem_buttonDelete          = document.getElementById( name_buttonDelete           );
  elem_iframeDisplay         = document.getElementById( name_iframeDisplay          );


  elem_selectMathResultant.addEventListener(  "change", fncSelectMathChange    );
  elem_buttonSave.addEventListener(           "click" , fncButtonSavePress     );
  elem_buttonSaveCalc.addEventListener(       "click" , fncButtonSaveCalcPress );
  elem_buttonDelete.addEventListener(         "click" , fncButtonDeletePress   );

  // array of fields to enable/disable by save actions
  fieldInputArray.push( elem_selectMathResultant  );

  fieldInputArray.push( elem_inputFieldCode       );
  fieldInputArray.push( elem_inputFieldFormula1   );
  fieldInputArray.push( elem_inputFieldFormula2   );
  fieldInputArray.push( elem_inputFieldVariable   );

  fieldInputArray.push( elem_buttonSave           );
  fieldInputArray.push( elem_buttonSaveCalc       );
  fieldInputArray.push( elem_buttonDelete         );
  fieldInputArray.push( elem_iframeDisplay );

  fieldInputDisable( false ); // default all fields enabled

  // init scherm velden
  fncSelectMathChange();
}

//
// enable/disable the input fields
// true  = disable
// false = enable
//
function fieldInputDisable( state ) {
  for ( iCount = 0; iCount < fieldInputArray.length; iCount++) {
    fieldInputArray[ iCount ].disabled  = state ;
  }
}

function fieldDeleteFromSelect( key ) {
   for ( iCount = 0; iCount < elem_selectMathResultant.length; iCount++ ) {
     if (elem_selectMathResultant.options[ iCount ].value == key )
        elem_selectMathResultant.remove( iCount );
   }
}

function fncSelectValue( selectElem, key ) {
   for ( iCount = 0; iCount < selectElem.length; iCount++ ) {
     if (selectElem.options[ iCount ].value == key ) {
        selectElem.selectedIndex = iCount;
        return true;
     }
   }
   return false
}


function fncSelectMakeEmpty( selectElem ) {
   var iCount;
   var elemLength = selectElem.options.length - 1;

   for(iCount = elemLength; iCount >= 0; iCount--) {
      selectElem.remove(iCount);
   }
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

  if (cValue == "") {
    dValue = null
  } else {
    dValue = Number( cValue );
  }

  return dValue;
}


//
// update the field on screen from the given json
//
function fncFieldsUpdate( dataJson ) {
   if ( 'name'  in dataJson ) {
      elem_inputFieldCode.value = dataJson.name;

      // update select if name if not the current (is does not exist in the list)
      var currentValue = elem_selectMathResultant.value;
      if ( currentValue != dataJson.name ) {
        var option = document.createElement("option");
        option.text = dataJson.name;
        elem_selectMathResultant.add( option );
        elem_selectMathResultant.value = dataJson.name;
      }

   } else {
      elem_inputFieldCode.value = "";
   }

   if ( 'formula1'  in dataJson ) {
      elem_inputFieldFormula1.value  = dataJson.formula1;
   } else {
      elem_inputFieldFormula1.value  = "";
   }

   if ( 'formula2'  in dataJson ) {
      elem_inputFieldFormula2.value  = dataJson.formula2;
   } else {
      elem_inputFieldFormula2.value  = "";
   }


   if ( 'variable'  in dataJson ) {
      elem_inputFieldVariable.value  = dataJson.variable;
   } else {
      elem_inputFieldVariable.value  = "";
   }

   if ( 'htmlDisplay'  in dataJson ) {
      elem_iframeDisplay.src = "data:text/html;charset=utf-8," + escape(dataJson.htmlDisplay);
   } else {
      elem_iframeDisplay.src = "data:text/html;charset=utf-8," + '<!doctype html><html><body></body></html>';
   }

}

//
// get the data form the input fields and set it in a json
//
function fncFieldGet() {
   data = {};
   data.name       = elem_inputFieldCode.value     ;
   data.formula1   = elem_inputFieldFormula1.value ;
   data.formula2   = elem_inputFieldFormula2.value ;
   data.variable   = elem_inputFieldVariable.value ;

   return data;
}

//
// Get the data from the given key and set it in the display fields
//
async function asyncDownloadInputData(key) {
  try {
     fieldInputDisable( true );

     if (key == null || key == "" ) {
        fncFieldsUpdate( {} );
        return;
     }

     url = '?prog=resultantJsonData&key=' + key ;

     config = {
        method: 'GET',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        }
     }
     response = await fetch( url, config );

     if (!response.ok) {
        alert( 'Error load data response: ' + response.status );
     } else {
        dataJson = await response.json();
        fncFieldsUpdate( dataJson );
     }
  } catch(err) {
    console.error(err);
    alert( 'Error load data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( false );
  }
}


//
// Get the data from the given key and set it in the display fields
//
async function asyncSaveInputData( options = "" ) {
  try {
     fieldInputDisable( true );

     url = '?prog=resultantJsonSave&options=' + options  ;

     data       = fncFieldGet();
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
        fncFieldsUpdate( dataJson );
     }
  } catch(err) {
    alert( 'Error save data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( false );
  }
}


//
// Get the data from the given key and set it in the display fields
//
async function asyncDeleteInputData(key) {
  try {
     fieldInputDisable( true );

     url = '?prog=resultantJsonDelete&key=' + key ;

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
        fieldDeleteFromSelect( key )
        // empty fields
        dataJson = {}; // await response.json();
        fncFieldsUpdate( dataJson );
     }
  } catch(err) {
    alert( 'Error delete data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( false );
  }
}

//
// by value change of list keys, get the data and display it
//
function fncSelectMathChange() {
  asyncDownloadInputData( elem_selectMathResultant.value );
}

function fncButtonSavePress() {
   asyncSaveInputData();
}

function fncButtonSaveCalcPress() {
   asyncSaveInputData( "calc" );
}

function fncButtonDeletePress() {
   keyValue = elem_inputFieldCode.value;
   if (keyValue == "" ) {
      return;
   }
   asyncDeleteInputData( keyValue );
}
