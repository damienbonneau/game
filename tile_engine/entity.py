from images import load_image, highlight_surface

class Entity(object):
    '''
    An object in the world:
    Can be displayed and selected
    '''
    def __init__(self, surface, position = (0,0), rect =None ,plan = 1, ):
        self.main_surface = surface
        self.surface = self.main_surface
        
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
        return self.surface    
    
    def get_rect(self):
        return self.rect
        
    def highlight(self):
        self.surface = highlight_surface(self.surface)
    
    def unhighlight(self):
        self.surface = self.main_surface
     
    def collides(self, position):
        return self.rect.collidepoint(position)
                
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
        Select on any visibly part 
        '''
        if super(ImageEntity, self).collides(position):
            xc, yc = position
            x0, y0 = self.position
            surface = self.get_surface()
            pix = surface.get_at((int(xc - x0), int(yc-y0)))   
            
            return pix != surface.get_colorkey()
            
        return False

 
        
class Hex(ImageEntity):
    name = 'hex'
    extension = 'png'
    
class Tank(ImageEntity):
    name = 'tank'
    extension = 'bmp'    