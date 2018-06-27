import os
from pygame import image
from bot_collections import DictUtil
from pattern.bot_singleton import Singleton

class AssetManager(object):

    def __init__(self):
        self.assetPath = "../assets/"
        self.__ext = {}
        self.__assets = {}

    def load(self, listPath):
        f = open(listPath+".botal","r")
        for bpath in f:
            path = os.path.abspath(os.path.normpath(self.assetPath + bpath.rstrip()))
            if path in self.__assets:
                continue
            callback = DictUtil.tryFetch(self.__ext, os.path.splitext(path)[1])
            asset = callback(path)
            DictUtil.tryStrictInsert(self.__assets, path, asset)

    def loadCallbacks(self):
        self.loadTypeCallback(".jpg", AssetManager.loadIMG)
        self.loadTypeCallback(".png", AssetManager.loadIMG)

    def loadAsset(self, path):
        return DictUtil.tryFetch(self.__assets, os.path.abspath(self.assetPath + os.path.normpath("./"+path)))

    def loadTypeCallback(self, extension, callback):
        DictUtil.tryStrictInsert(self.__ext, extension, callback)

    @staticmethod
    def loadIMG(path):
        return image.load(path)

Singleton.transformToSingleton(AssetManager)

