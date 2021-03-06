from images import load_image, highlight_surface
import pygame as pg

class Entity(object):
    '''
    An object in the world:
    Can be displayed and selected
    '''
    def __init__(self, surface, position = (0,0), rect =None ,plan = 1, ):
        self.rect = rect if rect!=None else surface.get_rect()
        self.set_surface(surface)
        self.plan = plan # For hierarchy display and selection purpose: the higher the plan number the more on the top it is displayed
        self.position = position
        self.set_position(position)
    
    def tick(self):
        '''
        this method is called every clock tick. Can be overwritten to update
        the object animation.
        '''
        pass
    
    def update(self):
        '''
        This is called in the game loop. Overwrite to update the object 
        behaviour.
        '''
        pass
        
    def handle_event(self, event):
        pass
        
    def set_position(self, position):
        xp, yp = position
        x,y = self.rect.x, self.rect.y
        self.rect.move_ip((xp-x,yp-y))
    
    def get_position(self):
        return self.position
        
    def set_surface(self, surface):
        self.default_surface = surface
        self.surface = surface
        self.highlighted_surface = highlight_surface(surface)
    
    def get_surface(self):
        return self.surface    
    
    def get_rect(self):
        return self.rect
        
    def activate(self):
        self.highlight()
        self.active = True
    
    def deactivate(self):
        self.unhighlight()
        self.active = False
        
    def highlight(self):
        self.surface = self.highlighted_surface
    
    def unhighlight(self):
        self.surface = self.default_surface
     
    def collides(self, position):
        return self.rect.collidepoint(position)


class InputBox(Entity):

    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.color = self.COLOR_INACTIVE
        self.FONT = pg.font.Font(None, 32)
    
        rect = pg.Rect(x, y, w, h)
        txt_surface = self.FONT.render(text, True, self.color)
        super(InputBox, self).__init__(surface = txt_surface,
                                        rect = rect,
                                        position = position, plan = plan
                                        )
    
        self.text = text
        self.active = False

    def activate(self):
        super(InputBox, self).activate()
        self.color = self.COLOR_ACTIVE 
        
    def deactivate(self):
        super(InputBox, self).deactivate()
        self.color = self.COLOR_INACTIVE

    def handle_event(self, event):       
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

                
class ImageEntity(Entity):
    name = None
    extension = 'png'
    
    def __init__(self, position = (0,0), plan = 1, color_key = -1, rect=None):
        surface = load_image(self.name, self.extension, color_key)
        super(ImageEntity, self).__init__(surface = surface,
                                        rect = rect,
                                        position = position, plan = plan
                                        )
        
    def collides(self, position):
        '''
        Select on any visible part 
        '''
        if super(ImageEntity, self).collides(position):
            xc, yc = position
            x0, y0 = self.position
            surface = self.get_surface()
            pix = surface.get_at((int(xc - x0), int(yc-y0)))   
            
            return pix != surface.get_colorkey()
            
        return False

class AnimatedEntity(Entity):
    name = None    
    
    def __init__(self, position = (0,0), 
            plan = 1,color_key = -1, rect=None,
            animation_boundary_condition = 'toric',
            nb_ticks_per_image = 5, surface = None, width = 40):
        '''
        animation_boundary_condition: `toric` or `mirror`    
        nb_ticks_per_image: number of ticks to wait before changing the image
        '''                
        
        
        self.surface_index = 0
        self.tick_counter = 0        
        
        
        if surface == None:
            surface = self.load_animation(width = width)
        
        rect = rect if rect!=None else surface.get_rect()
        rect = pg.Rect(rect.left, rect.top, width, rect.height)
        
        
        super(AnimatedEntity, self).__init__(surface = surface,
                                            rect = rect,
                                            position = position, 
                                            plan = plan
                                        )
        self.animation_boundary_condition = animation_boundary_condition
        self.animation_direction = 1
        self.nb_ticks_per_image = nb_ticks_per_image
    
    
    def get_surface(self):
        return self.surface.subsurface(self.animation_rect)    
    
    def set_next_surface(self):
        if self.animation_boundary_condition == 'toric':
            if self.animation_direction == 1:                
                self.surface_index += 1
                dw = self.width 
                
                if self.surface_index == self.nb_surfaces:
                    self.surface_index = 0
                    dw = -self.width*(self.nb_surfaces-1)
                    
            elif self.animation_direction == -1:
                self.surface_index -= 1
                dw = -self.width 
                
                if self.surface_index < 0:
                    self.surface_index = self.nb_surfaces - 1
                    dw = self.width*(self.nb_surfaces-1)
                
        elif self.animation_boundary_condition == 'mirror':            
            if self.animation_direction == 1:
                self.surface_index += 1
                if self.surface_index == self.nb_surfaces:
                    self.surface_index -= 1
                    self.animation_direction = -1
            else:
                self.surface_index -= 1 
                if self.surface_index <0:
                    self.surface_index += 1
                    self.animation_direction = 1
            dw = self.width*self.animation_direction
        self.animation_rect.move_ip((dw,0))
    
    def load_animation(self, name = None, extension = 'bmp', width = 40, 
        color_key = -1):
        if name == None:
            name = self.name
            
        surface = load_image(self.name, extension, color_key)
        total_width = surface.get_width()
        height = surface.get_height()
        self.nb_surfaces = int(total_width / width)
        
        self.animation_rect = pg.Rect(0,0,width,height)
        self.width = width
        return surface 
                  
    def tick(self):
        self.tick_counter += 1
        if self.tick_counter == self.nb_ticks_per_image:
            self.tick_counter = 0
            self.set_next_surface()
        