/*
Tab for writing to the pipes:
 
 when we make a change to the GUI, it should send the request to the pipe for new updates from PyCharm
 
 .csv
 .txt
 
 What format should the request be in? An array with 2 seperate pipes
 Nope, it's going to be a .csv with UTF+8
 (sectonCorner1, sectionCorner2)
 four ints ( x1,y1,x2,y2 )
 0010|0010|2000|1000 ( little-endian )
 
 (USGS, NOAA_buoy, NOAA_nws, OWM, ISS, NASA_EOnet, OSK)
 binary
 100100 ( USGS and OWM )
 (OSK)
 binary
 
 final file
 xxxx|xxxx|xxxx|xxxx|
 y_1|y_1name|y_2|y_2name
 
 x1,y1,x2,y2
 y_1name,y_1
 y_2name,y_2
 .
 .
 y_n name,y_n
 
 .bin
 
 */

void data() {
  getData("/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/dataVisualization/output.csv");
  mapImage(stringData, floatData);
  sendValues(checkGui()); // (checks GUI to update GUI data values ( if they are changed )) sends new values to pipe to pyCharm
}

public Dict[] checkGui() { // checks all GUI objects ( interactables for their values ) idk how to set the order
  Dict[] guiObjectsInfo = new Dict[guiObjects.size()];

  for ( int i = 0; i < guiObjects.size(); i++) {
  }

  return guiObjectsInfo;
}

public void sendValues(Dict[] nameAndValues ) {
}

void getData(String fileDirToTable) { //gets CSV and turns it into a Processing table
  //arrayTable = loadTable(fileDirToTable, "header");

  BufferedReader reader;

  try {
    reader = new BufferedReader(new FileReader(dataPath(fileDirToTable)), 8 * 1024 * 1024);
  }
  catch (FileNotFoundException e) {
    e.printStackTrace();
    return;
  }
  String line;
  int row = 0;

  int storedTime = millis();

  try {

    reader.readLine();  // skip header
    //line = reader.readLine();
    //println(line);


    while ( (line = reader.readLine()) != null && row < 50_000_000) {
      String[] tokens = split(line, ',');
      int currentTime = millis();
      //println(line + " " + row + " time: " + float((currentTime - storedTime))/1000 );

      // Assuming CSV column order: name, category, region, lat, lon, elev, mag, depth, uncert, offX, offY, weight
      stringData[0][row] = tokens[0];
      stringData[1][row] = tokens[1];
      stringData[2][row] = tokens[2];

      floatData[0][row] = float(tokens[3]);
      floatData[1][row] = float(tokens[4]);
      floatData[2][row] = float(tokens[5]);
      floatData[3][row] = float(tokens[6]);
      floatData[4][row] = float(tokens[7]);
      floatData[5][row] = float(tokens[8]);
      floatData[6][row] = float(tokens[9]);
      floatData[7][row] = float(tokens[10]);
      floatData[8][row] = float(tokens[11]);
      floatData[9][row] = float(tokens[12]);
      floatData[10][row] = float(tokens[13]);

      row++;

      /*if (row%50_000 == 0) {
       println(line + " " + row + " time: " + float((currentTime - storedTime))/1000 );
       }*/
    }

    reader.close();
  }
  catch (IOException e) {
    e.printStackTrace();
  }
}

void mapImage(String[][] stringColumns, float[][] floatColumns) {
  print("lol");
  for (int i = 0; i < 3_500_000; i++) { // there's 3.5 million rows to check and append to maphits
    //println(stringColumns[0][i] + " " + stringColumns[1][i] + " " + stringColumns[2][i] );

    if ("NOAA_ele".equals(stringColumns[0][i]) &&
      "20090101".equals(stringColumns[1][i]) &&
      "map".equals(stringColumns[2][i]))
    {
      //print(i);
      mapHits.append(i);
    }

    //mapImageToDisplay
  }
  //println(mapHits);

  //2,3 for equirectangular Y and X respectively
  //4,5; 6,7; 8,9

  if (toMakeImage == 0) {
    int colX = 3+mapOff, colY = 2+mapOff;

    /*
    println("=== Coordinate diagnostic ===");
     for (int i = 0; i < min(10, mapHits.size()); i++) {
     int entry = mapHits.get(i);
     float x = floatData[colX][entry];
     float y = floatData[colY][entry];
     float lat = floatData[0][entry];
     float lon = floatData[1][entry];
     println("entry " + entry + ": lat=" + lat + " lon=" + lon + " -> y_equ=" + y + " x_equ=" + x);
     }
     
     // Find actual min/max across all map data
     float minX = Float.MAX_VALUE, maxX = -Float.MAX_VALUE;
     float minY = Float.MAX_VALUE, maxY = -Float.MAX_VALUE;
     for (int i = 0; i < mapHits.size(); i++) {
     int entry = mapHits.get(i);
     minX = min(minX, floatData[colX][entry]);
     maxX = max(maxX, floatData[colX][entry]);
     minY = min(minY, floatData[colY][entry]);
     maxY = max(maxY, floatData[colY][entry]);
     }
     
     println("X range: " + minX + " to " + maxX + " (expected 0-1080)");
     println("Y range: " + minY + " to " + maxY + " (expected 0-540)");
     println("Total map hits: " + mapHits.size());
     
     */
    mapImageToDisplay = createImage(2160, 1080, RGB); //map size is 1080 * 540 as image
    mapImageToDisplay.loadPixels();

    for (int i = 0; i < mapImageToDisplay.pixels.length; i++) {
      mapImageToDisplay.pixels[i] = BLACK;
    }

    for (int i = 0; i < mapHits.size(); i++) {
      int entry = mapHits.get(i);
      int px = constrain(round(floatData[colX][entry]), 0, 2159);
      int py = constrain(round(floatData[colY][entry]), 0, 1079);
      int pixel = py * mapImageToDisplay.width + px;
      int data = round(floatData[10][pixel]);
      color c = (data == 1) ? LAND : SEA;

      int radius = 1;  // start with 1, increase if gaps remain
      for (int dy = -radius; dy <= radius; dy++) {
        for (int dx = -radius; dx <= radius; dx++) {
          int nx = constrain(px + dx, 0, 2159);
          int ny = constrain(py + dy, 0, 1079);
          int npixel = ny * mapImageToDisplay.width + nx;
          mapImageToDisplay.pixels[npixel] = c;
        }
      }
    }

    mapImageToDisplay.updatePixels();
    toMakeImage = 1;
  } 
}

  public void displayCDSEra5(){
    int typeOfCDS = 0 // 0 for 2 meter temperature, 1 sea surface temperature, 2 for total precipitation
    
  }
