/*
DISPLAY FOR ALL DATA
 Data is labelled using tags and categories in pyCharm, accessed using a Processing pipe
 "USGS and NOAA_buoy and Atmosphere"
 
 Every unique type of display data ( disaster, temperature, precipitation, point, section, . . . ) has a function corresponding then only send data that is to be displayed
 
 
 
 
 */

void draw() {
  if ( dataUpdate == false ) { // runs program at 20 FPS
    data();
    dataUpdate = true;
    //translate(0,0);
    //image(mapImage,0,0);
    //print(arrayTable);
    //printRow(100);
  }
  if(mapImageToDisplay != null){
    background(BLACK);
    display();
  }
  GUI();
  
  //print(mapHits);
}

void display() {
  controlAggregate(mapPosX, mapPosY, scaleMult);
  image(mapImageToDisplay,20,20);
  //image(mapImageToDisplay, 0, 0);
  popMatrix();
}

void GUI() {
  fill(#222222);
  rect(0, 0, 300, 1920);
}
