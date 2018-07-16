import os
from pygame import Surface
from bot_framework.bot_assetManager import AssetManager
from util.bot_asset_util import AssetUtil

def run():
    listFile = "tests/assetmanager/assetsList"
    pathLocation = "tests/assetmanager/"
    
    os.system("python scripts/bot_assetLister.py " + listFile + " " + pathLocation)
    
    AssetManager.initialize(pathLocation)
    assetManager = AssetManager.instance()
    assetManager.loadTypeCallback(".jpg", AssetUtil.loadIMG)
    assetManager.loadTypeCallback(".png", AssetUtil.loadIMG)

    AssetManager.instance().load(listFile)

    assert isinstance(assetManager.loadAsset("test.png"), Surface), "test.png failed to load"
    assert isinstance(assetManager.loadAsset("test.jpg"), Surface), "test.jpg failed to load"
    assert isinstance(assetManager.loadAsset("assetsubfolder/test2.png"), Surface), "test.jpg failed to load"
    assert isinstance(assetManager.loadAsset("/////test.jpg"), Surface), "test.jpg failed to load" #This is actually a duplicate load check
    assert isinstance(assetManager.loadAsset("/../assetmanager/test.jpg"), Surface), "test.jpg failed to load" #checks for dumb syntax

