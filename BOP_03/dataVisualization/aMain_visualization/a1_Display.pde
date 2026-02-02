/*
DISPLAY FOR ALL DATA
 Data is labelled using tags and categories in pyCharm, accessed using a Processing pipe
 "USGS and NOAA_buoy and Atmosphere"
 
 Every unique type of display data ( disaster, temperature, precipitation, point, section, . . . ) has a function corresponding then only send data that is to be displayed
 
 
 
 
 */

void draw() {
  if ( millis()%50 == 0 ) { // runs program at 20 FPS
    data();
    //translate(0,0);
    scale(0.5);
    //image(mapImage,0,0);
    display();
    //GUI();
    //print(arrayTable);
    //printRow(100);
  }
  //print(mapHits);
}

void display() {
  image(mapImageToDisplay,20,20);
  controlAggregate(mapPosX, mapPosY, scaleMult);
  //image(mapImageToDisplay, 0, 0);
  popMatrix();
}

void GUI() {
  fill(BLACK);
  rect(0, 0, 300, 1920);
}
