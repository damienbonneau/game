import pygame as pg
from point import Point
from math import cos, sin, sqrt, pi, atan2
from pygame import gfxdraw
from pygame import draw

DEG2RAD = pi / 180.

crimson = (196, 28, 23)
crimson_alpha = (196, 28, 23, 250)
crimson_dark = (150, 21, 18)
black = (0,0,0)
grey_dark = (50,50,50)
blue = (0, 50, 168)
blue_dark = (0, 31, 106)


def draw_arc(surface, center, radius, start_angle, stop_angle, color):
    x,y = center
    x = int(x)
    y = int(y)
    radius = int(radius)
    start_angle = int(start_angle%360)
    stop_angle = int(stop_angle%360)
    if start_angle == stop_angle:
        gfxdraw.circle(surface, x, y, radius, color)
    else:
        gfxdraw.arc(surface, x, y, radius, start_angle, stop_angle, color)
    
class Fractal(object):
    
    def __init__(self, radius = 200., draw_from_level = 4):
        r = radius  
        self.surface = pg.Surface((int(4 * r), int(4 * r))).convert_alpha()
        self.surface.fill((255,255,255,0))
        self.draw_from_level = draw_from_level
        self.color = crimson_alpha
        self.gen_fractal(center = (2*r,2*r), angle0 = 90, angle_opening = 220., \
                                            radius = radius, N = 7, rec_num = 5)
        
        
    def gen_fractal(self, center = (0.,0.), angle0 = 0, angle_opening = 220., \
                    radius = 200., N = 2, rec_num = 3):
        r = radius
        x0, y0 = center
        
        start_angle = angle0 - angle_opening / 2
        stop_angle  = angle0 + angle_opening / 2
        
        if rec_num<=self.draw_from_level:
            draw_arc(self.surface, center, radius, start_angle, stop_angle, self.color)
        
        if rec_num == 0:
            return
            
        rec_num = rec_num - 1
        
        da = angle_opening / (N-1)
        
        next_radius = sin(da / 2 * DEG2RAD) * radius
        
        for i in range(N):
            a =  da * i + angle0 - 90.
            new_center = (x0 + r * cos(a * DEG2RAD), y0 + r * sin(a * DEG2RAD))
            self.gen_fractal(new_center, a, angle_opening, next_radius, N, rec_num)
                  
    def get_surface(self):
        return self.surface
        

class Bra():
    def __init__(self):
        r = 200.
        a = 20.
        pattern1 = Fractal(radius = r).get_surface()
        pattern2 = Fractal(radius = r-a).get_surface()
        pattern3 = Fractal(radius = r-2 * a).get_surface()
        pattern4 = Fractal(radius = 40.).get_surface()
        left = pattern1
        left.blit(pattern2, (a ,a))
        # left.blit(pattern3, (r-2*a,r - 2*a))
        # left.blit(pattern4, (250,310))
        
        right = pg.transform.flip(left, True, False)
        width = left.get_width()
        height = left.get_height()
        self.surface = pg.Surface(size = (6 * r,  height)).convert_alpha()
        dr = r / 3
        self.surface.blit(left, (-dr,0))
        self.surface.blit(right, (2 * r + dr, 0 ))
        
    def get_surface(self):
        return self.surface    
    
if __name__ == '__main__':
   
    pg.init()
    screen_sizes = pg.display.list_modes()
    screen_sizes.sort()
    screen_sizes.reverse()
    screen_size = screen_sizes[8]
    print screen_size
    screen = pg.display.set_mode(screen_size)
    

    main_surface = pg.Surface(screen_size)
    background = pg.Surface(main_surface.get_size())
    background = background.convert_alpha()
    background.fill([255,255,255, 255])
    clock = pg.time.Clock()
    
    bra = Bra( )

    while 1:
        
        dt = clock.tick(30.0) / 30.0
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
            if e.type == pg.MOUSEBUTTONDOWN:
                
                if e.button == 1:
                    pass
                elif e.button == 4 : #Wheel-UP
                    print "Wheel up"
                
                elif e.button == 5 : #Wheel-down
                    print "Wheel down"
                else:
                    print "click %d" % e.button       
                
        
        #######################
        #### BEGIN DRAWING ####
        #######################
        main_surface.blit(background, (0,0))
        main_surface.blit(bra.get_surface(), (0,0))
        
        screen.blit(main_surface, (0,0))
        pg.display.flip()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

