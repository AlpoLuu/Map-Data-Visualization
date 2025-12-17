//I'll attempt encapsulation, though it only seems relevant if the object

//array for projections ( mercator, robinson, gall-peters )

color BLACK = #000000;
color WHITE = #FFFFFF;

int mapState = 0; // 0 - 2 ( inclusive ) 0 being mercator, 1 being robinson, 2 being gallPeters map

import java.io.*;

BufferedReader reader;


//array for temperature
//color[] temperature = { #FFDD00,#FF8400,#FF0000 } left to right: yellow, orange, red ( yellow being hot --> red being cold )

//testing variables
int[][] array = {{1,2},{1,2,3},{1,2,3,4}};

void setup() {
  size(1920, 1080);
  background(WHITE);
  rectMode(CORNERS);
  noSmooth();
  noStroke();
  
  test2DArrayLength();

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
//Projections for Map
//Fractional value or Binary value for map data
//Fractional use anti-aliasing, Binary anti-alias on top display
void mercatorMap(float[] mappingData) { //use 2D array of x-y to plot mercator projection (fractional/binary for [land/sea, x, y][mercator/robinson/gallPeters])
  mapType = 0

  for ( int i = 0; i < mappingData[1].length; i++ ) {
    for ( int j = 0; j < mappingData[2].length; j++ ) {
      if (mappingData[0][0] == 0) {
        fill(#455466);
      } else {
        fill(#708070);
      }
      point(mappingData[1][mapType],mappingData[2][mapType]);
    }
  }
  
  
}

//I may have to learn some rendering math
//chunk to hide non-displayed things

void robinsonMap() { //use 2D array of x-y to plot mercator projection

}

void gallPetersMap() {
}

//I need to add the ability to move around on the map using either WASD or arrow keys
