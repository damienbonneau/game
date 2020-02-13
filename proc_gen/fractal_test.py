import pygame as pg
from math import cos, sin, sqrt, pi, atan2
from pygame import gfxdraw
from pygame import draw

DEG2RAD = pi / 180.

crimson = (196, 28, 23)
crimson_alpha = (196, 28, 23, 250)
crimson_dark = (150, 21, 18)
black = (0,0,0, 255)
grey_dark = (50,50,50)
black_transparent = (0,0,0, 150)
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
    
class DisplayObj(object):
    def get_surface(self):
        return self.surface 
    
class Fractal(DisplayObj):
    
    def __init__(self, radius = 200., 
                    draw_from_level = 5, 
                    angle0 = 90, 
                    angle_openings = 220., 
                    N = 7, 
                    rec_num = 5,
                    radius_scaling_coeff = 1.,
                    center_scaling_coeff = 1.,
                    color = black):
        r = radius  
        self.surface = pg.Surface((int(6 * r), int(6 * r))).convert_alpha()
        self.surface.fill((255,255,255,0))
        self.draw_from_level = draw_from_level
        self.color = color
        
        self.gen_fractal(center = (3*r,2*r), angle0 = angle0, 
                                            angle_openings = angle_openings,
                                            radius = radius, 
                                            N = N, 
                                            draw_from_level = draw_from_level,
                                            rec_num = rec_num,
                                            radius_scaling_coeff = radius_scaling_coeff,
                                            center_scaling_coeff = None)
        
       
    def gen_fractal(self, center = (0.,0.), angle0 = 0, angle_openings = 220., \
                    radius = 200., N = 5, rec_num = 4, radius_scaling_coeff = 1.,
                    draw_from_level = 4,
                    center_scaling_coeff = None):
        r = radius
        x0, y0 = center
        
        if type(angle_openings) == type([]):
            angle_opening = angle_openings.pop(0)
        else:
            angle_opening = angle_openings
            
        start_angle = angle0 - angle_opening / 2
        stop_angle  = angle0 + angle_opening / 2
        
        if rec_num<=self.draw_from_level:
            draw_arc(self.surface, center, radius, start_angle, stop_angle, self.color)
        
        if rec_num == 0:
            return
        
            
        rec_num = rec_num - 1
        
        da = angle_opening / (N-1)
        
        next_radius = sin(da / 2 * DEG2RAD) * radius * radius_scaling_coeff
        
        if not center_scaling_coeff:
            center_scaling_coeff = radius_scaling_coeff
        r = r * center_scaling_coeff
        for i in range(N):
            if type(angle_openings) == type([]):
                new_angle_openings = angle_openings[:]
            else:
                new_angle_openings = angle_opening
            a =  da * i + angle0 - 90.
            
            new_center = (x0 + r * cos(a * DEG2RAD), y0 + r * sin(a * DEG2RAD))
            self.gen_fractal(new_center, a, 
                    new_angle_openings, 
                    next_radius, N, rec_num, 
                    radius_scaling_coeff = radius_scaling_coeff)
                  
    def get_surface(self):
        return self.surface


class StripeFineMeshLosange(DisplayObj):
    def __init__(self, w = 1000, h=800, top_edge_thickness = 14, 
                bottom_edge_thickness = 14,
                grid_sep = 8,
                color_mesh = black_transparent,
                color_edge = black ):
        self.surface = pg.Surface( (w, h) ).convert_alpha()
        self.surface.fill((255,255,255,0))
        
        ## Small mesh
        for i in range(-h,w, grid_sep):
            gfxdraw.line(self.surface, i, 0, i+h, h, color_mesh)
            gfxdraw.line(self.surface, i, h, i+h, 0, color_mesh)
        
        ## Edges
        y0 = 0
        y1 = h-bottom_edge_thickness 
        for y, dy in [(y0, top_edge_thickness), (y1, bottom_edge_thickness)]:
            s = pg.Surface((w, dy)).convert_alpha()
            s.fill(color_edge)
            self.surface.blit(s, (0, y))
        
class StripeEdge(DisplayObj):
    def __init__(self, radius = 70., N = 7):
        self.radius = radius
        fractal = self.gen_fractal()
        r = radius
        w,h = fractal.get_width(), fractal.get_height()
        
        self.surface = pg.Surface((int(r * (2*N + 12)), h)).convert_alpha()
        self.surface.fill((255,255,255,0))
        
        for i in range(N):  
            self.surface.blit(fractal, (i * 2*r,0))
        
    def gen_fractal(self):
        return  Fractal(
                    radius = self.radius, 
                    draw_from_level = 4, 
                    angle0 = 90, 
                    angle_openings = 180., 
                    N = 6, 
                    rec_num = 5,
                    color = black).get_surface()
                    
class StripeI(DisplayObj):
    def __init__(self):
        edge = StripeEdge().get_surface()
        
        h_main = 500
        w = edge.get_width()
        h_edge = edge.get_height()
        main = StripeFineMeshLosange(w , h_main, color_edge = (0,0,0,240)).get_surface()
        h = h_edge + h_main
        self.surface = pg.Surface((w, h)).convert_alpha()
        self.surface.fill((255,255,255,255))
        self.surface.blit(edge, (0,0))
        self.surface.blit(main, (0, 250))
        
class Bra(DisplayObj):
    def __init__(self):
        r = 200.
        a = 50.
        pattern1 = Fractal(radius = r, rec_num = 5, 
            angle_openings =[220, 180, 180, 220, 180, 180, 180],
            center_scaling_coeff = 0.85,
            radius_scaling_coeff = 1.,
            N = 6,
            draw_from_level = 4).get_surface()
        
        # pattern2 = Fractal(radius = r, rec_num = 5, 
            # angle_openings =[250, 180, 180, 220, 180, 180, 180],
            # center_scaling_coeff = 0.85,
            # radius_scaling_coeff = 1.,
            # N = 5,
            # draw_from_level = 4).get_surface()
        
        # pattern3 = Fractal(radius = r, rec_num = 2, 
            # angle_openings =[300, 180, 180, 220, 180, 180, 180],
            # center_scaling_coeff = 0.5,
            # radius_scaling_coeff = 1.,
            # angle0 = 70.,
            # N = 15,
            # draw_from_level = 0).get_surface()
        
        # pattern2 = Fractal(radius = r+a, rec_num = 3,
            # angle_openings =[280, 180, 180, 220, 180, 180, 180],
            # center_scaling_coeff = 0.85,
            # draw_from_level = 4,
            # N = 5
            # ).get_surface()
        # pattern3 = Fractal(radius = r-2 * a).get_surface()
        # pattern4 = Fractal(radius = 40.).get_surface()
        left = pattern1
        # left.blit(pattern2, (-2*a ,-a*1.5))
        # left.blit(pattern3, (0,0))
        # left.blit(pattern4, (250,310))
        
        right = pg.transform.flip(left, True, False)
        width = left.get_width()
        height = left.get_height()
        self.surface = pg.Surface(size = (6 * r,  height)).convert_alpha()
        self.surface.fill((255,255,255,255))
        dr = r / 3
        self.surface.blit(left, (-dr,0))
        # self.surface.blit(right, (2 * r + dr, 0 ))
    
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
    
    # surf = Bra().get_surface()
    surf = StripeI().get_surface()

    while 1:
        fps = 10.
        dt = clock.tick(fps) / fps
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
        main_surface.blit(surf, (0,0))
        
        screen.blit(main_surface, (0,0))
        pg.display.flip()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

