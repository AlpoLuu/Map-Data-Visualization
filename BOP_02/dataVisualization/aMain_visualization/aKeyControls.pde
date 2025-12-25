
int xTranslate = 0;
int yTranslate = 0;

void transformImage(int projType){ //translate the screen using keys with pushmatrix and popmatrix
  pushMatrix();
  
  switch(projType) {
    case 1:
      
      break;
     
    case 2:
    
      break;
    
    case 3:
    
      break;
  }
  translate(xTranslate,yTranslate);
  display();
  popMatrix();
}
