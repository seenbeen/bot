import os
from pattern.bot_singleton import Singleton
from bot_collections import DictUtil
from pygame import image

class AssetManager(object):

    def __init__(self):
        self.assetPath = "../assets/"
        self.ext = {}
        self.assets = {}

    def load(self):
        f = open(os.path.join(self.assetPath, "assetslist"),"r")
        for bpath in f:
            path = bpath.rstrip()
            callback = DictUtil.tryFetch(self.ext, os.path.splitext(path)[1])
            asset = callback(os.path.join(self.assetPath, path))
            DictUtil.tryStrictInsert(self.assets, path, asset)

    def loadCallbacks(self):
        self.loadTypeCallback(".jpg", AssetManager.loadIMG)
        self.loadTypeCallback(".png", AssetManager.loadIMG)

    def loadAsset(self, path):
        return DictUtil.tryFetch(self.assets, path)

    def loadTypeCallback(self, extension, callback):
        DictUtil.tryStrictInsert(self.ext, extension, callback)

    @staticmethod
    def loadIMG(path):
        return image.load(path)

Singleton.transformToSingleton(AssetManager)
