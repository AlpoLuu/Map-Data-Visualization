public boolean mouseBooleanRect(int mousePosX, int mousePosY, int[] dimensions){ //mouseX, mouseY are the parameters
  if( ( mousePosX >= dimensions[0] && mousePosX <= dimensions[0]+dimensions[2] )
    && ( mousePosY >= dimensions[1] && mousePosY <= dimensions[1]+dimensions[3] ) ){
    return true;
  }else{
    return false;
  }
}

public void printRow(int row){
  print(stringData[0][row] + " " + stringData[1][row] + " " + stringData[2][row] + " ");
  println(floatData[0][row] + " " + floatData[1][row] + " " + floatData[2][row] + " ");
}

public void readBytes(){
}

public void readString(){
}

public void readFloat(){
}
