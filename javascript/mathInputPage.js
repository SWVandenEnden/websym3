/*
  
*/

// init after load page
window.onload = initJavascript ;

var name_selectMathFormula    = "selectMathFormula";
var name_inputFieldCode       = "inputFieldCode"   ;
var name_inputFieldFormula    = "inputFieldFormula";
var name_buttonSave           = "buttonSave"       ;
var name_buttonSaveCalc       = "buttonSaveCalc"   ;
var name_buttonDelete         = "buttonDelete"     ;
var name_iframeDisplayFormula = "iframeDisplayFormula";

var name_inputFieldCalcType           = "inputFieldCalcType"          ;
var name_inputFormulaCalc             = "inputFormulaCalc"            ;
var name_inputFormulaReplace          = "inputFormulaReplace"         ;
var name_inputFieldOptimzeCustom      = "inputFieldOptimzeCustom"     ;
var name_buttonInputFieldAddCustom    = "buttonInputFieldAddCustom"   ;
var name_buttonInputFieldRemoveCustom = "buttonInputFieldRemoveCustom"; 
var name_inputFieldOptimzeSelected    = "inputFieldOptimzeSelected"   ;
var name_buttonInputFieldUpCustom     = "buttonInputFieldUpCustom"    ;
var name_buttonInputFieldDownCustom   = "buttonInputFieldDownCustom"  ;

var name_inputFormulaVarName          = "inputFormulaVarName"       ;
var name_inputFormulaVarValue         = "inputFormulaVarValue"      ;
var name_buttonSelectVariableAdd      = "buttonSelectVariableAdd"   ;
var name_buttonSelectVariableRemove   = "buttonSelectVariableRemove";
var name_selectVariable               = "selectVariable"            ;


var elem_selectMathFormula    = null;
var elem_inputFieldCode       = null;
var elem_inputFieldFormula    = null;
var elem_buttonSave           = null;
var elem_buttonSaveCalc       = null;
var elem_iframeDisplayFormula = null;
var elem_buttonDelete         = null;

var elem_inputFieldCalcType           = null;
var elem_inputFormulaCalc             = null;
var elem_inputFormulaReplace          = null;
var elem_inputFieldOptimzeCustom      = null;
var elem_buttonInputFieldAddCustom    = null;
var elem_buttonInputFieldRemoveCustom = null;
var elem_inputFieldOptimzeSelected    = null;
var elem_buttonInputFieldUpCustom     = null;
var elem_buttonInputFieldDownCustom   = null;

var elem_inputFormulaVarName          = null;
var elem_inputFormulaVarValue         = null;
var elem_buttonSelectVariableAdd      = null;
var elem_buttonSelectVariableRemove   = null;
var elem_selectVariable               = null;

var fieldInputArray = []; // array of field handle to enable/disable by db actions

//
// init the page after loading
//
function initJavascript() {
  // set all the objects in global variables
  elem_selectMathFormula            = document.getElementById( name_selectMathFormula    );
  elem_inputFieldCode               = document.getElementById( name_inputFieldCode       );
  elem_inputFieldFormula            = document.getElementById( name_inputFieldFormula    );
  elem_buttonSave                   = document.getElementById( name_buttonSave           );
  elem_buttonSaveCalc               = document.getElementById( name_buttonSaveCalc       );
  elem_buttonDelete                 = document.getElementById( name_buttonDelete         );
  elem_iframeDisplayFormula         = document.getElementById( name_iframeDisplayFormula );

  elem_inputFieldCalcType           = document.getElementById( name_inputFieldCalcType           );
  elem_inputFormulaCalc             = document.getElementById( name_inputFormulaCalc             );
  elem_inputFormulaReplace          = document.getElementById( name_inputFormulaReplace          );
  elem_inputFieldOptimzeCustom      = document.getElementById( name_inputFieldOptimzeCustom      );
  elem_buttonInputFieldAddCustom    = document.getElementById( name_buttonInputFieldAddCustom    );
  elem_buttonInputFieldRemoveCustom = document.getElementById( name_buttonInputFieldRemoveCustom );
  elem_inputFieldOptimzeSelected    = document.getElementById( name_inputFieldOptimzeSelected    );
  elem_buttonInputFieldUpCustom     = document.getElementById( name_buttonInputFieldUpCustom     );
  elem_buttonInputFieldDownCustom   = document.getElementById( name_buttonInputFieldDownCustom   );

  elem_inputFormulaVarName          = document.getElementById( name_inputFormulaVarName          );
  elem_inputFormulaVarValue         = document.getElementById( name_inputFormulaVarValue         );
  elem_buttonSelectVariableAdd      = document.getElementById( name_buttonSelectVariableAdd      );
  elem_buttonSelectVariableRemove   = document.getElementById( name_buttonSelectVariableRemove   );
  elem_selectVariable               = document.getElementById( name_selectVariable               );


  elem_selectMathFormula.addEventListener("change", fncSelectMathFormulaChange);
  elem_buttonSave.addEventListener(       "click" , fncButtonSavePress        );
  elem_buttonSaveCalc.addEventListener(   "click" , fncButtonSaveCalcPress    );
  elem_buttonDelete.addEventListener(     "click" , fncButtonDeletePress      );
  
  elem_buttonInputFieldAddCustom.addEventListener(       "click" , fncButtonInputFieldAddCustomPress        );
  elem_buttonInputFieldRemoveCustom.addEventListener(    "click" , fncButtonInputFieldRemoveCustomPress     );
  elem_buttonInputFieldUpCustom.addEventListener(        "click" , fncButtonInputFieldUpCustomPress         );
  elem_buttonInputFieldDownCustom.addEventListener(      "click" , fncButtonInputFieldDownCustomPress       );

  elem_buttonSelectVariableAdd.addEventListener(         "click" , fncButtonSelectVariableAddPress          );
  elem_buttonSelectVariableRemove.addEventListener(      "click" , fncButtonSelectVariableRemovePress       );

  // array of field to disable/enable by create/update/delete actions
  fieldInputArray.push( elem_selectMathFormula );
  fieldInputArray.push( elem_inputFieldCode    );
  fieldInputArray.push( elem_inputFieldFormula );
  fieldInputArray.push( elem_buttonSave        );
  fieldInputArray.push( elem_buttonSaveCalc    );
  fieldInputArray.push( elem_buttonDelete      ); 
  
  fieldInputArray.push( elem_inputFieldCalcType           ); 
  fieldInputArray.push( elem_inputFormulaCalc             ); 
  fieldInputArray.push( elem_inputFormulaReplace          ); 
  fieldInputArray.push( elem_inputFieldOptimzeCustom      ); 
  fieldInputArray.push( elem_buttonInputFieldAddCustom    ); 
  fieldInputArray.push( elem_buttonInputFieldRemoveCustom ); 
  fieldInputArray.push( elem_inputFieldOptimzeSelected    ); 
  fieldInputArray.push( elem_buttonInputFieldUpCustom     ); 
  fieldInputArray.push( elem_buttonInputFieldDownCustom   ); 

  fieldInputArray.push( elem_inputFormulaVarName          );
  fieldInputArray.push( elem_inputFormulaVarValue         );
  fieldInputArray.push( elem_buttonSelectVariableAdd      );
  fieldInputArray.push( elem_buttonSelectVariableRemove   );
  fieldInputArray.push( elem_selectVariable               );
  
  
  fieldInputDisable( false ); // default all fields enabled
  
  // init screen fields
  fncSelectMathFormulaChange();
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
   for ( iCount = 0; iCount < elem_selectMathFormula.length; iCount++ ) {
     if (elem_selectMathFormula.options[ iCount ].value == key )
        elem_selectMathFormula.remove( iCount );
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
      var currentValue = elem_selectMathFormula.value;
      if ( currentValue != dataJson.name ) {
        var option = document.createElement("option");
        option.text = dataJson.name;
        elem_selectMathFormula.add( option );
        elem_selectMathFormula.value = dataJson.name;
      }
      
   } else {
      elem_inputFieldCode.value = "";
   }      
   
   if ( 'formula'  in dataJson ) {
      elem_inputFieldFormula.value  = dataJson.formula;
   } else {
      elem_inputFieldFormula.value  = "";
   }
   
   if ( 'htmlDisplay'  in dataJson ) {
      elem_iframeDisplayFormula.src = "data:text/html;charset=utf-8," + escape(dataJson.htmlDisplay);
   } else {
      elem_iframeDisplayFormula.src = "data:text/html;charset=utf-8," + '<!doctype html><html><body></body></html>';
   }
   
   if ( 'optimizeType'  in dataJson ) {
      elem_inputFieldCalcType.value  = dataJson.optimizeType;
   } else {
      elem_inputFieldCalcType.value  = "";
   }

   if ( 'calcValue'  in dataJson ) {
      elem_inputFormulaCalc.checked  = dataJson.calcValue;
   } else {
      elem_inputFormulaCalc.checked  = false;
   }

   if ( 'replaceValue'  in dataJson ) {
      elem_inputFormulaReplace.checked  = dataJson.replaceValue;
   } else {
      elem_inputFormulaReplace.checked  = false;
   }


   fncSelectMakeEmpty( elem_inputFieldOptimzeSelected )
   var orgSelectIndex = elem_inputFieldOptimzeCustom.selectedIndex ;
   if ( 'optimizeList'  in dataJson ) {
      var lenArr = dataJson.optimizeList.length
      var iCount ;
      for( iCount = 0; iCount < lenArr; iCount++ ) {
         var curElem = dataJson.optimizeList[ iCount ];
         
         if ( fncSelectValue( elem_inputFieldOptimzeCustom, curElem) == true ) {
            fncButtonInputFieldAddCustomPress();
         }
      }
   }
   elem_inputFieldOptimzeCustom.selectedIndex = orgSelectIndex;
   
   
   fncSelectMakeEmpty( elem_selectVariable );
   if ( 'varList'  in dataJson ) {
      for( key in dataJson.varList ) {
        elem_inputFormulaVarName.value  = key ;
        elem_inputFormulaVarValue.value = dataJson.varList[ key ] ;
        fncButtonSelectVariableAddPress();
      }         
   }
   elem_inputFormulaVarName.value  = "" ;
   elem_inputFormulaVarValue.value = "" ;
   
}

//
// get the data form the input fields and set it into a json
//
function fncFieldGet() {
   data = {};
   data.name         = elem_inputFieldCode.value        ;
   data.formula      = elem_inputFieldFormula.value     ;
   data.optimizeType = elem_inputFieldCalcType.value    ;
   data.calcValue    = elem_inputFormulaCalc.checked    ;
   data.replaceValue = elem_inputFormulaReplace.checked ;
   data.optimizeList = [] ;
   data.varList      = {} ;

   for ( iCount = 0; iCount < elem_inputFieldOptimzeSelected.length; iCount++ ) {
     data.optimizeList.push( elem_inputFieldOptimzeSelected.options[ iCount ].value );
   }
   
   for ( iCount = 0; iCount < elem_selectVariable.length; iCount++ ) {
     option = elem_selectVariable.options[ iCount ] ;
     
     data.varList[ option.value ] = option.varValue;
   }
   
   return data;
}

//
// Load data
//
async function asyncDownloadInputData(key) {
  try {
     fieldInputDisable( true );
     
     if (key == null || key == "" ) {
        fncFieldsUpdate( {} );
        return;
     }
     
     url = '?prog=formulaJsonData&key=' + key ;
     
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
// Save the data
//
async function asyncSaveInputData( options = "" ) {
  try {
     fieldInputDisable( true );
     
     url = '?prog=formulaJsonSave&options=' + options  ;
     
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
// Delete data
//
async function asyncDeleteInputData(key) {
  try {
     fieldInputDisable( true );
     
     url = '?prog=formulaJsonDelete&key=' + key ;
     
     config = {
        method: 'DELETE',
        headers: {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
        }
     }     
     response = await fetch( url, config );
     
     if (!response.ok) {
        alert( 'Error verwijderen data response: ' + response.status );
     } else {
        fieldDeleteFromSelect( key )
        // empty fields
        dataJson = {}; // await response.json();
        fncFieldsUpdate( dataJson );
     }
  } catch(err) {
    console.error(err);
    alert( 'Error verwijderen data ' + err );
  }
  finally {
    // finally enable the fields
    fieldInputDisable( false );
  }
}


//
// by value change of list keys, get the data and display it
//
function fncSelectMathFormulaChange() {
  asyncDownloadInputData( elem_selectMathFormula.value );
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

function fncButtonInputFieldAddCustomPress() {
  if ( elem_inputFieldOptimzeCustom.selectedIndex  < 0 ) {
     return
  }
  selectOption = elem_inputFieldOptimzeCustom.options[ elem_inputFieldOptimzeCustom.selectedIndex ] ;
 
   var option = document.createElement("option");
   option.text  = selectOption.text  ;
   option.value = selectOption.value ;
   option.title = selectOption.title ;
   
   elem_inputFieldOptimzeSelected.add( option );
   
   elem_inputFieldOptimzeSelected.selectedIndex = elem_inputFieldOptimzeSelected.length - 1 ;
}

function fncButtonInputFieldRemoveCustomPress () {
   
   if ( elem_inputFieldOptimzeSelected.selectedIndex < 0 ) {
      return;
   }
   var curIndex = elem_inputFieldOptimzeSelected.selectedIndex;
   elem_inputFieldOptimzeSelected.remove( curIndex ) ;
   
   if ( curIndex >= elem_inputFieldOptimzeSelected.length ) {
      curIndex = elem_inputFieldOptimzeSelected.length - 1 ;
   }
   if ( curIndex >= 0  ) {
      elem_inputFieldOptimzeSelected.selectedIndex = curIndex;
   }
}
function fncButtonInputFieldUpCustomPress() {
   if ( elem_inputFieldOptimzeSelected.selectedIndex < 1 ) {
      return;
   }
   var curIndex = elem_inputFieldOptimzeSelected.selectedIndex ;
   var OptUp    = elem_inputFieldOptimzeSelected[ curIndex - 1 ];
   var OptDown  = elem_inputFieldOptimzeSelected[ curIndex     ];
   
   var optSave = {};
   optSave.text  = OptUp.text  ;
   optSave.value = OptUp.value ;
   optSave.title = OptUp.title ;

   OptUp.text  = OptDown.text  ;
   OptUp.value = OptDown.value ;
   OptUp.title = OptDown.title ;

   OptDown.text  = optSave.text  ;
   OptDown.value = optSave.value ;
   OptDown.title = optSave.title ;
   
   elem_inputFieldOptimzeSelected.selectedIndex = curIndex - 1;
}

function fncButtonInputFieldDownCustomPress() {
   if ( elem_inputFieldOptimzeSelected.selectedIndex < 0 ) {
      return;
   }
   var curIndex = elem_inputFieldOptimzeSelected.selectedIndex ;
   if ( curIndex >= elem_inputFieldOptimzeSelected.length - 1 ) {
     return ;
   }
   var OptUp   = elem_inputFieldOptimzeSelected[ curIndex     ];
   var OptDown = elem_inputFieldOptimzeSelected[ curIndex + 1 ];
   
   var optSave = {};
   optSave.text  = OptUp.text  ;
   optSave.value = OptUp.value ;
   optSave.title = OptUp.title ;

   OptUp.text  = OptDown.text  ;
   OptUp.value = OptDown.value ;
   OptUp.title = OptDown.title ;

   OptDown.text  = optSave.text  ;
   OptDown.value = optSave.value ;
   OptDown.title = optSave.title ;
   
   elem_inputFieldOptimzeSelected.selectedIndex = curIndex + 1;
}

function fncButtonSelectVariableAddPress() {
   varName  = elem_inputFormulaVarName.value ;
   varValue = elem_inputFormulaVarValue.value; 
   
   varName  = varName.trim();
   varValue = varValue.trim();
   
   if (varName == '' ) {
      return;
   }
   if (varValue == '' ) {
      return;
   }
   
   var option    = null ;
   var addOption = false;
   for ( iCount = 0; iCount < elem_selectVariable.length; iCount++ ) {
     if (elem_selectVariable.options[ iCount ].value == varName ) {
        option = elem_selectVariable.options[ iCount ];
        break;
     }
   }
   if (option == null) {
     option    = document.createElement("option");
     addOption = true;
   }
   option.text     = varName + ' = ' + varValue ;
   option.value    = varName     ;
   option.title    = option.text ;
   option.varValue = varValue    ;

   if (addOption == true) {
     elem_selectVariable.add( option );
   }
}


// When the user clicks on the button, toggle between hiding and showing the drop down content
function fncOpenDropDownMenu( menuName ) {
  document.getElementById(menuName).classList.toggle("show");
}

// Close the drop down menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

function fncButtonSelectVariableRemovePress() {
   if (elem_selectVariable.selectedIndex < 0 ) {
      return
   }
   option = elem_selectVariable[ elem_selectVariable.selectedIndex ];
   
   elem_inputFormulaVarName.value  = option.value    ;
   elem_inputFormulaVarValue.value = option.varValue ;
   
   elem_selectVariable.remove( elem_selectVariable.selectedIndex ); 
}

function fncAddText( textToAdd ) {
   elem_inputFieldFormula.value += ' ' + textToAdd;
}
