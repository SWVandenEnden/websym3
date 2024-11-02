/*

*/

// init after load page
window.onload = initJavascript ;

var name_selectMathThirdpower   = "selectMathThirdpower";

var name_inputFieldCode         = "inputFieldCode"       ;
var name_inputFieldDescription  = "inputFieldDescription";
var name_inputFieldA            = "inputFieldA" ;
var name_inputFieldB            = "inputFieldB" ;
var name_inputFieldC            = "inputFieldC" ;
var name_inputFieldD            = "inputFieldD" ;

var name_buttonSave             = "buttonSave"       ;
var name_buttonSaveCalc         = "buttonSaveCalc"   ;
var name_buttonDelete           = "buttonDelete"     ;
var name_iframeDisplay          = "iframeDisplay"    ;

var name_inputFormulaCalc       = "inputFormulaCalc";


var elem_selectMathThirdpower   = null;

var elem_inputFieldCode         = null;
var elem_inputFieldDescription  = null;
var elem_inputFieldA            = null;
var elem_inputFieldB            = null;
var elem_inputFieldC            = null;
var elem_inputFieldD            = null;

var elem_buttonSave             = null;
var elem_buttonSaveCalc         = null;
var elem_buttonDelete           = null;
var elem_iframeDisplay          = null;

var elem_inputFormulaCalc       = null;


var fieldInputArray = []; // array of field handle to enable/disable by db actions

//
// init the page after loading
//
function initJavascript() {
  // set all the objects in global variables
  elem_selectMathThirdpower  = document.getElementById( name_selectMathThirdpower   );

  elem_inputFieldCode        = document.getElementById( name_inputFieldCode         );
  elem_inputFieldDescription = document.getElementById( name_inputFieldDescription  );
  elem_inputFieldA           = document.getElementById( name_inputFieldA            );
  elem_inputFieldB           = document.getElementById( name_inputFieldB            );
  elem_inputFieldC           = document.getElementById( name_inputFieldC            );
  elem_inputFieldD           = document.getElementById( name_inputFieldD            );

  elem_buttonSave            = document.getElementById( name_buttonSave             );
  elem_buttonSaveCalc        = document.getElementById( name_buttonSaveCalc         );
  elem_buttonDelete          = document.getElementById( name_buttonDelete           );
  elem_iframeDisplay         = document.getElementById( name_iframeDisplay          );

  elem_inputFormulaCalc      = document.getElementById( name_inputFormulaCalc       );


  elem_selectMathThirdpower.addEventListener("change", fncSelectMathChange    );
  elem_buttonSave.addEventListener(          "click" , fncButtonSavePress     );
  elem_buttonSaveCalc.addEventListener(      "click" , fncButtonSaveCalcPress );
  elem_buttonDelete.addEventListener(        "click" , fncButtonDeletePress   );

  // array of fields to enable/disable by save actions
  fieldInputArray.push( elem_selectMathThirdpower );

  fieldInputArray.push( elem_inputFieldCode       );
  fieldInputArray.push( elem_inputFieldDescription);
  fieldInputArray.push( elem_inputFieldA          );
  fieldInputArray.push( elem_inputFieldB          );
  fieldInputArray.push( elem_inputFieldC          );
  fieldInputArray.push( elem_inputFieldD          );

  fieldInputArray.push( elem_buttonSave           );
  fieldInputArray.push( elem_buttonSaveCalc       );
  fieldInputArray.push( elem_buttonDelete         );
  fieldInputArray.push( elem_iframeDisplay );

  fieldInputArray.push( elem_inputFormulaCalc     );


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
   for ( iCount = 0; iCount < elem_selectMathThirdpower.length; iCount++ ) {
     if (elem_selectMathThirdpower.options[ iCount ].value == key )
        elem_selectMathThirdpower.remove( iCount );
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

//
// update the field on screen from the given json
//
function fncFieldsUpdate( dataJson ) {
   if ( 'name'  in dataJson ) {
      elem_inputFieldCode.value = dataJson.name;

      // update select if name if not the current (is does not exist in the list)
      var currentValue = elem_selectMathThirdpower.value;
      if ( currentValue != dataJson.name ) {
        var option = document.createElement("option");
        option.text = dataJson.name;
        elem_selectMathThirdpower.add( option );
        elem_selectMathThirdpower.value = dataJson.name;
      }

   } else {
      elem_inputFieldCode.value = "";
   }

   if ( 'description'  in dataJson ) {
      elem_inputFieldDescription.value  = dataJson.description;
   } else {
      elem_inputFieldDescription.value  = "";
   }

   if ( 'a'  in dataJson ) {
      elem_inputFieldA.value  = dataJson.a;
   } else {
      elem_inputFieldA.value  = "";
   }

   if ( 'b'  in dataJson ) {
      elem_inputFieldB.value  = dataJson.b;
   } else {
      elem_inputFieldB.value  = "";
   }

   if ( 'c'  in dataJson ) {
      elem_inputFieldC.value  = dataJson.c;
   } else {
      elem_inputFieldC.value  = "";
   }

   if ( 'd'  in dataJson ) {
      elem_inputFieldD.value  = dataJson.d;
   } else {
      elem_inputFieldD.value  = "";
   }

   if ( 'htmlDisplay'  in dataJson ) {
      elem_iframeDisplay.src = "data:text/html;charset=utf-8," + escape(dataJson.htmlDisplay);
   } else {
      elem_iframeDisplay.src = "data:text/html;charset=utf-8," + '<!doctype html><html><body></body></html>';
   }

   if ( 'calcValue'  in dataJson ) {
      elem_inputFormulaCalc.checked  = dataJson.calcValue;
   } else {
      elem_inputFormulaCalc.checked  = false;
   }
}

//
// get the data form the input fields and set it in a json
//
function fncFieldGet() {
   data = {};
   data.name         = elem_inputFieldCode.value        ;
   data.description  = elem_inputFieldDescription.value ;
   data.a            = elem_inputFieldA.value           ;
   data.b            = elem_inputFieldB.value           ;
   data.c            = elem_inputFieldC.value           ;
   data.d            = elem_inputFieldD.value           ;
   data.calcValue    = elem_inputFormulaCalc.checked    ;

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

     url = '?prog=thirdpowerJsonData&key=' + key ;

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

     url = '?prog=thirdpowerJsonSave&options=' + options  ;

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

     url = '?prog=thirdpowerJsonDelete&key=' + key ;

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
  asyncDownloadInputData( elem_selectMathThirdpower.value );
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
