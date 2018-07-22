import os
import pygame

from bot_collections import DictUtil
from bot_math import *
from bot_framework.bot_render import BOTSprite

class AssetUtil:
    def __init__(self):
        raise Exception("AssetUtil should not be initialized.")

    '''
        Loads a sprite sheet matching the format:
        imageSheetName nFrameSets
        (nFrameSets times)
        frameSetName nFrames
        (nFrames times)
        frameId spriteSheetX spriteSheetY width height centerX centerY delay
    '''
    @staticmethod
    def loadSpriteSheet(spritePath):
        result = {}
        fopen = open(spritePath)
        initialLine = fopen.readline().strip().split(" ")
        imgFile = initialLine[0]
        img = pygame.image.load(os.path.dirname(spritePath) + "/" + imgFile)
        nAnims = int(initialLine[1])
        for a in range(nAnims):
            animData = fopen.readline().strip().split(" ")
            animName = animData[0]
            result[animName] = []
            nFrames = int(animData[1])
            for f in range(nFrames):
                data = map(int, fopen.readline().strip().split(" "))
                surfRect = pygame.Rect(*data[1:5])
                delay = data[7]/1000.0
                cx, cy = data[5:7]
                
                # need to get (cx, cy) to be center of image
                newCx, newCy = max(surfRect.w, surfRect.w - cx), max(surfRect.h, surfRect.h - cy)

                newSurf = pygame.Surface((int(newCx*2), int(newCy*2)), pygame.SRCALPHA)
                # now to blit old surf onto new surf 
                ox, oy = int(newCx - cx), int(newCy - cy) # old surf relative to new surf
                newSurf.blit(img.subsurface(surfRect), (ox, oy))

                localRect = pygame.Rect(-cx, cy - surfRect.h, surfRect.w, surfRect.h)
                newFrame = BOTSprite.Frame(newSurf, localRect, delay)
                result[animName].append(newFrame)
        return result

    @staticmethod
    def loadIMG(path):
        return pygame.image.load(path)
