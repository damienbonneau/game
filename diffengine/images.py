from cache import memoize
import pygame as pg
import os
IMGDIR = 'tiles'

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
    print ('called load image')
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image