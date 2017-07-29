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
    