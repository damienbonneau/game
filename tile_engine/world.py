
from sortedcollection import SortedCollection

class World(object):
    '''
    Stores all the objects and has methods to access them
    '''
    
    def __init__(self, objects):
        self.objects = {} # plan : list of objects in the plan
        self.plans = []
        for o in objects:
            self.add_object(o)        
     
    def tick(self):
        for l in self.objects.values():
            for entity in l:
                entity.tick()
    
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
            self.plans = list(self.objects.keys())
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
                print (r.x, r.y, r.w, r.h)
            results[plan] = [objects[i] for i in indices]
         
        print (rect.x, rect.y, len(objects))
        sys.stdout.flush()