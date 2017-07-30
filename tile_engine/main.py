import pygame as pg
import sys
from camera import Camera

def display_scene(camera, world, surface, background):    
    surface.blit(background, (0,0))
    rect = camera.get_rect()
    objects = world.get_objects_ordered_for_display(rect)
    xc, yc = camera.get_position()
    for o in objects:
        xo, yo = o.get_position()
        surface.blit(o.get_surface(), (xo-xc, yo-yc))
    
     
def main_loop(world, screen, screen_size):
    main_surface = pg.Surface(screen_size)
    background = pg.Surface(main_surface.get_size())
    background = background.convert()
    background.fill([60,197,255])
    clock = pg.time.Clock()
    
    camera = Camera(screen.get_rect())
    font = pg.font.SysFont("Courier New", 32, bold=True)
    highlighted_object = None
    
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
            
        highlighted_object = world.select_at(camera.pix_to_position(pg.mouse.get_pos()))
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
        
def init_pg():
    pg.init()
    screen_sizes = pg.display.list_modes()
    screen_sizes.sort()
    screen_sizes.reverse()
    screen_size = screen_sizes[5]
    screen = pg.display.set_mode(screen_size, pg.FULLSCREEN)
    pg.display.toggle_fullscreen()
    return screen, screen_size     
    
if __name__ == "__main__":
    '''
    A small example with hexagonal tiles and some units
    '''
    
    from entity import Hex, Tank
    from world import World
    screen, screen_size = init_pg() 
    hex = Hex()
    N = M = 40
    r = hex.get_rect()
    w, h = r.width, r.height
    hexmap = [Hex(position = (i *w*0.75, (j+ 0.5* (i%2))*h), plan = 1) for i in range(N) for j in range(M)]
    
    tanks = [Tank(
    position = (i *w*0.75 + 10, (j+ 0.5* (i%2))*h- 10), plan = 2) for i,j in [(4,6),(1,1), (2,3)]
    ]
    
    world = World(objects = hexmap + tanks )
    main_loop(world, screen, screen_size)
        
            
            
            