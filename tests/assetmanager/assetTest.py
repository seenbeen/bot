import os
from pygame import Surface
from util.bot_assetManager import AssetManager

def run():
    listLocation = "tests/assetmanager/assetsList"
    pathLocation = "tests/assetmanager/"
    
    os.system("python scripts/bot_assetLister.py " + listLocation + " " + pathLocation)
    
    AssetManager.initialize()
    AssetManager.instance().assetPath = pathLocation

    AssetManager.instance().loadCallbacks()
    AssetManager.instance().load(listLocation)

    assert isinstance(AssetManager.instance().loadAsset("test.png"), Surface), "test.png failed to load"
    assert isinstance(AssetManager.instance().loadAsset("test.jpg"), Surface), "test.jpg failed to load"
    assert isinstance(AssetManager.instance().loadAsset("assetsubfolder/test2.png"), Surface), "test.jpg failed to load"
    assert isinstance(AssetManager.instance().loadAsset("/////test.jpg"), Surface), "test.jpg failed to load" #This is actually a duplicate load check
    assert isinstance(AssetManager.instance().loadAsset("/../assetmanager/test.jpg"), Surface), "test.jpg failed to load" #checks for dumb syntax

