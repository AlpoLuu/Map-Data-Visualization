void draw(){
    //loadData();
    translate(50,500);
    scale(0.50);
    image(mapImage,0,0);
    display();
    //GUI();
}

void display(){
  
}

void GUI(){
  fill(BLACK);
  rect(0, 0, 300, 1920);
}

void displayAtmosphere(){
}

void displayOcean(){
}

void displayEvents(){
}

void displayISS(){ // convert ISS position (x,y,z) if it's not in lat,long to lat,long then re-map back to mapping x,y
}
