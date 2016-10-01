# D. Bonneau 2015
# A hexagon tile based board generator
# 

import pygame
from pygame.locals import *

#import pygl2d and math
import sys; sys.path.insert(0, "..")
#import pygl2d
from numpy import *
MOUNTAIN = 3
ROCKS = 2
PLAIN = 1

SIN60 = 0.866025404
SIN30 = 0.5

SIDE = 35.
HSTEP = SIDE*(1+SIN30)
VSTEP = SIDE*2*SIN60



# Hexagonal tile
class HexTile(object):
    terrain = PLAIN
    def __init__(self,filename = "hex.png"):
        self.angle = 0
        self.alpha = 255.0
        self.scale = 1.0
        self.setScale(self.scale)
        self.points.reverse()
        self.font = None
        self.coord_text_display = None
        self.last_position = None
        self.color = [255,125,0]
        
    def setFont(self,font):
        self.font = font 
        
    def setScale(self,scale):
        self.scale = scale
        side = SIDE*self.scale
        self.points = [[side*SIN30,0],
                       [side*(SIN30+1),0],
                       [side*2,side*SIN60],
                       [side*(SIN30+1),2*side*SIN60],
                       [side*SIN30,2*side*SIN60],
                       [0,side*SIN60],
                       [side*SIN30,0]]
    
    def setTextCoord(self,text):
        pass
        #self.coord_text_display.change_text(text)
        
    def drawCoord(self,coord ):
        pass
        #self.coord_text_display.draw(coord)
    
    def draw(self,surf, position = [0,0]):
        pts = [(position[0] + x, position[1] +y) for (x,y) in self.points]
        self.last_position = position

        pygame.draw.polygon(surf, self.color, pts)
        pygame.draw.lines(surf, [0,0,0],True, pts,2)
    
    def printDbgInfo(self):
        print self.last_position
    
# Board storing all the hexagonal tiles        
class Board(object):
    def __init__(self,width=20,height=10):   
        self.scale = 1.0
        self.width = width
        self.height = height
        self.hexs = {}
        for j in arange(height):
            for i in arange(width):
                h = HexTile()
                h.setFont(pygame.font.SysFont("Courier New", 16, bold=True))
                h.setTextCoord("(%d,%d)" %(i,j)) # Set default text to be coordinate
                
                self.setHex(h,(i,j))
    
    def genHexBoard(self,size = 7):
        
        N = 2 * size - 1
        self.width = N
        self.height = N
        self.hexs = {}
        len_col = size
        j0 = size /2 - 1
        for i in range(N):
            dj0 = 0

            print len_col
            for j in range(1,len_col+1):
                h = HexTile()
                h.setFont(pygame.font.SysFont("Courier New", 16, bold=True))
                h.setTextCoord("(%d,%d)" %(i,j)) # Set default text to be coordinate
                pos =(i ,j + j0 + dj0)
                self.setHex(h,pos)
                print  "    ", pos
                
            if i < size -1:
                len_col += 1
                if i % 2 == 0:
                    j0 -= 1
            else:
                len_col -= 1
                if i % 2:
                    j0 += 1
            
    def getHex(self,pos):
        if not pos in self.hexs.keys():
            return None
        return self.hexs[pos]

    def setHex(self,hex,pos):
        self.hexs[pos] = hex
        
    def getSize(self):
        return self.width,self.height
        
    def setScale(self,scale):
        self.scale = scale
        for h in self.hexs.values():
            h.setScale(scale)
    
    def draw(self,surf,position ,sub_board_boundaries):

        # Draw hexs
        
        x0,y0 = position
        dx_text,dy_text = HSTEP*self.scale / 2,VSTEP*self.scale / 2
        i_min,i_max,j_min,j_max = sub_board_boundaries
        if i_min % 2 == 0:
            a_even_i = arange(i_min,i_max,step = 2)
            a_odd_i = arange(i_min+1,i_max,step = 2)
        else:
            a_even_i = arange(i_min+1,i_max,step = 2)
            a_odd_i = arange(i_min,i_max,step = 2)
        a_js = arange(j_min,j_max) 
        
        for i in a_even_i: 
            for j in a_js:
                y = j*VSTEP*self.scale+y0
                h = self.getHex((i,j))
                if h != None:
                    h.draw(surf, [i*HSTEP*self.scale+x0,y])
        for i in a_odd_i: 
            for j in a_js:
                y = (j+0.5)*VSTEP*self.scale+y0
                h = self.getHex((i,j))
                if h != None:
                    h.draw(surf,[i*HSTEP*self.scale+x0,y])
             

# Camera for displaying the board        
class Camera(object):
    def __init__(self,screen_size,board):
        self.board = board
        self.camera_speed = 12.5
        self.position = array([0,0])
        self.scale = 1.0
        self.screen_size = screen_size
        self.scales = [0.5, 1.0, 2.0, 4.0]
        self.scale_index = 1
        
        self.scale = self.scales[self.scale_index]
        self.surface = pygame.Surface(screen_size)
        background = pygame.Surface(self.surface.get_size())
        self.background = background.convert()
        self.background.fill([60,197,255])
        
    def zoomIn(self):
        self.scale_index += 1
        if self.scale_index >= len(self.scales ) -1 :
            self.scale_index = len(self.scales ) -1
        self.setScale(self.scales[self.scale_index])
    def zoomOut(self):
        self.scale_index -= 1
        if self.scale_index <= 0 :
            self.scale_index = 0
        self.setScale(self.scales[self.scale_index])
        
    def setScale(self,scale):
        self.scale = scale
        self.board.setScale(self.scale)
        
    def moveUp(self,dt):    
        self.position[1]+= dt*self.camera_speed
    
    def moveDown(self,dt):    
        self.position[1]+= -dt*self.camera_speed
        
    def moveLeft(self,dt):    
        self.position[0]+= -dt*self.camera_speed
    
    def moveRight(self,dt):    
        self.position[0]+= dt*self.camera_speed  

    def Pix2Hex(self,coord):
    
        side = SIDE * self.scale
        hstep = HSTEP * self.scale
        vstep = VSTEP * self.scale
        xpix,ypix = coord
        xpix += self.position[0]
        ypix -= self.position[1]
        
        # First get integer X
        x_hex = floor(xpix/hstep)
        if x_hex%2 ==0 :
            y_hex = floor(ypix/vstep)
        else:
            y_hex = floor(ypix/vstep-0.5)
        
        dx = xpix-x_hex*hstep
        dy = ypix-y_hex*vstep
        
        if dy< (side*SIN30-dx)*SIN60/SIN30:
            print "x-1 ; y-1"
            x_hex-=1
            y_hex-=1
        elif dy>dx/SIN30+hstep/2:
            print "x-1 "
            x_hex-=1
        x_hex = int(x_hex)
        y_hex = int(y_hex)
        print (dx,dy),(dy,dx/SIN30), "->" , (x_hex,y_hex )
        #print (x_hex,y_hex), self.board.getHex(x_hex,y_hex).printDbgInfo()
        return x_hex,y_hex    
        
    def draw(self):
        board_width,board_height = self.board.getSize() # in tiles
        screen_width,screen_height = self.screen_size # in pixels
        hex_height = VSTEP * self.scale
        hex_width = HSTEP * self.scale
        hex_side = SIDE * self.scale
        # self.hex_side = hex_side
        min_i = int(max(0,floor(self.position[0]/(hex_width)-1)))
        max_i = int(min(board_width,(ceil(self.position[0]+screen_width)/(hex_width)+1)))
        
        min_j = int(max(0,floor(-self.position[1]/hex_height)-1))
        #min_j = int(floor(-self.position[1]/hex_height)-1)
        max_j = int(min(board_height,ceil((-self.position[1]+screen_height)/hex_height)+1))
        
        sub_board_boundaries = [min_i,max_i,min_j,max_j]
        self.sub_board_boundaries = sub_board_boundaries
        
        self.surface.blit(self.background,(0,0))
        # Should invert both positions in principle, but the y-axis is inverted for display...
        self.board.draw(self.surface,[-self.position[0],self.position[1]],sub_board_boundaries)

    def print_dbg(self):
        print self.position
        print self.sub_board_boundaries
        print 
        
def main():
    
    print "init..."
    #init pygl2d
    SCREEN_WIDTH,SCREEN_HEIGHT = 1024,500
    SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]
    pygame.init()
    pygame.display.set_caption("")
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    
    #pygl2d.window.init(screen_size)
    #create starting objects
    clock = pygame.time.Clock()
    board =  Board(width = 0,height = 0)
    board.genHexBoard(size = 5)
    cam = Camera(SCREEN_SIZE,board)
    cam.setScale(1.0)
    #Create some text
    font = pygame.font.SysFont("Courier New", 32, bold=True)
    #fps_display = pygl2d.font.RenderText("", [0, 255, 0], font)
    #pygl2d.draw.init_background([60.,197.,255.,255.])
    print "starting loop..."
    while 1:
        
        #Tick the clock.
        dt = clock.tick(30.0) / 30.0
    
        #Always use change_text to, well, change text ;-)
        #fps_display.change_text(str(int(clock.get_fps())) + " fps")
        #print clock.get_fps()
        #get input
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return
            if e.type == pygame.MOUSEBUTTONDOWN:
                
                if e.button == 1:
                    pos = pygame.mouse.get_pos()
                    cam.Pix2Hex( pos)
                elif e.button == 4 : #Wheel-UP
                    print "Wheel up"
                    cam.zoomIn()
                elif e.button == 5 : #Wheel-down
                    print "Wheel down"
                    cam.zoomOut()
                else:
                    print "click %d" % e.button        
        #move the player
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            cam.moveLeft(dt)
        if key[K_RIGHT]:
            cam.moveRight(dt)
        if key[K_UP]:
           cam.moveUp(dt)
        if key[K_DOWN]:
           cam.moveDown(dt)
        
        if key[K_TAB]:
            print cam.print_dbg()
        
        #######################
        #### BEGIN DRAWING ####
        #######################

        #screen.blit(background, (0,0))
        cam.draw()
        screen.blit(cam.surface, (0,0))

        pygame.display.flip()
        
#run if executed
if __name__ == "__main__":
    # import cProfile, pstats, StringIO
    # pr = cProfile.Profile()
    # pr.enable()
    
    main()
    
    # pr.disable()

    # ps = pstats.Stats(pr).sort_stats('tottime').reverse_order()

    # #ps.print_stats()
    # ps.dump_stats("profile.txt")
    
    #cProfile.run(main())
