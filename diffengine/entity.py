from images import load_image, highlight_surface
import pygame as pg

import sys

def _print(*a, **kw):
    print(*a, **kw)
    sys.stdout.flush()

import logic as lg    

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
        
        # To cycle between objects
        self.prev_entity = None
        self.next_entity = None
    
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
    
    def select(self, position):
        return self
    
    def draw(self, surface, x, y):
        _x, _y = self.position
        surface.blit(self.get_surface(), (_x-x, _y-y))
    

def union_rects(rects):
    xsmin = [_r.x for _r in rects]
    xsmax = [_r.x + _r.width for _r in rects]
    ysmin = [_r.y for _r in rects]
    ysmax = [_r.y + _r.height for _r in rects]
    
    ymin = min(ysmin)
    ymax = max(ysmax)
    xmin = min(xsmin)
    xmax = max(xsmax)
    w = xmax - xmin
    h = ymax - ymin
    
    return pg.Rect(xmin, ymin, w, h)
    

class Container(object):
    '''
    An object in the world:
    Can be displayed and selected
    '''
    def __init__(self, entities=[], position = (0,0) ,plan = 1 ):
        self.entities = entities
        self.rect = union_rects([e.rect for e in entities])
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
        for o in self.entities:
            o.handle_event(event)
        
    def set_position(self, position):
        xp, yp = position
        x,y = self.rect.x, self.rect.y
        self.rect.move_ip((xp-x,yp-y))
        
    def get_position(self):
        return self.position
        
    def get_rect(self):
        return self.rect
     
    def collides(self, position):
        return self.rect.collidepoint(position)
    
    def select(self, position):
        for o in self.entities:
            if o.collides(position):
                return o
    
    def draw(self, surface, x, y):
        for o in self.entities:
            _x, _y = o.get_position()
            surface.blit(o.get_surface(), (_x-x, _y-y))
       
class RegisterGUI(Entity):
    def __init__(self,  position, size=16, h=20, w=20):
        self.COLOR_BCKGND = pg.Color('black')
        self.COLOR_SPACER = pg.Color('gray21')
        self.COLOR_BORDER = pg.Color('gray66')
        self.COLOR_DIGIT = pg.Color('gray66')
        self.surface = pg.Surface((w * size, h))
        self.bbrect = pg.Rect(0, 0, w * size, h)
        self.FONT = pg.font.Font(pg.font.match_font("couriernew"), 16, bold=True)
        self.w = w
        self.h = h
        self.size = size
        self.digits_to_surf = {i :self.FONT.render(f"{i}", True, self.COLOR_DIGIT) for i in [0, 1]}
        self.init_surface()
        self.digits = [0] * 16
        super(RegisterGUI, self).__init__(surface=self.surface, position=position)

    def init_surface(self):
        self.surface.fill(self.COLOR_BCKGND)
        w = self.w
        h = self.h
        for i in range(self.size):
            _rect = pg.Rect(i * w, 0, w, h)
            pg.draw.rect(self.surface, self.COLOR_SPACER, _rect, 1)
            
        pg.draw.rect(self.surface, self.COLOR_BORDER, self.bbrect, 3)
    
    def set_digit(self, i, digit):
        self.digits[n - 1 - i] = digit
        self.update_surface()
        
    def set_digits(self, list_digits):
        _digits = list_digits[:]
        _digits.reverse()
        self.digits = _digits
        self.update_surface()
        
    def update_surface(self):
        self.init_surface()
        
        for i,d in enumerate(self.digits):
            self.surface.blit(self.digits_to_surf[d], (self.w*i+ 2, 1))     
    
    def activate(self):
        pass
    
    def deactivate(self):
        pass
        
COLOR_BORDER_EXEC = pg.Color('cyan')
COLOR_BORDER_ERROR_INACTIVE = pg.Color('darkred')
COLOR_BORDER_ERROR_ACTIVE = pg.Color('red')
COLOR_INACTIVE = pg.Color('darkgreen')
COLOR_ACTIVE = pg.Color('green')
COLOR_BORDER_INACTIVE = pg.Color('gray21')
COLOR_BORDER_ACTIVE = pg.Color('gray66')
        
class InputBox(Entity):
    def __init__(self, position, w, h, text='', plan=1, max_length_text=12, line_index=0):
        
        self.active_status = 0 # 1 for acti
        self.syntax_status = 0 # 0 OK, 1 ERROR
        
        self.color_borders_error = [COLOR_BORDER_ERROR_INACTIVE, COLOR_BORDER_ERROR_ACTIVE]
        self.color_borders_ok = [COLOR_BORDER_INACTIVE, COLOR_BORDER_ACTIVE]
        self.color_borders_exec = [COLOR_BORDER_EXEC, COLOR_BORDER_EXEC]
        
        self.color_borders = self.color_borders_ok
        
        self.text_colors = [COLOR_INACTIVE, COLOR_ACTIVE]
        
        self.color = COLOR_INACTIVE
        self.FONT = pg.font.Font(pg.font.match_font("consolas"), 12)
        self.max_length_text = max_length_text
        self.line_index = line_index        rect = pg.Rect(0, 0, w, h)
        self.bbrect = pg.Rect(0, 0, w, h)
        self.txt_surface = self.FONT.render(text, True, self.color)
        surface = pg.Surface((w, h))
        
        # Callbacks
        self.set_text_callback = lambda _inputbox : None
        self.activate_callback = lambda _inputbox : None
        
        super(InputBox, self).__init__(surface = surface,
                                        rect = rect,
                                        position = position, plan = plan
                                        )
    
        self.text = text
        self.active = False
        self.update_surface()
        
        

    def activate(self):
        super(InputBox, self).activate()
        self.active_status = 1       
        self.update_surface()
        
    def deactivate(self):
        super(InputBox, self).deactivate()
        self.active_status = 0
        self.update_surface()
        
    def set_status_exec(self):
        self.color_borders = self.color_borders_exec
        self.update_surface()
        
    def unset_status_exec(self):
        self.color_borders = self.color_borders_error if self.syntax_status else self.color_borders_ok
        self.update_surface()
        
    def set_status_invalid_syntax(self):
        self.syntax_status = 1
        self.color_borders = self.color_borders_error
        self.update_surface()
    
    def set_status_valid_syntax(self):
        self.syntax_status = 0
        self.color_borders = self.color_borders_ok
        self.update_surface()

    def handle_event(self, event):       
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN or event.key == pg.K_TAB:
                    if pg.key.get_pressed()[pg.K_LSHIFT] or pg.key.get_pressed()[pg.K_RSHIFT]:
                        if self.prev_entity is not None:
                            self.deactivate()
                            self.activate_callback(self.prev_entity)
                    
                    elif self.next_entity is not None:
                        self.deactivate()
                        self.activate_callback(self.next_entity)
                        
                    
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_length_text:
                        self.text += event.unicode
                        
                self.text = self.text.upper()
                self.set_text_callback(self)  
                self.update_surface()
    
    def set_text(self, text):
        self.text = text
        self.set_text_callback(self)
        self.update_surface()

    def update_surface(self):
        surface = pg.Surface((self.rect.width, self.rect.height))
        self.txt_surface = self.FONT.render(self.text, True, self.text_colors[self.active_status])  
        surface.blit(self.txt_surface, (5, 5))
        pg.draw.rect(surface, self.color_borders[self.active_status], self.bbrect, 1)
        self.set_surface(surface)
        
    def update(self):
        pass
        
class LoggerGUI(Entity):
    def __init__(self, logger, display_block_size=8, position=(200, 200), w=384, h = 200):
        self.FONT = pg.font.Font(pg.font.match_font("consolas"), 12)
        self.surface = pg.Surface((w, h))
        self.display_block_size = display_block_size
        
        super(LoggerGUI, self).__init__(surface=self.surface, position=position)
        self.COLOR_BCKGND = (20, 20, 20)
        self.COLOR_DIGIT = pg.Color('cyan')
        self.bbrect = pg.Rect(0,0, w, h)
        
        self.digits_to_surf = {i :self.FONT.render(f"{i}", True, self.COLOR_DIGIT) for i in [0, 1]}
        self.logger = logger
        self.update_surface()
        
    def update_surface(self):
        self.surface.fill(self.COLOR_BCKGND)
        pg.draw.rect(self.surface, COLOR_BORDER_INACTIVE, self.bbrect, 1)
        
        cw = 10
        ch = 20
        n_cols = 20
        n_lines = 10
        i = 0
        j = 0
        _blk_size = 0
        for d in self.logger.log:
            self.surface.blit(self.digits_to_surf[d], (cw * i + 2, ch * j + 2 ))
            _blk_size += 1
            i += 1
            if _blk_size == self.display_block_size:
                i += 1
                _blk_size = 0
                
            if i >= 27:
                i = 0
                j += 1
    
    def tick(self):
        self.logger.tick()
        if self.logger.received:
            self.update_surface()
    
    def highlight(self):
        pass
        
    def unhighlight(self):
        pass
        
class ShiftRegisterGUI(Entity):
    def __init__(self, shift_register, position=(-100, 200), h=20):
        self.FONT = pg.font.Font(pg.font.match_font("consolas"), 12)
        cw = 10
        self.shift_register = shift_register
        self.cw = cw
        w = self.shift_register.size * cw
        self.surface = pg.Surface((w, h))
        super(ShiftRegisterGUI, self).__init__(surface=self.surface, position=position)
        self.COLOR_BCKGND = (20, 20, 20)
        self.COLOR_DIGIT = pg.Color('cyan')
        self.bbrect = pg.Rect(0,0, w, h)
        
        self.digits_to_surf = {i :self.FONT.render(f"{i}", True, self.COLOR_DIGIT) for i in [0, 1]}
        self.update_surface()
        
    def update_surface(self):
        self.surface.fill(self.COLOR_BCKGND)
        pg.draw.rect(self.surface, COLOR_BORDER_INACTIVE, self.bbrect, 1)
        
        cw = 10
        ch = 20
        n_cols = 20
        n_lines = 10
        i = 0
        j = 0
        _blk_size = 0
        for d in self.shift_register.buffer:
            if d != None:
                self.surface.blit(self.digits_to_surf[d], (cw * i + 2, ch * j + 2 ))
            i += 1
            
    def tick(self):
        self.shift_register.tick()
        self.update_surface()
    
    def highlight(self):
        pass
        
    def unhighlight(self):
        pass
        
COLOR_CYAN = pg.Color('cyan')
class SourceGUI(Entity):
    def __init__(self, source, position=(-200, 200), w = 20, h=20):
        self.FONT = pg.font.Font(pg.font.match_font("consolas"), 12)
        self.surface = pg.Surface((w, h))
        super(SourceGUI, self).__init__(surface=self.surface, position=position)
        self.COLOR_BCKGND = (20, 20, 20)
        
        self.bbrect = pg.Rect(0,0, w, h)
        
        self.sym_to_surf = {i :self.FONT.render(f"{i}", True, COLOR_CYAN) for i in [0, 1, 'S']}
        self.source = source
        self.update_surface()
        
    def update_surface(self):
        self.surface.fill(self.COLOR_BCKGND)
        pg.draw.rect(self.surface, COLOR_CYAN, self.bbrect, 4)
        self.surface.blit(self.sym_to_surf['S'], (5, 5 ))
            
    def tick(self):
        self.source.tick()
    
    def highlight(self):
        pass
        
    def unhighlight(self):
        pass
    
        
class ProcessorGUI(Container):
    def __init__(
        self, 
        processor, 
        position=(50, 100), 
        w=120, 
        h=20, 
        plan = 1,
        activate_callback=lambda widget: None
    ):
        x, y = position
        self.processor = processor
        n_lines = processor.program_stack_size
        prog_lines = [InputBox((x, y + i * h), w, h, line_index=i) for i in range(n_lines)]
        
        for _inputbox in prog_lines:
            def set_text_callback(inputbox):
                text = inputbox.text
                i = inputbox.line_index
                line_status = self.processor.check_instruction_syntax(text)
                _print(text, i, line_status)
                self.processor.set_prog_line(i, text)
                if line_status != lg.VALID_SYNTAX:
                    inputbox.set_status_invalid_syntax()
                else:
                    inputbox.set_status_valid_syntax()
            _inputbox.set_text_callback = set_text_callback
            
            
        self.lines = prog_lines
        self.current_line = self.lines[self.processor.stack_pointer]
        self.set_program(self.processor.program)
        self.register_gui = RegisterGUI(size = processor.register_size, position=(x, y - 20))
        self.register_gui.set_digits(self.processor.register)
        
        entities = prog_lines + [self.register_gui]
        super(ProcessorGUI, self).__init__(entities=entities, position=position, plan=plan)
        
        for e in self.entities:
            e.activate_callback = activate_callback
            
        for e1, e2 in zip(self.lines, [self.lines[-1]] + self.lines[:-1]):
            e1.prev_entity = e2
            e2.next_entity = e1
            
    def update(self):
        pass
            
    def tick(self):
        self.current_line.unset_status_exec()
        self.processor.tick()
        self.current_line = self.lines[self.processor.stack_pointer]
        self.current_line.set_status_exec()
        
        self.register_gui.set_digits(self.processor.register)
        
    def set_program(self, list_lines):
        for l, text in zip(self.lines, list_lines):
            l.set_text(text)
            
    def get_program(self):
        return [l.text for l in self.lines]
    

