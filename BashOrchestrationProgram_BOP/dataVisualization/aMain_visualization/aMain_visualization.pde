//I'll attempt encapsulation, though it only seems relevant if the object

//array for projections ( mercator, robinson, gall-peters )

color BLACK = #000000;
color WHITE = #FFFFFF;

int mapState = 0; // 0 - 2 ( inclusive ) 0 being mercator, 1 being robinson, 2 being gallPeters map



//array for temperature 
//color[] temperature = { #FFDD00,#FF8400,#FF0000 } left to right: yellow, orange, red ( yellow being hot --> red being cold )

void setup(){
    size(1920,1080);
    background(WHITE);
    rectMode(CORNERS);
    noStroke();
}


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

/*



dataDisplay

slider and button bar ( black )

slider(


*/

void mercatorMap(){
}

void robinsonMap(){
}

void gallPetersMap(){
}
