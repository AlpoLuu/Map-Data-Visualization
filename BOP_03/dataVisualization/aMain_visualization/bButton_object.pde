class Button extends GUI{

  private int form; //0 is used for toggleables between states ( ON / OFF, THISDATA or NOTTHISDATA )
  private int state;

  public Button(int formToTake, int ifModulo, int[] dimensionsToSet, color[] GUIcolors ){
      this.form = formToTake;
      this.dimensions = dimensionsToSet;
      this.colors = GUIcolors;
  }
  
  public void buttonVisual(){ //displays a button, with a text ontop the button
    if(state == 0){ //depending on state, make the button a particular color
      fill(this.colors[0]);
    }else{
      fill(this.colors[1]);
    }
    rect(this.dimensions[0],this.dimensions[1],this.dimensions[2],this.dimensions[3]); //draws button
    fill(WHITE); // makes text white, aligns leftward, draws text with current state 
    textSize(20);
    textAlign(LEFT);
    text(this.name + " " + this.state,this.dimensions[0],this.dimensions[1]);
  }
  
  public void mouseReleased() { // this is button collision
    if( mouseBooleanRect(mouseX, mouseY, this.dimensions) ){ //when mouse released on button dimensions, flips state value between 0 and 1
      state = (state+1)%2;
    }
    
   
  }
  
  
}
