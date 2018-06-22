import os
from pygame import Surface
from util.bot_assetManager import AssetManager

def run():
    AssetManager.initialize()
    AssetManager.instance().assetPath = "assets/"

    AssetManager.instance().loadCallbacks()
    AssetManager.instance().load()

    assert isinstance(AssetManager.instance().loadAsset("tests/test.png"), Surface), "test.png failed to load"
    assert isinstance(AssetManager.instance().loadAsset("tests/test.jpg"), Surface), "test.jpg failed to load"
    assert AssetManager.instance().ext['.jpg'] == AssetManager.instance().ext['.png'], "callbacks failed to load properly"
