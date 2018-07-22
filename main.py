import pygame._view #required for py2exe
from bot_framework.bot_GOSS import GameApplication
from app.app import BOTGameApp

# hmm... this is surprisingly clean .-.
GameApplication.initialize(BOTGameApp)
GameApplication.instance().run()
GameApplication.shutdown()
