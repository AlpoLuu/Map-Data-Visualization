

void controlAggregate(int translateX, int translateY,  float zoomAmount){
  pushMatrix();
  translate(-translateX, -translateY);
  scale(zoomAmount);
  
}

void zoomOnCursor(){
  
}

/*
void moveMap(int keyPressed1){
  if(keyPressed1 == 87){ // move map upwards, w
    translateY += 0.05;
  }
  if(keyPressed1 == 83){ // move map downwards, s
    translateY -= 0.05;
  }
    if(keyPressed1 == 65){ // move map left, a
    translateX += 0.05;
  }
  if(keyPressed1 == 68){ // move map right, d
    translateX -= 0.05;
  }
}*/

void keyPressed(){
  println(keyCode, key);
  //87 = w, 65 = a, 83 = s, 68 = d
  
  if(keyCode == 87){ // move map upwards, w
    mapPosY = mapPosY + 25;
  }
  if(keyCode == 83){ // move map downwards, s
    mapPosY = mapPosY - 25;
  }
  if(keyCode == 65){ // move map left, a
    mapPosX = mapPosX + 25;
  }
  if(keyCode == 68){ // move map right, d
    mapPosX = mapPosX - 25;
  }
  if(keyCode == 84){ //press "t" to rotate between map types
    toMakeImage = 0;
    mapOff = (mapOff+2)%8;
  }
  
}


void keyReleased(){
  //70 = f, 82 = r
  if(keyCode == 70){ // zoom map, r
    scaleMult = scaleMult + 0.10;
  }
  if(keyCode == 82){ // zoom map, f
    scaleMult = scaleMult - 0.10;
  }
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
