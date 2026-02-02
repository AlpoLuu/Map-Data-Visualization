/*
GUI
parent class for all interactive and non-interactive, mainly used to standardize properties ( lock, space, set conditions ) so interactions with eachother are cleaner

Can be made fancier if I ever come back to re-design BOP

*/

class GUI{
  
  //all gui elements will be made using pos of top-left corner, and dimensions: setting the standard through the parent object
  //all gui elements will be rectangles
  
  public String name;
  
  protected int[] dimensions = new int[4];
  
  public int value = 0;

  protected color[] colors = new color[2];
  
  //protected int localH = 0; // GUI will have a local and global hierarchy ( global hierarchy is not in any object, and initialized before void setup ) ( used to distinguish things close to eachother )
  
  
  
  
  //define a function for only tracking within a bounding box ( specified by dimensions of object ) for all instantiated objects 
    // How do I reduce the amounting of track check bounding boxes
      // There are shape simplification, check for overlap though there are not gonna be enough complex shapes for this to matter
    
  //define a function for locking interaction-state based on a "lock" toggle system where:
    // a GUI that is being used toggles lock, unless condition ( where the condition for unlocking can be exiting a bigger bounding box, a key, timer, rapid clicks, . . . )
    
  
  protected void mouseReleased(){
  }
}
