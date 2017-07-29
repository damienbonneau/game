from sortedcollection import SortedCollection
import pygame as pg
import os
IMGDIR = 'tiles'

from functools import wraps
import sys
'''
http://book.pythontips.com/en/latest/function_caching.html
'''
def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper

@memoize    
def highlight_surface(img, a = 40):
    newimg=img.copy().convert()
    newimg.lock()
    colorkey=newimg.get_colorkey()
    rect = newimg.get_rect()
    #print colorkey
    #print "COLORIZE 2"
    for x in range(rect.w):
        for y in range(rect.h):
            pixcolor=newimg.get_at((x,y))
            if pixcolor!=colorkey:
                R=min(pixcolor[0]+a, 255)
                G=min(pixcolor[1]+a, 255)
                B=min(pixcolor[2]+a, 255)
                pixcolor=(R,G,B)
                newimg.set_at((x,y),pixcolor)
    newimg.unlock()
    return newimg    

@memoize
def load_image(name, extension = 'png', colorkey = -1):
    img_path = os.path.join(IMGDIR,'{}.{}'.format(name, extension))
    image = pg.image.load(img_path).convert()
    print 'called load image'
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, colorkey

class Entity(object):
    '''
    An object in the world:
    Can be displayed and selected
    '''
    def __init__(self, surface, position = (0,0), rect =None ,plan = 1, ):
        self.main_surface = surface
        self.highlighted_surface = highlight_surface(surface)
        self.displayed_surface = self.main_surface
        
        self.plan = plan # For hierarchy display and selection purpose: the higher the plan number the more on the top it is displayed
        self.position = position
        self.rect = rect if rect!=None else surface.get_rect()
        self.set_position(position)
        
    def set_position(self, position):
        xp, yp = position
        x,y = self.rect.x, self.rect.y
        self.rect.move_ip((xp-x,yp-y))
    
    def get_position(self):
        return self.position
        
    def get_surface(self):
        return self.displayed_surface    
    
    def get_rect(self):
        return self.rect
        
    def highlight(self):
        self.displayed_surface = self.highlighted_surface
    
    def unhighlight(self):
        self.displayed_surface = self.main_surface
     
    def collides(self, position):
        return self.rect.collidepoint(position)
                
class ImageEntity(Entity):
    name = None
    extension = 'png'
    
    def __init__(self, position = (0,0), plan = 1, color_key = -1, rect=None):
        surface, self.color_key = load_image(self.name, self.extension, color_key)
        super(ImageEntity, self).__init__(surface = surface,
                                        rect = rect,
                                        position = position, 
                                        )
        
    def collides(self, position):
        '''
        Select on any visibly part 
        '''
        if super(ImageEntity, self).collides(position):
            xc, yc = position
            x0, y0 = self.position
            pix = self.get_surface().get_at((int(xc - x0), int(yc-y0)))   
            
            return pix != self.color_key
            
        return False
        
class Hex(ImageEntity):
    name = 'hex'
    extension = 'png'

class World(object):
    '''
    Stores all the objects and has methods to access them
    '''
    
    def __init__(self, objects):
        self.objects = {} # plan : list of objects in the plan
        self.plans = []
        for o in objects:
            self.add_object(o)        
        
    def select_at(self, position):
        plans = self.plans[:]
        plans.reverse()
        for p in plans:
            objects_in_plan = self.objects[p]
            for o in objects_in_plan:
                if o.collides(position):
                    return o
                    
        return None            
            
    def add_object(self,o):
        plan = o.plan
        if plan not in self.objects.keys():
            self.objects[plan] = SortedCollection(key = lambda o: o.position)
            self.plans = self.objects.keys()
            self.plans.sort()
            
        self.objects[plan].insert(o)        
                    
    def get_objects(self, rect):
        '''
        returns all objects within rect
        '''
        results = {}
        for plan in self.objects.keys():
            objects = self.objects[plan]
            all_rects = [o.get_rect() for o in objects]
            indices = rect.collidelistall(all_rects)
            results[plan] = [objects[i] for i in indices]
                    
        return results
        
        
    def get_objects_ordered_for_display(self, rect):    
        objects = self.get_objects(rect)
        results = []
        for p in self.plans:
            results += objects[p]
        return results
    
    def dbg_get_objects(self, rect):
        objects = self.get_objects_ordered_for_display( rect)
        
        results = {}
        for plan in self.objects.keys():
            objects = self.objects[plan]
            all_rects = [o.get_rect() for o in objects]
            indices = rect.collidelistall(all_rects)
            for r in all_rects:
                print r.x, r.y, r.w, r.h
            results[plan] = [objects[i] for i in indices]
         
        print rect.x, rect.y, len(objects)
        sys.stdout.flush()
    
class Camera(object):
    def __init__(self, rect):
        self.rect = rect
        self.camera_speed = 12
    
    def get_rect(self):
        return self.rect
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def __ds__(self, dt):
        return dt*self.camera_speed
        
    def move_up(self,dt):    
        self.rect.move_ip((0,  -self.__ds__(dt)))
    
    def move_down(self,dt):    
        self.rect.move_ip((0, self.__ds__(dt)))
        
    def move_left(self,dt):    
        self.rect.move_ip((-self.__ds__(dt), 0))
    
    def move_right(self,dt):    
        self.rect.move_ip(( self.__ds__(dt), 0))
    
    def pix_to_position(self, pos):
        return [a0 + a for a,a0 in zip(self.get_position(), pos)] 
    
    def reset(self):
        self.rect.move_ip((-self.rect.x, - self.rect.y))
    
      
    
def display_scene(camera, world, surface, background):    
    surface.blit(background, (0,0))
    rect = camera.get_rect()
    objects = world.get_objects_ordered_for_display(rect)
    xc, yc = camera.get_position()
    for o in objects:
        xo, yo = o.get_position()
        surface.blit(o.get_surface(), (xo-xc, yo-yc))
     

def init_pg():
    pg.init()
    screen_sizes = pg.display.list_modes()
    screen_sizes.sort()
    screen_sizes.reverse()
    screen_size = screen_sizes[-1]
    print screen_size
    screen = pg.display.set_mode(screen_size)
    # pg.display.toggle_fullscreen()
    return screen, screen_size
     
def main_loop(world, screen, screen_size):
    
    print "init..."
    
    
    main_surface = pg.Surface(screen_size)
    
    background = pg.Surface(main_surface.get_size())
    background = background.convert()
    background.fill([60,197,255])
    clock = pg.time.Clock()
    
    camera = Camera(screen.get_rect())
    
    font = pg.font.SysFont("Courier New", 32, bold=True)
    
    highlighted_object = None
    
    print "starting loop..."
    while 1:
        
        dt = clock.tick(30.0) / 30.0
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                return
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    return
            if e.type == pg.MOUSEBUTTONDOWN:
                
                if e.button == 1:
                    pos = pg.mouse.get_pos()
                    print camera.pix_to_position( pos)
                elif e.button == 4 : #Wheel-UP
                    print "Wheel up"
                
                elif e.button == 5 : #Wheel-down
                    print "Wheel down"
                    
                else:
                    print "click %d" % e.button       
        
        
        ## Highlighting the current object
        
        if highlighted_object!= None:
            highlighted_object.unhighlight()
            
        highlighted_object = world.select_at(pg.mouse.get_pos())
        if highlighted_object!= None:
            highlighted_object.highlight()
            
        ## Move the camera
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            camera.move_left(dt)
        if key[pg.K_RIGHT]:
            camera.move_right(dt)
        if key[pg.K_UP]:
           camera.move_up(dt)
        if key[pg.K_DOWN]:
           camera.move_down(dt)
        if key[pg.K_SPACE]:
               world.dbg_get_objects(camera.get_rect())
        
        #######################
        #### BEGIN DRAWING ####
        #######################
        
        display_scene(camera, world, main_surface, background)
        
        screen.blit(main_surface, (0,0))

        pg.display.flip()
        
#run if executed
if __name__ == "__main__":
    screen, screen_size = init_pg() 
    hex = Hex()
    N = M = 10
    r = hex.get_rect()
    w, h = r.width, r.height
    hexmap = [Hex(position = (i *w*0.75, (j+ 0.5* (i%2))*h), plan = 1) for i in range(N) for j in range(M)]
    
    world = World(objects = hexmap )
    main_loop(world, screen, screen_size)
        
            
            
            