

void controlAggregate(int translateX, int translateY,  float zoomAmount){
  pushMatrix();
  translate(-translateX, -translateY);
  scale(zoomAmount);
  
}

void zoomOnCursor(){
  
}

void moveMap(int keyPressed1){
  if(keyPressed1 == 87){ // move map upwards, w
    mapPosY += 5;
  }
  if(keyPressed1 == 83){ // move map downwards, s
    mapPosY -= 5;
  }
    if(keyPressed1 == 65){ // move map left, a
    mapPosX += 5;
  }
  if(keyPressed1 == 68){ // move map right, d
    mapPosX -= 5;
  }
}

void keyPressed(){
  println(keyCode, key);
  //87 = w, 65 = a, 83 = s, 68 = d
}


void keyReleased(){
}

void mouseReleased(){
  for( GUI guiObject : guiObjects ){ //checks mousereleased of every GUI object including children slider and button
    if(guiObject instanceof Button){ //checks mousereleased if GUI is a button
      Button buttonObject = (Button) guiObject;
      buttonObject.mouseReleased();
    }
    if(guiObject instanceof Slider){ //checks mousereleased if GUI is a slider
      Slider sliderObject = (Slider) guiObject;
      sliderObject.mouseReleased();
    }
    //if(!(guiObject instanceof Slider) && !(guiObject instanceof Button)){
    //}
  }
}
