/*
    graphDraw.js

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
// Draw classes
// ............
// - drawBase         : base class for all drawings
// - drawPoint        : draw point
// - drawLine         : draw line
// - drawCircle       : draw circle
// - drawArea         : draw area
// - drawText         : draw textdrawGraph
//
// - drawGraph
//

//
// base class for all drawings
//
class drawBase {
   constructor( oGlobal ) {
     this.clsGlobal  = oGlobal ; // = class commonGlobal()
     this.oElement   = null    ;
     this.cColor     = ''      ;

   }

   hide() {
      this.oElement.style.display = 'none' ;
   }
   show() {
      this.oElement.style.display = '' ;
   }

   setColor( cColor ) {
      this.oElement.style.color = cColor ;
   }
   getColor() {
      return this.cColor ;
   }

   setOpacity( dOpacity ) {
      this.oElement.style.opacity = dOpacity ;
   }
   getOpacity() {
      return this.oElement.style.opacity ;
   }

   setZIndex( iZIndex ) {
      this.oElement.style.zIndex = iZIndex ;
   }

   removeObject( oObject ) {
      if ( oObject && oObject.parentNode ) {
         oObject.parentNode.removeChild( oObject );
      }
      return null ;
   }


   deleteElement() {
      this.oElement = this.removeObject( this.oElement );
      // if ( this.oElement && this.oElement.parentNode ) {
      //   this.oElement.parentNode.removeChild( this.oElement );
      // }
      this.oElement = null ;
   }

   // destructor is never called so an special function to destroy the class
   destroyClass() {
      this.deleteElement();
   }

   destructor() {
      this.destroyClass();
   }

}

//
// draw point class
//
class drawPoint extends drawBase {

   constructor( oGlobal, xPos, yPos, cColor ) {

     super( oGlobal );

     this.iXpos      = 0    ;
     this.iYpos      = 0    ;
     this.cColor     = ''   ;
     this.oCircle    = null ;

     if ( arguments.length >= 4 ) {
        this.createPoint( xPos, yPos, cColor );
     }
   }

   createPoint( xPos, yPos, cColor ) {
      // this.deletePoint();
      this.deleteElement();

      this.oElement = this.clsGlobal.createSvg() ;

      this.oElement.style.position = 'absolute' ;

      this.oElement.style.width  = ( this.clsGlobal.iPointWidth * 2 ) + 'px'  ;
      this.oElement.style.height = ( this.clsGlobal.iPointWidth * 2 ) + 'px' ;

      this.oCircle = this.clsGlobal.createSvg( 'circle' ) ;
      this.oCircle.setAttribute( 'cx'          , this.clsGlobal.iPointWidth  );
      this.oCircle.setAttribute( 'cy'          , this.clsGlobal.iPointWidth  );
      this.oCircle.setAttribute( 'r'           , this.clsGlobal.iPointWidth  );
      this.oCircle.setAttribute( 'stroke-width', '0'     );
      this.oCircle.setAttribute( 'fill'        , cColor );

      this.oElement.appendChild( this.oCircle );

      this.cColor = cColor ;

      this.setPosition( xPos, yPos );

      this.clsGlobal.oDrawField.appendChild( this.oElement );
   }

   setColor( cColor ) {
      this.cColor = cColor ;
      this.oCircle.setAttribute( 'fill', cColor );
   }

   // set position point, x,y = center point
   setPosition( xPos, yPos ) {
     if ( xPos != null ) { this.iXpos = xPos; }
     if ( yPos != null ) { this.iYpos = yPos; }

     this.oElement.style.left = this.iXpos - this.clsGlobal.iPointWidth + 'px' ;
     this.oElement.style.top  = this.iYpos - this.clsGlobal.iPointWidth + 'px' ;
   }

   // delete
   deleteElement() {
      if ( this.oCircle && this.oCircle.parentNode ) {
         this.oCircle.parentNode.removeChild( this.oCircle );
      }
      this.oCircle = null ;

      super.deleteElement();
   }
}

//
// draw line class
//
class drawLine extends drawBase {
   constructor( oGlobal, iX1, iY1, iX2, iY2, cColor ) {

     super( oGlobal );

     this.iXTop   = 0 ; // left top position of element
     this.iYTop   = 0 ;

     this.iWidth  = 0 ;
     this.iHeight = 0 ;

     this.iX1     = 0 ; // start point line
     this.iY1     = 0 ;
     this.iX2     = 0 ; // end point line
     this.iY2     = 0 ;

     this.cColor  = '';

     this.lDashed = false ;

     this.oLine = null ;

     if ( arguments.length >= 6 ) {
        this.createLine( iX1, iY1, iX2, iY2, cColor );
     }
   }

   createLine( iX1, iY1, iX2, iY2, cColor ) {
      this.deleteElement();

      this.oElement = this.clsGlobal.createSvg() ;

      this.oElement.style.position = 'absolute' ;

      this.oLine = this.clsGlobal.createSvg( 'line' ) ;
      this.oLine.setAttribute( 'stroke-width'  , this.clsGlobal.iLineWidth );
      this.oLine.setAttribute( 'stroke'        , cColor  );
      this.oLine.setAttribute( 'stroke-linecap', 'round' );
// stippellijn
//      this.oLine.setAttribute( 'stroke-dasharray', '5, 5' );

      this.oElement.appendChild( this.oLine );

      this.setPosition( iX1, iY1, iX2, iY2 );

      this.cColor = cColor ;

      this.clsGlobal.oDrawField.appendChild( this.oElement );
   }

   setDashed( lDash ) {
      if ( lDash ) {
          if ( ! this.lDashed ) {
              this.lDashed = true ;
              this.oLine.setAttribute( 'stroke-dasharray', '5, 5' );
          }
      } else {
          if ( this.lDashed ) {
              this.lDashed = false ;
              this.oLine.removeAttribute( 'stroke-dasharray' );
          }
      }
   }

   setStrokeWidth( iWidth ) {
      this.oLine.setAttribute( 'stroke-width', iWidth );
   }

   setPosition( iX1, iY1, iX2, iY2 ) {
      if ( iX1 != null ) this.iX1 = iX1 ;
      if ( iY1 != null ) this.iY1 = iY1 ;
      if ( iX2 != null ) this.iX2 = iX2 ;
      if ( iY2 != null ) this.iY2 = iY2 ;

      this.iXTop  = Math.min( this.iX1, this.iX2 );
      this.iYTop  = Math.min( this.iY1, this.iY2 );

      this.iXTop -= this.clsGlobal.iLineWidth ;
      this.iYTop -= this.clsGlobal.iLineWidth ;

      this.iWidth  = Math.abs( this.iX1 - this.iX2 ) + this.clsGlobal.iLineWidth * 2 ;
      this.iHeight = Math.abs( this.iY1 - this.iY2 ) + this.clsGlobal.iLineWidth * 2 ;

      this.oElement.style.width  = this.iWidth  + 'px' ;
      this.oElement.style.height = this.iHeight + 'px' ;

      this.oElement.style.left   = this.iXTop   + 'px' ;
      this.oElement.style.top    = this.iYTop   + 'px' ;

      this.oLine.setAttribute( 'x1' , this.iX1 - this.iXTop );
      this.oLine.setAttribute( 'y1' , this.iY1 - this.iYTop );
      this.oLine.setAttribute( 'x2' , this.iX2 - this.iXTop );
      this.oLine.setAttribute( 'y2' , this.iY2 - this.iYTop );
   }

   setColor( cColor ) {
      this.cColor = cColor ;

      this.oLine.setAttribute( 'stroke', cColor );
   }

   // delete
   deleteElement() {
      if ( this.oLine && this.oLine.parentNode ) {
         this.oLine.parentNode.removeChild( this.oLine );
      }
      this.oLine = null ;

      super.deleteElement();
   }
}

//
// svg circle
//
// draw a circle
// iXpos, iYpos = center
// dRadius      = radius circle
// dAngleStart  = start angle, 0 = top circle, it may a negative start angle
// dAngleEnd    = end angle, always positive
//
// iXpos        = class drawLine, then the line will be used
//
class drawCircle extends drawBase {
   constructor( oGlobal, iXpos, iYpos, dRadius, cColor, dAngleStart, dAngleEnd, lFill = false ) {

     super( oGlobal );

     this.iXTop       =   0 ; // left top position of element
     this.iYTop       =   0 ;

     this.iWidth      =   0 ;
     this.iHeight     =   0 ;

     this.iXPos       =   0 ; // center circle
     this.iYPos       =   0 ;
     this.dRadius     =   0 ; // radius circle
     this.dAngleStart =   0 ; // start angel in degrees
     this.dAngleEnd   = 360 ; // end angel in degrees

     this.cColor      =  '' ;

     this.lFill       = lFill ;

     this.oArc        = null;

     // line object given...
     if ( iXpos instanceof drawLine ) {
         var oLine  = iXpos ;

         iXpos       = oLine.iX1 ;
         iYpos       = oLine.iY1 ;
         dRadius     = oGlobal.lineLength( oLine.iX1, oLine.iY1, oLine.iX2, oLine.iY2 );
         cColor      = oLine.getColor();
         dAngleStart = oGlobal.lineHook( oLine.iX1, oLine.iY1, oLine.iX2, oLine.iY2 ) + 90;
         dAngleEnd   = dAngleStart + 359.9 ;

         this.createArc( iXpos, iYpos, dRadius, cColor, dAngleStart, dAngleEnd );

     } else if ( arguments.length >= 5 ) {
         this.createArc( iXpos, iYpos, dRadius, cColor, dAngleStart, dAngleEnd );
     }
   }

   createArc( iXpos, iYpos, dRadius, cColor, dAngleStart, dAngleEnd ) {
      this.deleteElement();


      this.oElement = this.clsGlobal.createSvg() ;

      this.oElement.style.position = 'absolute' ;

      this.oArc = this.clsGlobal.createSvg( 'path' ) ;
      this.oArc.setAttribute( 'stroke-width'  , this.clsGlobal.iLineWidth );
      this.oArc.setAttribute( 'stroke'        , cColor  );
      this.oArc.setAttribute( 'stroke-linecap', 'round' );

      this.oElement.appendChild( this.oArc );

      this.cColor = cColor ;
      this.setFill( this.lFill );

      this.setPosition( iXpos, iYpos, dRadius, dAngleStart, dAngleEnd );

      this.clsGlobal.oDrawField.appendChild( this.oElement );
   }

   // https://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
   polarToCartesian( centerX, centerY, radius, angleInDegrees ) {
      var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;

      return {
          x: centerX + (radius * Math.cos(angleInRadians)),
          y: centerY + (radius * Math.sin(angleInRadians))
      };
   }

   describeArc( x, y, radius, startAngle, endAngle ){
      var start = this.polarToCartesian(x, y, radius, endAngle  );
      var end   = this.polarToCartesian(x, y, radius, startAngle);

      var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

      if ( this.lFill != true ) {
        var d = [
            "M", start.x, start.y,
            "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
        ].join(" ");
      }
      else {
        var d = [
            "M" , start.x, start.y,
            "A" , radius, radius, 0, largeArcFlag, 0, end.x, end.y,
            "L" , x, y,
            "L" , start.x, start.y,
            " Z"
        ].join(" ");
      }
      return d;
   }

   setPosition( iXpos, iYpos, dRadius, dAngleStart, dAngleEnd ) {
      if ( iXpos       != null ) { this.iXPos       = iXpos       ; }
      if ( iYpos       != null ) { this.iYPos       = iYpos       ; }
      if ( dRadius     != null ) { this.dRadius     = dRadius     ; }
      if ( dAngleStart != null ) { this.dAngleStart = dAngleStart ; }
      if ( dAngleEnd   != null ) { this.dAngleEnd   = dAngleEnd   ; }

      // full circle = 0 -> 360, but 360 will be translated too 0
      if ( this.dAngleEnd   == 360 ) { this.dAngleEnd   = 359.9; }
      if ( this.dAngleStart == 360 ) { this.dAngleStart = 359.9; }

      this.iXTop  = this.iXPos - this.dRadius - this.clsGlobal.iLineWidth ;
      this.iYTop  = this.iYPos - this.dRadius - this.clsGlobal.iLineWidth ;

      this.iWidth  = this.dRadius * 2 + this.clsGlobal.iLineWidth * 2 ;
      this.iHeight = this.dRadius * 2 + this.clsGlobal.iLineWidth * 2 ;

      this.oElement.style.width  = this.iWidth  + 'px' ;
      this.oElement.style.height = this.iHeight + 'px' ;

      this.oElement.style.left   = this.iXTop   + 'px' ;
      this.oElement.style.top    = this.iYTop   + 'px' ;

      var cPath = '';

      if ( this.dAngleStart > this.dAngleEnd ) {
         cPath = this.describeArc( this.iXPos - this.iXTop, this.iYPos - this.iYTop, this.dRadius, this.dAngleEnd, this.dAngleStart );
      } else {
         cPath = this.describeArc( this.iXPos - this.iXTop, this.iYPos - this.iYTop, this.dRadius, this.dAngleStart, this.dAngleEnd );
      }
      this.oArc.setAttribute( 'd', cPath );
   }

   setColor( cColor ) {
      this.cColor = cColor ;
      this.oArc.setAttribute( 'stroke', cColor );
      if ( this.lFill == true ) {
         this.oArc.setAttribute( 'fill', cColor  );
      }
   }

   setFill ( lFill ) {
      this.lFill = lFill ;
      if ( this.lFill == true ) {
          this.oArc.setAttribute( 'stroke-width'  , 0 );

          // no stroke width for filled hooks
          this.oArc.setAttribute( 'fill', this.cColor  );

          // hook always below lines & circles
          this.setZIndex( this.clsGlobal.zIndexCircleFilled )
      } else {
          this.oArc.setAttribute( 'stroke-width'  , this.clsGlobal.iLineWidth );
          this.oArc.setAttribute( 'fill', 'none'       );
      }
   }

   // delete
   deleteElement() {
      if ( this.oArc && this.oArc.parentNode ) {
         this.oArc.parentNode.removeChild( this.oArc );
      }
      this.oArc = null ;

      super.deleteElement();
   }
}

//
// draw a area (path)
// arrCorr = absolute coordinates  [ {xpos:1, ypos:2},.. ]
//
class drawArea extends drawBase {
   constructor( oGlobal, arrCorr, cColor, lFill = true ) {

     super( oGlobal );

     this.iXTop       =   0 ; // left top position of element
     this.iYTop       =   0 ;

     this.iXBottom    =   0 ; // right bottom position of element
     this.iYBottom    =   0 ;

     this.iWidth      =   0 ;
     this.iHeight     =   0 ;

     this.lFill       = false;

     this.oArea         = null ;
     this.StrokeWidth   = 0 ; // this.clsGlobal.iLineWidth    ;
     this.OpacityArea   = this.clsGlobal.dAreaOpcacity ;
//     this.OpacityStroke = 0                            ; // no lines but reserve the space

     if ( arguments.length >= 3 ) {
         this.createArea( arrCorr, cColor, lFill );
     }
   }

   createArea( arrCorr, cColor, lFill ) {
      this.deleteElement();


      this.oElement = this.clsGlobal.createSvg() ;

      this.oElement.style.position = 'absolute' ;

      this.oArea = this.clsGlobal.createSvg( 'path' ) ;
      this.oArea.setAttribute( 'stroke-width'  , this.StrokeWidth );
      this.oArea.setAttribute( 'stroke'        , cColor  );
//      this.oArea.setAttribute( 'stroke-linecap', 'round' );

      this.oElement.appendChild( this.oArea );

      this.lFill  = lFill ;
      // this.setColor( cColor );
      this.cColor = cColor ;

      this.setCoordinates( arrCorr );

      this.clsGlobal.oDrawField.appendChild( this.oElement );
   }

   setColor( cColor ) {
      this.cColor = cColor ;
      this.oArea.setAttribute( 'stroke'        , cColor             );
//      this.oArea.setAttribute( 'stroke-opacity', this.OpacityStroke );

      if ( this.lFill == true ) {
         this.oArea.setAttribute( 'fill', cColor                    );
         this.oArea.setAttribute( 'fill-opacity', this.OpacityArea  );

         this.setZIndex( this.clsGlobal.zIndexAreaFilled )

      } else {
         this.oArea.removeAttribute( 'fill' );
         this.oArea.setAttribute( 'fill-opacity', 0  );
      }
   }

   setFilled( lFilled ) {
       this.lFill = lFilled ;
       this.setColor( this.cColor );
   }

   setCoordinates( arrCorr ) {
      // min xpos, ypos, max xpos, ypos nodig
      var iPos  ;
      var oElem ;

      this.iXTop    = arrCorr[0].xPos ;
      this.iYTop    = arrCorr[0].yPos ;
      this.iXBottom = arrCorr[0].xPos ;
      this.iYBottom = arrCorr[0].yPos ;

      for ( iPos = 1; iPos < arrCorr.length; iPos++ ){
         oElem = arrCorr[ iPos ] ;
         if ( oElem.xPos < this.iXTop    ) { this.iXTop    = oElem.xPos ; }
         if ( oElem.yPos < this.iYTop    ) { this.iYTop    = oElem.yPos ; }
         if ( oElem.xPos > this.iXBottom ) { this.iXBottom = oElem.xPos ; }
         if ( oElem.yPos > this.iYBottom ) { this.iYBottom = oElem.yPos ; }
      }
      // safety for line width
      this.iXTop    -= this.clsGlobal.iLineWidth * 2 ;
      this.iYTop    -= this.clsGlobal.iLineWidth * 2 ;
      this.iXBottom += this.clsGlobal.iLineWidth * 2 ;
      this.iYBottom += this.clsGlobal.iLineWidth * 2 ;

      this.iWidth      = this.iXBottom - this.iXTop ;
      this.iHeight     = this.iYBottom - this.iYTop ;

      // set element position
      this.oElement.style.width  = this.iWidth  + 'px' ;
      this.oElement.style.height = this.iHeight + 'px' ;

      this.oElement.style.left   = this.iXTop   + 'px' ;
      this.oElement.style.top    = this.iYTop   + 'px' ;

      // determine path
      var cPath ;
      cPath = 'M' + ( arrCorr[0].xPos - this.iXTop ) + ' ' + ( arrCorr[0].yPos - this.iYTop ) ;
      for ( iPos = 1; iPos < arrCorr.length; iPos++ ){
         oElem = arrCorr[ iPos ] ;
         cPath += ' L' + ( oElem.xPos - this.iXTop ) + ' ' + ( oElem.yPos - this.iYTop ) ;
      }
      // area = always closed if it is filled
      if ( this.lFill == true ) {
         cPath += ' Z' ;
      }
      this.oArea.setAttribute( 'd', cPath );

      this.setColor( this.cColor );
   }


   setStrokeWidth( dStrokeWidth ) {
       this.StrokeWidth = dStrokeWidth ;
       this.oArea.setAttribute( 'stroke-width'  , this.StrokeWidth );
       this.setColor( this.cColor );
   }

   // delete
   deleteElement() {
      if ( this.oArea && this.oArea.parentNode ) {
         this.oArc.parentNode.removeChild( this.oArea );
      }
      this.oArea = null ;

      super.deleteElement();
   }

}

//
// draw text class, arrText = array, format [  { text: "Text", style:"fill:blue" }, .. ]
// x,y = left bottom text
//
class drawText extends drawBase {

   constructor( oGlobal, xPos, yPos, arrText ) {

     super( oGlobal );

     this.iXpos      = 0         ;
     this.iYpos      = 0         ;
     this.oText      = null      ;
     this.arrText    = []        ;
     this.iFontSize  = 0         ;

     if ( arguments.length >= 4 ) {
        this.createText( xPos, yPos, arrText );
     }
   }

   createText( xPos, yPos, arrText ) {
      // this.deletePoint();
      this.deleteElement();

      this.oElement = this.clsGlobal.createSvg() ;

      this.oElement.style.position = 'absolute' ;

      this.iFontSize = this.clsGlobal.iTextFontSize ;

      // do not site width & height,
      this.oElement.style.width  =  '600px'  ;
      // this.oElement.style.height =  'px' ;

      // <svg id="idtext" style="position:absolute;top:500px;left:500px;font-size:20px">
      // <text x="0" y="20"">
      //   <tspan>Testing</tspan>
      //   <tspan style="fill:red;font-weight: bold">Testing</tspan>
      // </text>
      // </svg>
      this.oText = this.clsGlobal.createSvg( 'text' ) ;
      this.oText.setAttribute( 'x', 0  );
      this.oText.setAttribute( 'y', this.iFontSize);
      this.oText.style.fontSize = this.iFontSize + 'px' ;

      this.oElement.appendChild( this.oText );

      for ( var iCnt in arrText ) {
         var oTextSpan = this.clsGlobal.createSvg( 'tspan' ) ;
         var oTextMess = this.clsGlobal.createText( arrText[ iCnt ].text );

         oTextSpan.style = arrText[ iCnt ].style ;
         oTextSpan.appendChild( oTextMess );

         this.oText.appendChild( oTextSpan );

         this.arrText.push( oTextSpan );
      }


      this.setPosition( xPos, yPos );

      this.clsGlobal.oDrawField.appendChild( this.oElement );

      // set dynamic the text width
      this.oElement.style.width  =  this.getSize().width + 'px'  ;
   }

   // get the size object of the text
   getSize() {
      var oSize ;
      if ( this.oElement.style.display == 'none' ) {
          this.show();
          oSize = this.oText.getBBox();
          this.hide();
      } else {
          oSize = this.oText.getBBox();
      }
      return oSize ;
   }

   setColor( cColor ) {
      for ( var iCnt in this.arrText ) {
        this.arrText[ iCnt ].style.setAttribute( 'fill', cColor );
      }
   }

   setFontSize( iFontSize ) {
      if ( iFontSize != null ) { this.iFontSize = iFontSize; }

      this.oText.style.fontSize = this.iFontSize + 'px' ;
      this.oText.setAttribute( 'y', this.iFontSize);

      this.setPosition( null, null );

      this.oElement.style.width  =  this.getSize().width + 'px'  ;
   }

   setFont( cFont ) {
       this.oElement.style.fontFamily = cFont;
       this.setFontSize( null );
   }

   // set position point, x,y = center point
   setPosition( xPos, yPos ) {
     if ( xPos != null ) { this.iXpos = xPos; }
     if ( yPos != null ) { this.iYpos = yPos; }

     this.oElement.style.left = this.iXpos + 'px' ;
     this.oElement.style.top  = ( this.iYpos - this.iFontSize ) + 'px' ;
   }

   setWidth( dWidth ) {
      this.oElement.style.width =  dWidth + 'px'  ;
   }

   center( xStart, xEnd ) {
     var iLen   = xEnd - xStart ;
     var iWidth = this.getSize().width ;

     if ( iWidth < iLen ) {
        this.setPosition( xStart + ( iLen - iWidth ) / 2 );
     } else {
        this.setPosition( xStart );
     }
   }

   // delete
   deleteElement() {
      for ( var iCnt in this.arrText ) {
        this.removeObject( this.arrText[ iCnt ] );
      }
      this.arrText = [] ;

      this.oText = this.removeObject( this.oText ) ;

      super.deleteElement();
   }
}


class drawGraph extends drawBase {

   constructor( oGlobal ) {

     super( oGlobal );

     this.oLineHor    = null ;
     this.oLineVer    = null ;
     this.oLinesHor   = [];
     this.oLinesVer   = [];
     this.oNumHor     = [];
     this.oNumVer     = [];

     this.graphXStart = -10;
     this.graphXEnd   =  10;
     this.graphXStep  =   1;
     this.graphYStart = -10;
     this.graphYEnd   =  10;
     this.graphYStep  =   1;

     // - the axes with info and grid
     this.graphAxeColor       = "black";
     this.graphAxeLineWidth   = 2 ;      // pixels
     this.graphAxeZIndex      = 10;
     this.graphAxeShow        = true;

     this.graphNumberColor    = "darkgray"; // "black";
     this.graphNumberFontSize = 16;      // pixels
     this.graphNumberZIndex   = 15;
     this.graphNumberShow     = true;

     this.graphGridColor      = "lightGray";
     this.graphGridLineWidth  = 1;       // pixels
     this.graphGridZIndex     = 5;
     this.graphGridShow       = true;

   }

   //
   // setters for the variables
   //
   setX( xStart = null, xEnd = null, xStep = null ) {
     if (xStart != null) {
       this.graphXStart = xStart;
     }
     if (xEnd != null) {
       this.graphXEnd = xEnd;
     }
     if (xStep != null) {
       this.graphXStep = xStep;
     }
   }
   setY( yStart = null, yEnd = null, yStep = null ) {
     if (yStart != null) {
       this.graphYStart = yStart;
     }
     if (yEnd != null) {
       this.graphYEnd = yEnd;
     }
     if (yStep != null) {
       this.graphYStep = yStep;
     }
   }

   setAxe( cColor = null, iLineWidth = null, izIndex = null, bShow = null ) {
     if (cColor != null) {
       this.graphAxeColor = cColor;
     }
     if ( iLineWidth != null ) {
       this.graphAxeLineWidth = iLineWidth;
     }
     if (izIndex != null) {
       this.graphAxeZIndex = iZIndex;
     }
     if (bShow != null ) {
       this.graphAxeShow = bShow;
     }
   }

   setNumber( cColor = null, iFontSize = null, izIndex = null, bShow = null ) {
     if (cColor != null) {
       this.graphNumberColor = cColor;
     }
     if ( iFontSize != null ) {
       this.graphNumberFontSize = iFontSize;
     }
     if ( izIndex != null ) {
       this.graphNumberZIndex.izIndex;
     }
     if (bShow != null ) {
       this.graphNumberShow = bShow;
     }
   }

   setGrid( cColor = null, iLineWidth = null, izIndex = null, bShow = null ) {
     if (cColor != null) {
       this.graphGridColor = cColor;
     }
     if ( iLineWidth != null ) {
       this.graphGridLineWidth = iLineWidth;
     }
     if (izIndex != null) {
       this.graphGridZIndex = iZIndex;
     }
     if (bShow != null ) {
       this.graphGridShow = bShow;
     }
   }


   //
   // Convert function x-value into a graph x-value
   //
   funcXtoGraphX( xFunc ) {
     // func  = this.graphXStart -> this.graphXEnd
     // graph = 0                -> this.iScreenWidth
     var dPart  = 0;
     var xGraph = 0;

     dPart   = (xFunc - this.graphXStart ) / ( this.graphXEnd - this.graphXStart );
     xGraph  =  Math.min( this.clsGlobal.iScreenWidth, ( (this.graphXEnd - this.graphXStart) / (this.graphYEnd - this.graphYStart)) * this.clsGlobal.iScreenHeight ) * dPart ;
     xGraph += this.clsGlobal.iScreenX ; // for drawing this module use absolute

     return xGraph;
   }

   //
   // Convert function y-value into a graph y-value
   //
   funcYtoGraphY( yFunc ) {
     // func  = this.graphYStart -> this.graphYEnd     ( bottom to up    )
     // graph = 0                -> this.iScreenHeight ( up     to bottom)

     var dPart  = 0;
     var yGraph = 0;

     dPart   = (yFunc - this.graphYStart ) / ( this.graphYEnd - this.graphYStart );
     dPart   = 1.0 - dPart;
     yGraph  =  Math.min( ( (this.graphYEnd - this.graphYStart) / (this.graphXEnd - this.graphXStart)) * this.clsGlobal.iScreenWidth, this.clsGlobal.iScreenHeight ) * dPart;
     yGraph += this.clsGlobal.iScreenY ; // for drawing this module use absolute

     // console.log( "funcYtoGraphY", yFunc, yGraph, dPart, this.clsGlobal.iScreenY, this.clsGlobal.iScreenWidth );
     return yGraph;
   }

   //
   // convert function x,y value into a graph x,y value
   // give object with variable x and y back
   //
   funcXYtoGraphXY( xFunc, yFunc ) {
     var oGraphXY = {};

     oGraphXY.x = this.funcXtoGraphX( xFunc );
     oGraphXY.y = this.funcYtoGraphY( yFunc );

     return oGraphXY;
   }

   createGraph() {
      this.deleteElement();

      var oStartXY = {};
      var oEndXY   = {};

      if (this.graphAxeShow == true) {
        oStartXY = this.funcXYtoGraphXY( this.graphXStart, 0 );
        oEndXY   = this.funcXYtoGraphXY( this.graphXEnd  , 0 );

        // console.log( "oStartXY: ", oStartXY );
        // console.log( "oEndXY  : ", oEndXY   );

        this.oLineHor = new drawLine( this.clsGlobal, oStartXY.x, oStartXY.y, oEndXY.x, oEndXY.y, this.graphAxeColor );
        this.oLineHor.setStrokeWidth( this.graphAxeLineWidth );
        this.oLineHor.setZIndex( this.graphAxeZIndex );

        oStartXY = this.funcXYtoGraphXY( 0, this.graphYStart );
        oEndXY   = this.funcXYtoGraphXY( 0, this.graphYEnd   );

        this.oLineVer = new drawLine( this.clsGlobal, oStartXY.x, oStartXY.y, oEndXY.x, oEndXY.y, this.graphAxeColor );
        this.oLineVer.setStrokeWidth( this.graphAxeLineWidth );
        this.oLineVer.setZIndex( this.graphAxeZOrder );
      }

      var oLine = null;
      var cText = "";
      var oText = null;
      var oSize = null;
      var xPos  = 0 ;
      var yPos  = 0 ;

      for ( xPos = this.graphXStart; xPos <= this.graphXEnd; xPos += this.graphXStep) {
        oStartXY = this.funcXYtoGraphXY( xPos, this.graphYStart );
        oEndXY   = this.funcXYtoGraphXY( xPos, this.graphYEnd   );

        if ( this.graphGridShow == true ) {
          oLine = new drawLine( this.clsGlobal, oStartXY.x, oStartXY.y, oEndXY.x, oEndXY.y, this.graphGridColor );
          oLine.setStrokeWidth( this.graphGridLineWidth );
          oLine.setZIndex(      this.graphGridZIndex    );

          this.oLinesVer.push( oLine )
        }

        if (xPos == this.graphXStart) { continue; }
        if (xPos == this.graphXEnd  ) { continue; }

        if ( this.graphNumberShow == true ) {
          cText    = (Math.round( xPos * 10000 ) / 10000) .toString();
          oStartXY = this.funcXYtoGraphXY( xPos, 0 );
          oText    = new drawText( this.clsGlobal, oStartXY.x, oStartXY.y, [  { text: cText, style: "fill:" + this.graphNumberColor }] );
          oText.setZIndex(   this.graphNumberZIndex   );
          oText.setFontSize( this.graphNumberFontSize );

          oSize = oText.getSize();

          oStartXY.x -= oSize.width / 2 ;
          oStartXY.y += oSize.height - 2 ;

          if (xPos < 0) {
            oStartXY.x -= oSize.width / 4 ;
          }

          if (xPos == 0) {
            oStartXY.x -= oSize.width;
          }

          oText.setPosition( oStartXY.x, oStartXY.y );

          this.oNumHor.push( oText );
        }
      }

      for ( yPos = this.graphYStart; yPos <= this.graphYEnd; yPos += this.graphYStep) {
        oStartXY = this.funcXYtoGraphXY( this.graphXStart, yPos );
        oEndXY   = this.funcXYtoGraphXY( this.graphXEnd  , yPos );

        if ( this.graphGridShow == true ) {
          oLine = new drawLine( this.clsGlobal, oStartXY.x, oStartXY.y, oEndXY.x, oEndXY.y, this.graphGridColor );
          oLine.setStrokeWidth( this.graphGridLineWidth );
          oLine.setZIndex(      this.graphGridZIndex    );

          this.oLinesHor.push( oLine )
        }

        if (yPos == 0               ) { continue; }
        if (yPos == this.graphYStart) { continue; }
        if (yPos == this.graphYEnd  ) { continue; }

        if (yPos != 0 && this.graphNumberShow == true) {
          cText    =  (Math.round( yPos * 10000 ) / 10000) .toString();
          oStartXY = this.funcXYtoGraphXY( 0, yPos );
          oText    = new drawText( this.clsGlobal, oStartXY.x, oStartXY.y, [  { text: cText, style: "fill:" + this.graphNumberColor }] );
          oText.setZIndex(   this.graphNumberZIndex   );
          oText.setFontSize( this.graphNumberFontSize );

          oSize = oText.getSize();

          oStartXY.x -= oSize.width + 2 ;
          oStartXY.y += oSize.height / 4 ;

          oText.setPosition( oStartXY.x, oStartXY.y );

          this.oNumVer.push( oText );
        }

      }
   }
   deleteElement() {
      if ( this.oLineHor != null ) {
         this.oLineHor.deleteElement();
         this.oLineHor = null;
      }
      if ( this.oLineVer != null ) {
         this.oLineVer.deleteElement();
         this.oLineVer = null;
      }
      for( const oObject of this.oLinesHor ) { oObject.deleteElement(); }
      for( const oObject of this.oLinesVer ) { oObject.deleteElement(); }
      for( const oObject of this.oNumHor   ) { oObject.deleteElement(); }
      for( const oObject of this.oNumVer   ) { oObject.deleteElement(); }

      this.oLinesHor = [];
      this.oLinesVer = [];
      this.oNumHor   = [];
      this.oNumVer   = [];

      super.deleteElement();
   }

}


class drawGraphLine extends drawBase {

   constructor( oGlobal, oGraph ) {

     super( oGlobal );

     this.arrPoints  = []; // array of points given
     this.oPoints    = []; // array of points on screen = drawPoint object
     this.pointColor = "red";
     this.oGraph     = oGraph ; // drawGraph
     this.zIndex     = 50;
   }

   setPoints( arrPoints ) {
     // console.log( "setPoints:" , arrPoints );
     this.arrPoints = arrPoints;
   }
   setColor( cColor ) {
     this.pointColor = cColor;
   }

   createGraphLine() {

      // console.log( "createGraphLine:" , this.oPoints );
      this.deleteElement();

      var oXY = {};
      var xPos = 0;
      var yPos = 0;
      var yArr = [];
      var oPoint = null;
      var yPoint = null;
      var oDraw  = null;

      // console.log( "Start createGraphLine", this.arrPoints );

      // for the moment only the real parts
      for (var iCnt = 0; iCnt < this.arrPoints.length; iCnt++) {
        oPoint = this.arrPoints[ iCnt ]

        // console.log( "createGraphLine, oPoint:", oPoint );

        xPos = oPoint.x.re;
        if (xPos < this.oGraph.graphXStart) {
          continue;
        }
        if (xPos > this.oGraph.graphXEnd) {
          continue;
        }

        yArr = oPoint.y ;

        // console.log( "yArr:", yArr );

        for( var iYCnt = 0; iYCnt < yArr.length; iYCnt++) {
          yPoint = yArr[ iYCnt ];
          yPos = yPoint.re ;

          if ( yPos < this.oGraph.graphYStart ) {
            continue;
          }
          if ( yPos > this.oGraph.graphYEnd ) {
            continue;
          }

          // console.log( "points: ", xPos, yPos );

          // convert to screen positions
          oXY = this.oGraph.funcXYtoGraphXY( xPos, yPos );

          // console.log( "oXY:" , oXY, this.pointColor );

          oDraw = new drawPoint( this.clsGlobal, oXY.x, oXY.y, this.pointColor );
          oDraw.setZIndex( this.zIndex );

          this.oPoints.push( oDraw );
        }
      }
   }
   deleteElement() {
      for( const oObject of this.oPoints ) { oObject.deleteElement(); }

      this.oPoints = [];

      super.deleteElement();
   }

}
