from math import atan2
import math
#import gtk
from fltk import *
import random
import sys
import copy

class Cell:
   def __init__(self,occ):
       self.occupied=occ
   def __str__(self):
       return str(self.occupied)
class Grid:
   #first coordinate is x (width, i.e. column), second is y (height)
   def __init__(self,w,h):
       self.width=w
       self.height=h
       self.m_grid = [[] for i in range(self.width)]
       for i in range(w):
           for j in range(h):
               self.m_grid[i].append(Cell(0))
       for i in range(5):
           self.populate()
   def populate(self):
       xmax = random.randint(1,self.width/4)
       ymax = random.randint(1,self.height/4)
       xpos = random.randint(int(.1*self.width),int(.6*self.width))
       ypos = random.randint(int(.1*self.height),int(.6*self.height))
       for i in range(xmax):
          for j in range(ymax):
             self.m_grid[xpos + i][ypos+j].occupied=1
   def occupied(self,c):
       if c[0] > self.width or c[1] > self.height:
           return 1
       else:
           return self.m_grid[c[0]][c[1]].occupied
   def occCode(self,pos,code):
       if code == 0:
           return self.occupiedUp(pos)
       if code == 3:
           return self.occupiedRight(pos)
       if code == 2:
           return self.occupiedDown(pos)
       if code == 1:
           return self.occupiedLeft(pos)
   def occupiedRight(self,c):
       if c[0]+1 < self.width and c[0]+1 >= 0:
           return self.m_grid[c[0]+1][c[1]].occupied
       else:
           return 1
   def occupiedLeft(self,c):
       if c[0]-1 < self.width and c[0]-1 >= 0:
           return self.m_grid[c[0]-1][c[1]].occupied
       else:
           return 1
   def occupiedUp(self,c):
       if c[1]+1 < self.height and c[1]+1 >= 0:
           return self.m_grid[c[0]][c[1]+1].occupied
       else:
           return 1
   def occupiedDown(self,c):
       if c[1]-1 < self.height and c[1]-1 >= 0:
           return self.m_grid[c[0]][c[1]-1].occupied
       else:
           return 1
   def showScreen(self):
       for j in range(self.height):
           for i in range(self.width):
               print self.m_grid[i][j]
           print ' '
#    def show(self):
#        for i in range(self.width):
#            for j in range(self.height):
#                if self.m_grid[i][j].occupied is 0:
#                    fl_rectf(5*i,5*j,5,5,255,255,255)
#                else:
#                    fl_rectf(5*i,5*j,5,5,0,0,0)
   def __str__(self):
       s = str('')
       for j in range(self.height-1,-1,-1):
           for i in range(self.width):
               s += self.m_grid[i][j].__str__() + ' '
           s += '\n'
       return s
   def showPos(self,pos):
       s = str('')
       for j in range(self.height-1,-1,-1):
           for i in range(self.width):
               if (i,j) == pos:
                   s += 'X' + ' '
               else:
                   s += self.m_grid[i][j].__str__() + ' '
           s += '\n'
       return s
   def printPath(self,path):
       s = str('')
       for j in range(self.height-1,-1,-1):
           for i in range(self.width):
               if (i,j) in path:
                   s += 'X' + ' '
               else:
                   s += self.m_grid[i][j].__str__() + ' '
           s += '\n'
       return s
   def drawGrid():
       for j in range(self.height-1,-1,-1):
           for i in range(self.width):
               print i,j

# class Square(Fl_Button):
#     def __init__(self,xpos,ypos,width,height, color, label = None):
#         self.fill_c = color
#         Fl_Button.__init__(self,xpos,ypos,width,height,label)
#         self.box(FL_FLAT_BOX)

# class gridWindow(Fl_Window):
#     def __init__(self,dimx,dimy,grid,label=None):
#         Fl_Window.__init__(self,dimx,dimy,label)
#         window.label(label)

class bug2:
   def __init__(self,s,t):
       self.start = s
       self.end = t
       self.rise = float(self.end[1]-self.start[1])
       self.run = float(self.end[0]-self.start[0])
       self.path = []
       self.myDir = 0
       self.findDirectPath()
   def doBug2(self,grid):
       self.bug2Path = []
       self.bug2Path += self.start,
       self.pos = self.start
       mark = (0,0)
       while self.pos != self.end:
           next = self.path.index(self.pos) + 1
           #if the path is obstructed
           if grid.occupied(self.path[next]):
               #mark the position
               mark = self.pos
               self.myDir = self.getDir(self.path[next-1],self.path[next])
               print 'stuck from', self.pos, self.path[next]
               length = self.circumNavigate(mark,grid)
               if length == 0:
                   'there is no path to goal'
                   print grid.showPos(self.getCurrent(self.bug2Path))
                   return 0 #failure
               else:
                   self.pos = self.getCurrent(self.bug2Path)
                   continue
           #otherwise, carry on
           else:
              self.bug2Path += self.path[next],
              self.myDir = self.getDir(self.path[next-1],self.path[next])
              self.pos = self.getCurrent(self.bug2Path)
       print 'the ant has arrived in candy land'
       return 1 #success
   def circumNavigate(self,marker,grid):
       print 'encountered object direction:',self.myDir, ' at marker ',marker
       localpos = copy.deepcopy(marker)
       localPath = []
       localPath += marker,
       print grid.printPath(localPath)
       #turn to right
       self.myDir = (self.myDir - 1)%4
       while True:
          if localpos in self.path and self.path.index(localpos) > self.path.index(marker):
             print 'arrived back to direct path'
             print localpos
             print 'localPath was:', localPath
             self.bug2Path += copy.deepcopy(localPath) #arrived back to the ST direct path
             return len(localPath)
          else:
             print 'local path is now',localPath
             moved = False
          # for i in range(-1,3,1):
          #     if not grid.occCode(localpos,(self.myDir+i)%4) and moved is False:
          #         print 'moving', (self.myDir+i)%4
          #         self.move(localPath,(self.myDir+i)%4)
          #         localpos = self.getCurrent(localPath)
          #
          #         print 'just moved',self.myDir
           #############################################################
           #KEEP THE OBJECT TO THE LEFT OF OUR FORWARD MOVING DIRECTION
           #i.e. myDir+1
           #############################################################
             #turn to left relative to current direction
#             a = raw_input('press any key to go')
             for i in range(5,1,-1):
                if not grid.occCode(localpos,(self.myDir+i)%4):
                   self.move(localPath,(self.myDir+i)%4)
                   moved = True
                   break
                elif i is 2:
                   print 'hopelessly lost'
             # if not grid.occCode(localpos,(self.myDir+1)%4):
             #    self.move(localPath,(self.myDir+1)%4)
             #    moved = True
             # #otherwise, try current direction
             # elif not grid.occCode(self.myDir,localPath):
             #    self.move(localPath,self.myDir)
             # elif not grid.occCode((self.myDir-1)%4,localPath):
             #    self.move(localPath,(self.myDir-1)%4)
             # elif not grid.occCode((self.myDir-2)%4):
             #    self.move(localPath,(self.myDir-2)%4)
             # else:
             #    print 'hopelessly lost'
             #    return 0
             localpos = self.getCurrent(localPath)
             print grid.printPath(localPath)
             if moved is False:
                print 'no path found; cannot find direction to move'
                return 0
             if localpos == marker and len(localPath) > 1:
                print 'no path found'
                print grid.printPath(localPath)
                print localPath
                return 0
   def getDir(self,pos1,pos2):
       if pos2[0]-pos1[0] == 1:
           return 3 #right
       if pos2[1]-pos1[1] == 1:
           return 0 #up
       if pos2[0]-pos1[0] == -1:
           return 1 #left
       if pos2[1]-pos1[1] == -1:
           return 2 #down
   def findDirectPath(self):
       self.path += self.start,
       if self.run == 0.0:
           if self.end[1] > self.start[1]:
               while self.getCurrent(self.path) != self.end:
                   self.moveUp(self.path)
               return
           else:
               while self.getCurrent(self.path) != self.end:
                   self.moveDown(self.path)
               return
       elif self.rise == 0.0:
           if self.end[0] > self.start[0]:
               while self.getCurrent(self.path) != self.end:
                   self.moveRight(self.path)
               return
           else:
               while self.getCurrent(self.path) != self.end:
                   self.moveLeft(self.path)
               return
       else:
           self.slope = self.rise/self.run
           self.vdir = atan2(self.rise,self.run)
           current = self.start
           while current != self.end:
               if self.vdir > 0:
                   if self.end[0] > self.start[0]:
                       if int(math.floor(self.f(self.path[len(self.path)-1][0]+1))) == self.path[len(self.path)-1][1]:
                           self.moveRight(self.path)
                       else:
                           self.moveUp(self.path)
                   else:
                       if int(math.floor(self.f(self.path[len(self.path)-1][0]-1))) == self.path[len(self.path)-1][1]:
                           self.moveLeft(self.path)
                   #otherwise move up one unit
                       else:
                           self.moveUp(self.path)
               else:
               #slope is negative
               #bottom to top
                   if self.end[0] > self.start[0]:
                       if int(math.ceil(self.f(self.path[len(self.path)-1][0]+1))) == self.path[len(self.path)-1][1]:
                           self.moveRight(self.path)
                       else:
                           self.moveDown(self.path)
               #top to bottom
                   else:
                       if int(math.ceil(self.f(self.path[len(self.path)-1][0]-1))) == self.path[len(self.path)-1][1]:
                           self.moveLeft(self.path)
                       else:
                           self.moveDown(self.path)
               current = self.getCurrent(self.path)
   def sign(self,x):
       if x>0:
           return int(1)
       elif x<0:
           return int(-1)
       else:
           return int(0)
   def dist(self,p1,p2):
       return math.sqrt((p1[1]-p2[1])**2+(p1[0]-p2[0])**2)
   def f(self,x):
       return float(self.slope*x + (self.start[1]-self.slope*self.start[0]))
   def __str__(self):
       return str(self.path)
   def move(self,path,code):
       if code == 0:
           self.moveUp(path)
       if code == 3:
           self.moveRight(path)
       if code == 2:
           self.moveDown(path)
       if code == 1:
           self.moveLeft(path)
   def moveUp(self,path):
       print 'move up'
       self.myDir = 0
       path += (path[len(path)-1][0],path[len(path)-1][1]+1),
   def moveDown(self,path):
       print 'move down'
       self.myDir = 2
       path += (path[len(path)-1][0],path[len(path)-1][1]-1),
   def moveLeft(self,path):
       print 'move left'
       self.myDir = 1
       path += (path[len(path)-1][0]-1,path[len(path)-1][1]),
   def moveRight(self,path):
       print 'move right'
       self.myDir = 3
       path += (path[len(path)-1][0]+1,path[len(path)-1][1]),
   def getCurrent(self,path):
       return path[len(path)-1]

class Square(Fl_Widget):
   def __init__(self,xpos,ypos,width,height, color, label = None):
       self.fill_c = color
       Fl_Widget.__init__(self,xpos,ypos,width,height,label)
   def draw(self):
       fl_rectf(self.x(),self.y(),self.w(),self.h(),self.fill_c)
   def handle(self,e):
       a = super(Fl_Widget,self).handle(e)
       if a == FL_PUSH:
           print 'button pushed'
   def redraw(self):
       self.draw()

class gridWindow(Fl_Window):
   def __init__(self,dimx,dimy,grid,label="gridWindow"):
       Fl_Window.__init__(self,100,100,dimx,dimy,label)
       self.drawGrid(grid)
   def drawGrid(self,grid):
       for i in range(grid.width):
           for j in range(grid.height):
               if grid.m_grid[i][j].occupied is 1:
                   s=Fl_Button(i*5,j*5,5,5,FL_BLACK)
                   s.box(FL_FLAT_BOX)
                   s.show()
               else:
                   s=Fl_Button(i*5,j*5,5,5,FL_WHITE)
                   s.box(FL_FLAT_BOX)
                   s.show()

def Test():
   bug = bug2((0,0),(19,19))
   grid = Grid(20,20)
   print bug
   print grid
#   a=raw_input('g to go')
   go(bug,grid)
def go(bug,grid):
   bug.doBug2(grid)
   print 'the final path is:\n', bug.bug2Path
   print 'the direct path is:\n', bug.path
   print 'no path\n', grid
   print 'the final path: \n', grid.printPath(bug.bug2Path)
#   print 'compare to the direct path\n', grid.printPath(bug.path)

if __name__ == "__main__":
   Test()
