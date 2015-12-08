from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults
from phue import Bridge

from controller import Controller

APP_ID = "huedump"

class App(CementApp):
    class Meta:
        label = APP_ID
        base_controller = "base"
        handlers = [Controller]
