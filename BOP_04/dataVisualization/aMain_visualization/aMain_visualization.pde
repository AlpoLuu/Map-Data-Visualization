import java.io.*;
import java.util.ArrayList;


// I need properties for how the points, global and sectors will be represented
// compression for the representation on processing ( all points do not display a temperature number, only the viewable ones )

// grid gradient for sector data ( interpolate alpha of 128 pixels spaced using the gradient )
  // this includes 

color BLACK = #000000;
color WHITE = #FFFFFF;
color LAND = #67a364;
color SEA = #6473a3;

int mapState = 0; // 0 - 2 ( inclusive ) 0 being mercator, 1 being robinson, 2 being gallPeters ma

int toMakeImage = 0; // state variable for whether to make a new image, so new images aren't made every 50 milliseconds

Table arrayTable;
BufferedReader reader;


//array for temperature
//color[] temperature = { #FFDD00,#FF8400,#FF0000 } left to right: yellow, orange, red ( yellow being hot --> red being cold )

/*
Unit Conversions from standardized units to common units

k ( kelvin in kelvins ) - 273.15 = c ( celsius in degrees celsius ), ( used in all temperature values )
(k - 273.15) * 9/5 + 32 = f ( fahrenheit in degrees fahrenheit ), ( used in American temperature values )
m (meters) * 0.001 = mm ( millimeters ), ( used in total precipitation )
*/

int mapOff = 0; // ( between 0 - 6, variable that controls what map is being displayed )

//testing variables
//int[][] array = {{1,2},{1,2,3},{1,2,3,4}};
PImage mapImageToDisplay;

boolean mapMoveLeft = false;
boolean mapMoveRight = false;
boolean mapMoveUp = false;
boolean mapMoveDown = false;
 
int mapPosX = 0;
int mapPosY = 0;
float scaleMult = 1;

boolean dataUpdate = false;

DataInputStream response_pipe;
PrintWriter pipeWriter;

//ArrayList<DatumRow> rowsData = new ArrayList<DatumRow>();
ArrayList<GUI> guiObjects = new ArrayList<GUI>();

String CSVDir = "/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/dataVisualization/output.csv";

float[][] floatData = new float[11][50_000_000]; //index 8 is data, rest is lat/long with a or not a projection
String[][] stringData = new String[3][50_000_000]; //index 0 is provider, index 1 is time, index 2 is name

IntList mapHits;
IntList CDSHits;

int PROV = 0; int TIME = 1; int NAME = 2; //consts for stringData array

int LAT = 0; int LONG = 1; //consts for floatData array
int Y_EQU = 2, X_EQU = 3, Y_MER = 4, X_MER = 5, Y_ROB = 6, X_ROB = 7, Y_GALL = 8, X_GALL = 9;
int DATA = 10;

void setup() {
  mapHits = new IntList();
  
  size(2160, 1080, P2D);
  background(WHITE);
  rectMode(CORNERS);
  noSmooth();
  noStroke();
  getData(CSVDir);
  
  //data(response_pipe);
}
  //no rasterization, no vectorization for test 1


  //String line = reader.readLine();  // Blocks until data available
  //BufferedReader cyclic = new BufferedReader(new InputStreamReader(System.in));
  //BufferedReader realtime = new BufferedReader(new InputStreamReader(System.in));


//Fractional value or Binary value for map data
//Fractional use anti-aliasing, Binary anti-alias on top display
