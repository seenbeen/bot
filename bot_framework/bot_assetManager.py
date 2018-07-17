import os
from util.bot_collections import DictUtil
from util.pattern.bot_singleton import Singleton

class AssetManager(object):

    def __init__(self, assetPath="../assets/"):
        self.assetPath = assetPath
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

    def loadAsset(self, path):
        return DictUtil.tryFetch(self.__assets, os.path.abspath(self.assetPath + os.path.normpath("./"+path)))

    def loadTypeCallback(self, extension, callback):
        DictUtil.tryStrictInsert(self.__ext, extension, callback)

Singleton.transformToSingleton(AssetManager)

