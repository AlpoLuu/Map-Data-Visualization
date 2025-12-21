void testMap(){
   // /home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)\RF_megafile_mask_downsampled 
   
     // Load binary data
  byte[] rawData = loadBytes("/home/user/Desktop/Sand and Star/BashOrchestrationProgram_BOP/data/NOAA(elevation tiles)/RF_megafile_mask_downsampled");
  
  // Create image from data
  mapImage = createImage(2700, 1350, RGB); //4x for 10800x5400, 8x for 5400x2700, 16x for 2700x1350, 32x for 1350x675 (2x is the limit for downsample amount )
  mapImage.loadPixels();
  
  for (int i = 0; i < rawData.length && i < mapImage.pixels.length; i++) {
    // Map 0/1 flags to colors
    if (rawData[i] == 0) {
      mapImage.pixels[i] = SEA;
    } else {
      mapImage.pixels[i] = LAND;
    }
  }
  
  mapImage.updatePixels();
  noLoop();  // Static image — no need to redraw
}
