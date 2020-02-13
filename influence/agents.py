FACE_DOWN = 0
FACE_UP = 1

from ..tile_engine.entity import ImageEntity



class DoubleSidedTile(ImageEntity):
    name_image_up = None
    name_image_down = None
    extension = 'png'
    
    def __init__(self, position = (0,0), plan = 4, color_key = -1, rect=None, starting_side = FACE_DOWN):
        self.side = starting_side
        surface_up = load_image(self.name_image_up, self.extension, color_key)
        surface_down = load_image(self.name_image_down, self.extension, color_key)
        
        self.surfaces = {FACE_UP : surface_up, FACE_DOWN: surface_down}
        surface = self.surfaces[starting_side]       
        
        super(DoubleSidedTile, self).__init__(surface = surface,
                                        rect = rect,
                                        position = position, plan = plan
                                        )
    def update(self):
        self.surface = self.surfaces[self.side]
    
    
class Agent(DoubleSidedTile):
    influence = 1
    intrigue = 1
    abilities = []
    tier = 1
    
    name_image_up = None
    name_image_down = None
    
    def __init__(self, position_on_board, starting_side = FACE_DOWN):
        self.side = starting_side
        super(Agent,self).__init__(position = position_on_board. starting_side = starting_side)
        
    def flip(self):
        self.side = not self.side        
        super(Agent, self).update()
                       
        