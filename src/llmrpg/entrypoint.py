from lapinou.scene import Scene

from .scenes.main_menu import MainMenuScene


def get_entrypoint_scene() -> Scene:
    return MainMenuScene()
