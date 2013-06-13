# Twitter settings
CONSUMER_KEY = "your consumer key"
CONSUMER_SECRET = "your consumer secret"
ACCESS_KEY = "your acces key"
ACCESS_SECRET = "your access secret"
TRACK = ["what", "you want", "to", "track"]
SCREEN_NAME = "yourtwitterid"

# Log file
LOG = "twitterbox.log"
DEBUG = False

# Messages to display
MSG_FILE = "messages.txt"
SLIDE_TIME = 5 # seconds for each slide and non-alert message

# Directory to pull slides from
# Slides should be 1024 by 768 image files
# Set to None for no slides
SLIDE_DIR = None

# Camera attached?
CAMERA = True

# Video output
FONT = "Droid Sans Mono"
FONT_SIZE = 60
FONT_COLOR = "red"
BACKGROUND_COLOR = "black"
# a filename to use as a background for the text messages
BACKGROUND_IMAGE = None

SERVER_PORT = 80

# Where did you plug in the light?
LIGHT_PIN_1 = 22
LIGHT_PIN_2 = 23 # set to None if there is only one light
LIGHT_RUN_TIME = 10 # seconds to keep the light on
ALERT_DISPLAY_TIME = 10 # seconds to keep the alert message on screen
TEXT_EFFECT = 'blink' # or 'type'

LIGHT_BLINK_DELAY = 0.2 # seconds. Set to 0 for solid on (no blink)

# Priority queue priorities
PRIORITY_LOW = 10
PRIORITY_HIGH = 1

FAKE_TWEET = "@%s: Check out this cool twitter box!" % SCREEN_NAME


import os, sys
sys.path.append(os.environ['HOME'])
sys.path.append('/home/pi')
# Now get the local settings
from local_settings import *
