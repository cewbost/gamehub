import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class GameConfig(AppConfig):
    name = 'game'
    
    def ready(self):
        """This method is called on django setup.
        """
        logger.info('game.ready')
        import game.signals