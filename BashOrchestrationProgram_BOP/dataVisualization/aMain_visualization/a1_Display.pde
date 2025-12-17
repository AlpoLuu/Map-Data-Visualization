void draw(){
    display();
    GUI();
}

void display(){
  switch(mapState){
    case 0:
      mercatorMap();
    case 1:
      robinsonMap();
    case 2:
      gallPetersMap();
  }
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

void displayISS(){
}
