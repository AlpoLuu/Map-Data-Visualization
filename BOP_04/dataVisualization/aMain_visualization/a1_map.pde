/*
Explicit formula for each display projection here

zoom, translateX, translateY
(1.00, 0, 0); section grab (0,0),(2160,1080)
(1.00, 1080, 540); section grab (1080,540),(2160,1080)
for (1,x,y); section grab (x,y),(2160,1080)

s is zoom, x is translateX, y is translateY

( scale is from corner )

x, y >= 0
for (1,x,y); section grab (x,y),(2160,1080)

x >= 0, y < 0
for (1,x,y); section grab (x,0),(2160,1080+y)
  
x < 0, y >= 0
for (1,x,y); section grab (0,y),(2160+x,1080)

x,y <= 0
for (1,x,y); section grab (0,0),(2160+x,1080+y)

---------

x, y >= 0
for (0.5,x,y); section grab (x,y),(2160*0.5,1080*0.5)

x >= 0, y < 0
for (0.5,x,y); section grab (x,0),(2160*0.5,1080*0.5)

x < 0, y >= 0
for (0.5,x,y); section grab (0,y),(2160*0.5+x,1080*0.5)

x,y <= 0
for (0.5,x,y); section grab (0,0),(2160*0.5+x,1080*0.5+y)

(s,x,y); section grab (x or 0, y or 0),(2160*s or 2160*s+x, 1080*s or 1080*s+y)
( in processing ); ( in pyCharm )
independent of projection type

*/


// grab column with maptype x and y with its datum then load

void setPointDisplay(color colorOfPoint, int xPos, int yPos){
}
