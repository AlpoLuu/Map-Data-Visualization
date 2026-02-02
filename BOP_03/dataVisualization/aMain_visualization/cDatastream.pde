
// might be scrapped for data processing purposes: too much data to be loaded solely through a class into one big array
// manual calculation to compress is done by hand and filtered through requests from processing to pyCharm

class DatumRow{
  
    private String provider; //sets coordinates, str info and data
    private String time;
    private String name;
    
    //private float latitude;
    //private float longitude;
    
    private float equY;
    private float equX;
    
    private float merY;
    private float merX;
    
    private float robY;
    private float robX;
    
    private float gallY;
    private float gallX;
    
    private float data;
    
    private DataInputStream stream;
    
    private int displayType = 0; // is the thing a point, sector ( all things are pretty much point )
  
    private DatumRow(DataInputStream reader){
      this.stream = reader;
    }
    
    private void readArraySent(){
      
    }
}

class Dict{
  private String key1;
  private int value1;
  
  private Dict(String keyOutside, int valueOutside){
    this.key1 = keyOutside;
    this.value1 = valueOutside;
  }
}
