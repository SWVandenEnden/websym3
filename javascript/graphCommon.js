/*
    script_common.js
    
    Copyright (C) 2018 S.W. van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
    
*/   

//
// Global class
// ............
// - commonGlobal   : Global variable class
//
//

//
// Global variable class
//
// - lineLength       : Length of a line given the 2 points
// - lineHook         : Hook between the 2 points in gred
// - lineHookSmallest : the smallest hook between 2 lines
// - lineEnd          : give point line end
//
// - lineAB              : y=ax+b, calc from 2 given points
// - linesCrossSection   : Calc cross section of 2 given lines
// - circlesCrossSection : Calc cross section of 2 given circles
//
// - roundNumber      : round number to 10 decimals
// - checkEqual       : check if numbers are equal
//
class commonGlobal {

  constructor( cName ) {
    this.oDrawField         = null  ; // div element
    this.cDrawField         = ''    ; // id drawfield
    
    this.drawDebug          = false ;
    
    this.iLineWidth         =   3   ; // width of line
    // this.iLineWidthResult   =   5   ; // width of line for the result of the problem
    this.iPointWidth        =   1   ; // width of 1 point = radius
    // this.dHookFilledRadius  =  40   ; // the lenght of the raidus of a filled hook
    // this.dAreaOpcacity      =   0.1 ; // opacity filled area
    // this.zIndexCircleFilled =  -1   ;
    // this.zIndexAreaFilled   = -10   ;
    
    this.iUniqueNumber    = 0    ; // unique number generator 
    
    this.iScreenWidth     = 1280 ; // size of the drawfield (this.oDrawField)
    this.iScreenHeight    =  720 ;
    this.cScreenBackColor = '#f8f8f8' ; // light gray
    this.iScreenX         = 0 ;  // absolute x position 
    this.iScreenY         = 0 ;  // absolute y position`

    this.iTextFontSize    =  24  ; 
    
    // - format graph field -> verplaatsen naar drawGraph
    // this.graphXStart = -10;
    // this.graphXEnd   =  10;
    // this.graphXStep  =   1;
    // this.graphYStart = -10;
    // this.graphYEnd   =  10;
    // this.graphYStep  =   1;
  
    // - the axes with info and grid
    // this.graphAxeColor       = "black";
    // this.graphAxeLineWidth   = 2 ;      // pixels
    // this.graphAxeZOrder      = 10;
    
    // this.graphNumberColor    = "darkgray"; // "black";
    // this.graphNumberFontSize = 16;      // pixels 
    // this.graphNumberZIndex   = 15;
    
    // this.graphGridColor      = "lightGray";
    // this.graphGridLineWidth  = 1;       // pixels
    // this.graphGridZIndex     = 5;

    // - the graph line
    // this.graphLineColor      = "red";
    // this.graphLineWidth      = 1 ;      // pixels
    // this.graphLineZIndex     = 20;
    
    if ( arguments.length >= 1 ) {
       this.setDrawField( cName );
    }
  }

  setDrawField( cName ) {
    this.cDrawField    = cName ;
    this.oDrawField    = document.getElementById( this.cDrawField );
    this.iScreenWidth  = this.oDrawField.clientWidth  ; // get the inner width & height
    this.iScreenHeight = this.oDrawField.clientHeight ;
    this.iScreenX      = 0 ;  // absolute x position 
    this.iScreenY      = 0 ;  // absolute y position`
    
    // var absPos = this.getAbsolutePosition( this.oDrawField );
    // this.iScreenX = absPos.left ;
    // this.iScreenY = absPos.top  ;
    
  }

  // https://stackoverflow.com/questions/1480133/how-can-i-get-an-objects-absolute-position-on-the-page-in-javascript
  getAbsolutePosition(element) {
    var top = 0, left = 0;
    do {
        top   += element.offsetTop  || 0;
        left  += element.offsetLeft || 0;
        element = element.offsetParent;
    } while(element);

    return {
        top: top,
        left: left
    };
  }

  // unique number generator
  getUniqueNumber() {
    return ( ++this.iUniqueNumber );
  }
  
  createSvg( cName ) {
     if ( ! cName ) {
       cName = 'svg' ;
     }
     return document.createElementNS('http://www.w3.org/2000/svg', cName );
  }
  
  createText( cText ) {
     return document.createTextNode( cText );
  }
 
 
  // calculations
  
  
  //
  // - lineLength  : Length of a line given the 2 points
  // - lineHook    : Hook between the 2 points in gred
  //
  lineLength( x1, y1, x2, y2 ) {
      var iLen = Math.sqrt( Math.pow( x2 - x1, 2 ) + Math.pow( y2 - y1, 2 ) ) ;
     
      iLen = this.roundNumber( iLen );
      
      return iLen ;
  }
  
  // Hook between the 2 points in gred
  //
  // range is from -180 to 180
  // -180 gred = horizontal, point 1 is right of point 2
  //  -90 gred = vertical, point 1 below point 2
  //    0 gred = horizontal, where point 1 is left of point 2
  //   90 gred = vertical, point 1 above point 2
  //  180 gred = same as -180
  //   
  lineHook( x1, y1, x2, y2 ) {
     var dHook = Math.atan2( y2 - y1, x2 - x1 );
     
     dHook *= 180 / Math.PI ;
     
     dHook = this.roundNumber( dHook );
     
     return dHook;
  }
  
  //
  // smallest hook 
  // x1,y1           = hook point
  // x2, y2 & x3 & y3 = legs
  lineHookSmallest( x1, y1, x2, y2, x3, y3 ) {
      var oResult = {} ;
      
      var oHookStart = glbTools.clsGlobal.lineHook( x1, y1,x2, y2 ) ;
      var oHookEnd   = glbTools.clsGlobal.lineHook( x1, y1,x3, y3 ) ;

      // swap hooks 
      if ( oHookStart > oHookEnd ) {
          var oHelp = oHookStart  ;
          
          oHookStart = oHookEnd   ;
          oHookEnd   = oHelp      ;
      }
      // oHookstart is now always < oHookEnd 
      if ( ( oHookEnd - oHookStart ) > 180  ) {
          oHookEnd -= 360 ;
      }
      
      oResult.oHookStart = oHookStart ;
      oResult.oHookEnd   = oHookEnd   ;
      
      return oResult ;
      
  }
  
  // give point line end
  lineEnd( x1, y1, iLen, dHook ) {
      var oResult = {} ;
      
      oResult.x1    = x1    ;
      oResult.y1    = y1    ;
      oResult.iLen  = iLen  ;
      oResult.dHook = dHook ;
      
      oResult.iXEnd = x1 + Math.cos( dHook * Math.PI / 180 ) * iLen ;
      oResult.iYEnd = y1 + Math.sin( dHook * Math.PI / 180 ) * iLen ;
      
      // calculcation errors, always 10 decimals
      oResult.iXEnd = Number( oResult.iXEnd.toFixed( 10 ));
      oResult.iYEnd = Number( oResult.iYEnd.toFixed( 10 ));
      
      return oResult ;
  }
  
  
  // calc a & b from y = ax + b
  //
  //
  // 2 points, x1, y1, x2, y2
  //
  // y = ax + b
  //
  // y1 = a x1 + b 
  // y2 = a x2 + b
  //
  // b       = y2 - a x2
  // y1      = a x1 + y2 - a x2
  // y1 - y2 = a x1 - a x2 
  //
  // a = ( y1 - y2 ) / ( x1 - x2 )
  // b = y2 - x2 ( ( y1 - y2 ) / ( x1 - x2 ) )
  //
  lineAB( x1, y1, x2, y2 ) {
     var oResult = {} ;

     oResult.a = ( y1 - y2 ) / (x1 - x2 );
     oResult.b = y2 - x2 * oResult.a ;

     return oResult ;
  }
  
  // cross section of 2 lines
  //
  // y  = a  x + b
  // y  = a2 x + b2
  // a x + b = a2 x + b2
  // a x - a2 x = b2 - b
  // x = ( b2 - b ) / ( a - a2 )
  // y = a x + b
  linesCrossSection( l1xStart, l1yStart, l1xEnd, l1yEnd
                   , l2xStart, l2yStart, l2xEnd, l2yEnd
                   ) {
      var oResult = {} ;
      
      oResult.AB1 = this.lineAB( l1xStart, l1yStart, l1xEnd, l1yEnd );
      oResult.AB2 = this.lineAB( l2xStart, l2yStart, l2xEnd, l2yEnd );
      
      oResult.xPos = ( oResult.AB2.b - oResult.AB1.b ) / ( oResult.AB1.a - oResult.AB2.a ) ;
      oResult.yPos = oResult.AB1.a * oResult.xPos + oResult.AB1.b ;
      
      oResult.xPos = this.roundNumber( oResult.xPos );
      oResult.yPos = this.roundNumber( oResult.yPos );
      
      return oResult ;
  }
      
  //    
  // cross section 2 ciclrs
  //
  // c1 = r1 & x1, y1
  // c2 = r2 & x2, y2

  // circle => r^2 = ( x - x1 )^2 + ( y - y2 )^2 
  // x1 = a, y1 = b
  // r^2 = (x-a)^2 + (y-b)^2
  // r^2 = x^2 -xa -xa + a^2 + y^2 - yb - yb + b^2
  // r^2 = x^2 - 2xa + a^2 + y^2 - 2yb + b^2
  // x^2 - 2xa + a^2 + y^2 - 2yb + b^2 - r^2 = 0

  // x1^2 - 2x1a1 + a1^2 + y1^2 - 2y1b1 + b1^2 - r1^2 = 0
  // x2^2 - 2x2a2 + a2^2 + y2^2 - 2y2b2 + b2^2 - r2^2 = 0
  //
  // now x1 = x2 & y1 = y2  ( cross section circles )
  //
  // -2x1a1 + 2x2a2 + a1^2 - a2^2 - 2y1b1 + 2y2b2 + b1^2 - b2^2 - r1^2 + r2^2 = 0 
  // -2xa1  + 2xa2  + a1^2 - a2^2 - 2yb1  + 2yb2  + b1^2 - b2^2 - r1^2 + r2^2 = 0
  //
  // x( 2a2 - 2a1 ) = - a1^2 + a2^2 + 2yb1 - 2yb2 - b1^2 + b2^2 + r1^2 - r2^2
  // x = ( - a1^2 + a2^2 + 2yb1 - 2yb2 - b1^2 + b2^2 + r1^2 - r2^2 ) / ( 2a2 - 2a1 )
  // x = ( - a1^2 + a2^2 - b1^2 + b2^2 + r1^2 - r2^2 + 2yb1 - 2yb2 ) / ( 2a2 - 2a1 )
  //
  // q = - a1^2 + a2^2 - b1^2 + b2^2 + r1^2 - r2^2 
  // p = 2a2 - 2a1
  //
  // x = ( q + 2yb1 - 2yb2 ) / p
  // s = 2b1 - 2b2
  //
  // x = ( q + y * s ) / p = q/p + ys/p
  //
  // substitute 1e circle
  //
  // ( x - a1 )^2 + (y- b1)^2 - r1^2 = 0
  // ( q/p + ys/p - a1 ) ^ 2 + ( y1 - b1 ) ^2 - r1^2 = 0
  // t = q/p - a1
  //
  // ( ys/p + t ) ^ 2 + ( y1 - b1 ) ^2 - r1^2 = 0
  // y^2 * s^2 / p^2 + 2 s y t / p + t^2 + y1^2 - 2b1y + b^2 - r1^2 = 0
  // 
  // k = s^2 / p^2 + 1
  // l = + 2 s t / p - 2b1 
  // m = + t^2 + b^2 - r1^2
  //
  // y = ( -l + sqrt( l^2 - 4km )  ) / 2k
  // y = ( -l - sqrt( l^2 - 4km )  ) / 2k
  //
  circlesCrossSection( r1, x1, y1, r2, x2, y2 ) {
      var oResult = {} ;
      
      oResult.r1 = r1 ;
      oResult.x1 = x1 ;
      oResult.y1 = y1 ;
      oResult.r2 = r2 ;
      oResult.x2 = x2 ;
      oResult.y2 = y2 ;
      

      // var r1 = r1 ;
      var a1 = x1 ;
      var b1 = y1 ;
        
      // var r2 = r2 ;
      var a2 = x2 ;
      var b2 = y2 ;
        
// console.log( 'r1: ', r1 ) ;        
// console.log( 'a1: ', a1 ) ;
// console.log( 'b1: ', b1 ) ;

// console.log( 'r2: ', r2 ) ;        
// console.log( 'a2: ', a2 ) ;
// console.log( 'b2: ', b2 ) ;

      var q = - a1 * a1 + a2 * a2 - b1 * b1 + b2 * b2 + r1 * r1 - r2 * r2 ; // - a1^2 + a2^2 - b1^2 + b2^2 + r1^2 - r2^2
      var p = 2 * a2 - 2 * a1                                 ; // 2a2 - 2a1 
        
      var s = 2 * b1 - 2 * b2 ; // 2b1 - 2b2
        
// console.log( 'q:', q ) ;        
// console.log( 'p:', p ) ;
// console.log( 's:', s ) ;

      // t = q/p - a1
      var t = q / p - a1 ; // t = q/p - a1

// console.log( 't:', t );
        
      var k = s * s / ( p * p ) + 1     ;  // s^2 / p^2 + 1
      var l = 2 * s * t / p - 2 * b1    ;  // + 2 s t / p - 2b1 
      var m = t * t + b1 * b1 - r1 * r1 ;  // + t^2 + b^2 - r1^2

// console.log( 'k:', k ) ;        
// console.log( 'l:', l ) ;
// console.log( 'm:', m ) ;
        
      var z = l * l - 4 * k * m ; //  l^2 - 4km 

// console.log( 'z:', z ) ;
        
      var rY1 = ( -1 * l + Math.sqrt( z ) ) / ( 2 * k );
      var rY2 = ( -1 * l - Math.sqrt( z ) ) / ( 2 * k );
       
      var rX1 = ( q + rY1 * s ) / p ; // ( q + y * s ) / p
      var rX2 = ( q + rY2 * s ) / p ; // ( q + y * s ) / p
        
// console.log( 'r x1, y1 :', rX1, rY1 ) ;
// console.log( 'r x2, y2 :', rX2, rY2 ) ;
        

      oResult.rX1 = this.roundNumber( rX1 );
      oResult.rY1 = this.roundNumber( rY1 );
      oResult.rX2 = this.roundNumber( rX2 );
      oResult.rY2 = this.roundNumber( rY2 );
      
      return oResult ;
  }

  //
  // cross section circle & line
  //
  // (x-x1)^2 + (y-y1)^2 = r1^2
  // y = ax + b
  //
  // substitute
  //
  // (x-x1)^2 + ( ax+b-y1)^2 = r1^2
  // t = b-y1
  //
  // (x-x1)^2 + ( ax+t)^2 = r1^2
  // x^2 - 2x * x1 + x1^2 + a^2 * x^2 + 2atx + t^2 - r^2 = 0
  //
  // k = 1 + a^2 
  // l = -2 * x1 + 2at
  // m = x1^2 + t^2 - r^2
  //
  // x = ( -l + sqrt( l^2 - 4km )  ) / 2k
  // x = ( -l - sqrt( l^2 - 4km )  ) / 2k
  
  circleLineCrossSection( r1, x1, y1, x2, y2, x3, y3 ) {
      var oResult = {} ;
      
      oResult.r1 = r1 ;
      oResult.x1 = x1 ;
      oResult.y1 = y1 ;
      oResult.x2 = x2 ;
      oResult.y2 = y2 ;
      oResult.x3 = x3 ;
      oResult.y3 = y3 ;
      
      var lSwap = false ;
      if ( oResult.x2 == oResult.x3 ) {
          lSwap = true ;
          oResult.x2 = y2 ;
          oResult.y2 = x2 ;

          oResult.x3 = y3 ;
          oResult.y3 = x3 ;
      }
      
      var oLineAB = this.lineAB( oResult.x2, oResult.y2, oResult.x3, oResult.y3 );
      oResult.a = oLineAB.a ;
      oResult.b = oLineAB.b ;
      
      var t = oResult.b - oResult.y1 ; //  b-y1
      
// console.log( 't :', t );

      var k = 1 + oResult.a * oResult.a ; //   1 + a^2 
      var l = -2 * oResult.x1 + 2 * oResult.a * t; //  -2 * x1 + 2at
      var m = oResult.x1 * oResult.x1 + t * t - oResult.r1 * oResult.r1 ; //   x1^2 + t^2 - r^2

// console.log( 'k :', k );
// console.log( 'l :', l );
// console.log( 'm :', m );
      
      var z = l * l - 4 * k * m ; //  l^2 - 4km 

// console.log( 'z :', z );
      
      var rX1 = ( -1 * l + Math.sqrt( z ) ) / ( 2 * k );
      var rX2 = ( -1 * l - Math.sqrt( z ) ) / ( 2 * k );
      
      var rY1 = oResult.a * rX1 + oResult.b ;
      var rY2 = oResult.a * rX2 + oResult.b ;

      if ( lSwap == true ) {
        oResult.rX1 = this.roundNumber( rY1 );
        oResult.rY1 = this.roundNumber( rX1 );
        oResult.rX2 = this.roundNumber( rY2 );
        oResult.rY2 = this.roundNumber( rX2 );
      } else {
        oResult.rX1 = this.roundNumber( rX1 );
        oResult.rY1 = this.roundNumber( rY1 );
        oResult.rX2 = this.roundNumber( rX2 );
        oResult.rY2 = this.roundNumber( rY2 );
      }
      
// console.log( 'circleLineCrossSection:',  oResult );
      return oResult ;
  }
  
  // round number 
  roundNumber( dNumber ) {
      return Number( dNumber.toFixed( 10 ))
  }
  
  // check numbers equal, calc with 10 decimals, check with 8 decimals
  checkEqual( dNum1, dNum2 ) {
      var d1      = Number( dNum1.toFixed( 8 ));
      var d2      = Number( dNum2.toFixed( 8 ));
      var lResult = false ;
      
      if ( d1 == d2 ) {
          lResult = true ;
      } 
      return lResult ;
  }
  
}
