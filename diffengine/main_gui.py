import pygame as pg
import sys
from camera import Camera

def display_scene(camera, world, surface, background):    
    surface.blit(background, (0,0))
    rect = camera.get_rect()
    objects = world.get_objects_ordered_for_display(rect)
    xc, yc = camera.get_position()
    for o in objects:
        o.draw(surface, xc, yc)
        # xo, yo = o.get_position()
        # surface.blit(o.get_surface(), (xo-xc, yo-yc))
    
     
def main_loop(world, screen, screen_size):
    main_surface = pg.Surface(screen_size)
    background = pg.Surface(main_surface.get_size())
    background = background.convert()
    background.fill([60,197,255])
    clock = pg.time.Clock()
    
    camera = Camera(screen.get_rect())
    font = pg.font.SysFont("Courier New", 32, bold=True)
    hover_object = None
    
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
                    
                    world.active_object = world.select_at(camera.pix_to_position(pg.mouse.get_pos()))
                    world.activate(world.active_object)
                    
                elif e.button == 4 : #Wheel-UP
                    print ("Wheel up")
                
                elif e.button == 5 : #Wheel-down
                    print ("Wheel down")
                else:
                    print ("click %d" % e.button )
            
            if world.active_object:
                world.active_object.handle_event(e)
        
        ## Highlighting the current object
        if hover_object!= None:
            hover_object.unhighlight()
            
        hover_object = world.select_at(camera.pix_to_position(pg.mouse.get_pos()))
        if hover_object!= None:
            hover_object.highlight()
            
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
        
        world.tick()
        
def init_pg():
    pg.init()
    screen_sizes = pg.display.list_modes()
    screen_sizes.sort()
    screen_sizes.reverse()
    screen_size = screen_sizes[5]
    # screen = pg.display.set_mode(screen_size, pg.FULLSCREEN)
    screen = pg.display.set_mode(screen_size)
    pg.display.toggle_fullscreen()
    return screen, screen_size     
    
if __name__ == "__main__":
    '''
    A small example with hexagonal tiles and some units
    '''
    
    from entity import InputBox, ColumnInputBoxes
    from world import World
    screen, screen_size = init_pg() 
    # text_boxes = [InputBox((10, y), 500, 20) for y in [10, 30, 50, 70, 90, 110]]
    
    
    
    world = World()
    text_boxes = [ColumnInputBoxes(activate_callback=world.activate)]
    world.add_objects(text_boxes)
    main_loop(world, screen, screen_size)
        
            
            
            