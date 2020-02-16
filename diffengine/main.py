import pygame as pg
import sys
from camera import Camera
from logic import Processor, Logger, RandomSource, ShiftRegister, connect, TERMINALS
from entity import InputBox, ProcessorGUI, LoggerGUI, SourceGUI, ShiftRegisterGUI
from world import World

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
    # background.fill([60,197,255])
    background.fill([0,0,0])
    clock = pg.time.Clock()
    
    camera = Camera(screen.get_rect())
    # font = pg.font.SysFont("Courier New", 32, bold=True)
    hover_object = None
    
    pg.key.set_repeat(200, 20)
  
    i_world_tick_divs = 4
    world_tick_divs = [1, 2, 5, 10, 30, 60, 120]
    
    world_tick_incr = 0
    
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
                    
                    active_object = world.select_at(camera.pix_to_position(pg.mouse.get_pos()))
                    world.activate(active_object)
                    
                elif e.button == 4 : #Wheel-UP
                    print ("Wheel up")
                    if i_world_tick_divs>0:
                        i_world_tick_divs -= 1
                
                elif e.button == 5 : #Wheel-down
                    if i_world_tick_divs< len(world_tick_divs) - 1:
                        i_world_tick_divs += 1
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
        
        
        if key[pg.K_PLUS]:
            if i_world_tick_divs>0:
                i_world_tick_divs -= 1
        
        if key[pg.K_MINUS]:
            if i_world_tick_divs< len(world_tick_divs):
                i_world_tick_divs += 1
        
        #######################
        #### BEGIN DRAWING ####
        #######################
        
        display_scene(camera, world, main_surface, background)
        screen.blit(main_surface, (0,0))
        pg.display.flip()
        if world_tick_incr >= world_tick_divs[i_world_tick_divs]:        
            world.tick()
            world_tick_incr = 0
            
            for _terminal in TERMINALS:
                _terminal.tick()
            
        world_tick_incr += 1
        
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
    screen, screen_size = init_pg() 
    
    logger = Logger()
    logger_gui = LoggerGUI(logger=logger)
    
    source = RandomSource()
    source_gui = SourceGUI(source=source, position=(-200, 200))
    
    shift_reg = ShiftRegister(size=16)    
    shift_register_gui = ShiftRegisterGUI(shift_register=shift_reg,
        position=(-180, 200))
    
    processor = Processor()
    world = World()
       
    connect(source, shift_reg)
    connect(shift_reg, processor)
    connect(processor, logger)
    
    processor_gui = ProcessorGUI(processor=processor, activate_callback=world.activate)    
    world.add_objects([source_gui, shift_register_gui, processor_gui, logger_gui])
    main_loop(world, screen, screen_size)
        
            
            
            