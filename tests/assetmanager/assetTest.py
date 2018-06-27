import os
from pygame import Surface
from util.bot_assetManager import AssetManager

def run():
    os.system("python scripts/bot_assetLister.py tests/assetmanager/assetsList tests/")
    AssetManager.initialize()
    AssetManager.instance().assetPath = "tests/assetmanager/"

    AssetManager.instance().loadCallbacks()
    AssetManager.instance().load("tests/assetmanager/assetsList")

    assert isinstance(AssetManager.instance().loadAsset("test.png"), Surface), "test.png failed to load"
    assert isinstance(AssetManager.instance().loadAsset("test.jpg"), Surface), "test.jpg failed to load"
    assert isinstance(AssetManager.instance().loadAsset("test.jpg"), Surface), "test.jpg failed to load" #This is actually a duplicate load check
    
