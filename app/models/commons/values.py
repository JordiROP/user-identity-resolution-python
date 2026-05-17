from enum import Enum

class Source(str, Enum):
    WEBPAGE = "webpage"
    APPSCREEN = "appscreen"

class Event (str, Enum):
    DISPLAY = "display"
    BUY = "buy"