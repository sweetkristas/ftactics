#!/usr/bin/env python

""" -*- Mode: Python; tab-width: 4 -*-
    
    Dependencies: pyGame http://www.pygame.org
                  json
    
    Run as follows.
    Standalone mode: python ftactics.py
"""

import json
import os
import pygame
from pygame.locals import *
import sys


def load_map(file_name):
    with open(file_name, 'r') as f:
        return json.loads(f.read())
        
class ImageCache(object):
    def __init__(self, image_data_file):
        self.cache = {}
        self.img_cache = {}
        with open(image_data_file, 'r') as f:
            img_data = json.loads(f.read())
            for key, item in img_data.iteritems():
                image_name = item['image']
                if self.img_cache.has_key(image_name):
                    image = self.img_cache[image_name]
                else:
                    image = pygame.image.load(os.path.join('images',image_name)).convert_alpha()
                    self.img_cache[image_name] = image
                x1,y1,x2,y2 = item['area']
                self.cache[key] = image.subsurface((x1,y1,x2-x1,y2-y1))                
    def __getitem__(self, itemname):
        if self.cache.has_key(itemname):
            return self.cache[itemname]
        raise KeyError        

class SortedUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that sorts them by depth."""
    def sprites(self):
        """The list of sprites in the group, sorted by depth."""
        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)
        
class Creature(pygame.sprite.Sprite):
    """Base class for creatures in the game"""
    def __init__(self, name, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = IMAGE_CACHE[name]
        r = self.image.get_rect()
        self.rect = pygame.rect.Rect(r.left, r.top, r.w*2, r.h*2)
        self.depth = 0
    #def _get_pos(self):
    #    return self.rect.mid
    #def _set_pos(self, pos):
    #    self.pos = pos
    #pos = property(_get_pos, _set_pos)

class Game(object):
	"""The main game object"""
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.game_over = False
		self.sprites = SortedUpdates()		
	def main(self):
		fps_clock = pygame.time.Clock()
		self.screen.blit(self.background,(0,0))
		pygame.display.flip()
		while not self.game_over:
			self.sprites.update()
			dirty = self.sprites.draw(self.screen)
			pygame.display.update(dirty)
			fps_clock.tick(60)
			for event in pygame.event.get():
				if event.type == pg.QUIT:
					self.game_over = True
	
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024,768))
    pygame.display.set_caption('Fantasy Tactics Combat Simulator')
    MAPDATA_CACHE = load_map('data/mapdata.cfg')
    IMAGE_CACHE = ImageCache('data/imagedata.cfg')	
	Game().main()
