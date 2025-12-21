//I'll attempt encapsulation, though it only seems relevant if the object

//array for projections ( mercator, robinson, gall-peters )

color BLACK = #000000;
color WHITE = #FFFFFF;
color LAND = #67a364;
color SEA = #6473a3;

int mapState = 0; // 0 - 2 ( inclusive ) 0 being mercator, 1 being robinson, 2 being gallPeters map

import java.io.*;

BufferedReader reader;


//array for temperature
//color[] temperature = { #FFDD00,#FF8400,#FF0000 } left to right: yellow, orange, red ( yellow being hot --> red being cold )






//testing variables
int[][] array = {{1,2},{1,2,3},{1,2,3,4}};
PImage mapImage;


void setup() {
  size(1920, 1980, P2D);
  background(WHITE);
  rectMode(CORNERS);
  noSmooth();
  noStroke();
  
  test2DArrayLength();
  testMap();

  //no rasterization, no vectorization for test 1

  BufferedReader archived = new BufferedReader(new InputStreamReader(System.in));
  //String line = reader.readLine();  // Blocks until data available
  //BufferedReader cyclic = new BufferedReader(new InputStreamReader(System.in));
  //BufferedReader realtime = new BufferedReader(new InputStreamReader(System.in));
}

//void projectionMath(){ better to pre-process in pycharm than do math in processing, numerical operations are faster on pycharm than in processing )
//}
//only math is done latitude/longitude to "standard grid coordinates" which are then mappable 3 different map types using (presumably) matrix math which processing is slightly better at when small
//I need a good definition for standard grid coordinates

//I'll do the math

void test2DArrayLength(){
  println(array[1].length);
}
  

/*
dataDisplay
 
 slider and button bar ( black )
 
 slider(
 
 
 */

void map(float[][] mappingData, int projType){ // takes the data set and draws every coordinate as a point coloured desaturated blue or desat green
   for ( int i = 0; i < mappingData[1].length - 1; i++ ) {
      if (mappingData[i][1+2 +2+2+2 +1] == 0) { //checks if map val for coordinate is 0 or 1 then sets point colour to desat blue or desat green
        fill(#455466);
      } else {
        fill(#708070);
      }
      point(mappingData[1+i][1+1+projType*2], mappingData[1+i][1+2+projType*2]); //draws point using column i+1 ( val i ), sets position according to projectionType ( mercator, robinson or gall-peters )
   }
}


//Projections for Map
//Fractional value or Binary value for map data
//Fractional use anti-aliasing, Binary anti-alias on top display

/*
void mercatorMap(float[][] mappingData) { //use 2D array of x-y to plot mercator projection (fractional/binary for [lat, long, x_mer, y_mer, x_rob, y_rob, x_gall, y_gall, land/ocean val, temp][station/global point])
  int mapType = 0;
  int mercatorJump

  for ( int i = 0; i < mappingData[1].length; i++ ) {
    for ( int j = 0; j < mappingData[1].length; j++ ) {
      if (mappingData[0][0] == 0) {
        fill(#455466);
      } else {
        fill(#708070);
      }
      point(mappingData[1+mercatorJump][],mappingData[2+mercatorJump][]);
    }
  }
}
*/

//I may have to learn some rendering math
//chunk to hide non-displayed things

/*
void robinsonMap() { //use 2D array of x-y to plot mercator projection

}
*/

/*
void gallPetersMap() {
}*/

//I need to add the ability to move around on the map using either WASD or arrow keys
