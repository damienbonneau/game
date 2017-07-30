import pygame as pg
from math import pi, cos, sin, atan2,sqrt
import math

class Point():
    def __init__(self,x, y):
        self.x = x
        self.y = y
    
    def __getitem__(self, index):
        if index == 0: return self.x
        if index == 1: return self.y
        raise IndexError("Point type only supports index 0 and 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Point type only supports index 0 and 1")
        return

    def __iter__(self):
        for index in range(2):
            yield self[index]
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return (other != None) and (abs(self[0] - other[0]) < 10e-10) and (
            abs(self[1] - other[1]) < 10e-10)

    def __ne__(self, other):
        return (other == None) or (abs(self[0] - other[0]) > 10e-10) or (
            abs(self[1] - other[1]) > 10e-10)

    def distance(self, other):
        """  the distance to another coordinate """
        return math.sqrt((other[0] - self.x)**2 + (other[1] - self.y)**2)

    def angle_deg(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in degrees """
        return 180.0 / math.pi * self.angle_rad(other)

    def angle_rad(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in radians """
        return math.atan2(self.y - other[1], self.x - other[0])

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)
        
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __abs__(self):
        return math.sqrt(abs(self.x)**2 + abs(self.y)**2)


def lines(s, points, color, width):
    points = [(int(p.x), int(p.y)) for p in points]   
    pg.draw.aalines(s, color, True, points, 1)
    
class DecoratedCircularTile(object):
    nb_sides = 12
    
    def __init__(self, radius = 200. , arc_radius = 60., 
                n_sampling = 80, order = 10,
                color_key = (255, 127, 0)):
        self.color_key = color_key
        self.radius = radius
        self.arc_radius = arc_radius
        self.nb_sampling = n_sampling 
        self.width = self.height = 2 * (self.radius + arc_radius)
        self.dtheta = 2 * pi / self.nb_sides
        self.theta0s = [k*self.dtheta/order for k in range(order)]
        
        
        self.define_points()
        self.gen_surface()
        
    def define_points(self):
        p0 = Point(self.width / 2, self.height / 2)
        N = self.nb_sides
        dtheta = self.dtheta
        R = self.radius
        R2 = self.arc_radius
        
        self.list_points = []
        for theta0 in self.theta0s:
        
            base_points = [p0 + R * Point(cos(dtheta * k + theta0), sin(dtheta * k+theta0)) for k in range(N)]
            
            dx, dy = base_points[1] - base_points[0]
            side = sqrt(dx**2 + dy**2)
            print side
            d = sqrt(R2**2 - (side / 2)**2) / sqrt(2)
            centers_for_arcs = [p0 + (R+d) * Point(cos(a), sin(a)) for a in [ i* dtheta + dtheta/2 + theta0 for i in range(N)]]
            
            # all points:
            start_angles = []
            finish_angles = []
            for i in range(N):
                xc, yc = centers_for_arcs[i]
                xs, ys = base_points[i]
                xf, yf = base_points[(i+1) % N]            
                start_angles += [atan2(ys - yc,xs - xc)]
                finish_angles += [atan2(yf - yc,xf - xc)]

            points = []
            for i in range(N):
                start_angle = start_angles[i]
                finish_angle = finish_angles[i]
                if finish_angle>start_angle:
                    finish_angle -= 2*pi
                center = centers_for_arcs[i]
                dtheta_arc = (finish_angle - start_angle) / (self.nb_sampling)
                for k in range(self.nb_sampling+1):
                    a = start_angle + k *dtheta_arc
                    p = center + R2 * Point( cos(a), sin(a) )
                    points += [p]
                
            self.list_points += [points]
        # self.centers_for_arcs = centers_for_arcs
        # self.base_points = base_points
       
    def gen_surface(self):
        bg_color = (125,125,125)
        color = (0,0,0)
        s = pg.Surface((int(self.width), int(self.height)))
        s.fill(bg_color)
        for points in self.list_points:
            lines(s, points, (0,0,0), 12)
        # lines(s, self.base_points, (0,0,255), 1)
        # lines(s, self.centers_for_arcs, (255,0,0), 1)
        self.surface = s
    
    def get_surface(self):
        return self.surface
    
if __name__ == '__main__':
   
    pg.init()
    screen_sizes = pg.display.list_modes()
    screen_sizes.sort()
    screen_sizes.reverse()
    screen_size = screen_sizes[5]
    screen = pg.display.set_mode(screen_size)
    

    main_surface = pg.Surface(screen_size)
    background = pg.Surface(main_surface.get_size())
    background = background.convert()
    background.fill([60,197,255])
    clock = pg.time.Clock()
    
    tile = DecoratedCircularTile()

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
        main_surface.blit(tile.get_surface(), (0,0))
        screen.blit(main_surface, (0,0))
        pg.display.flip()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

