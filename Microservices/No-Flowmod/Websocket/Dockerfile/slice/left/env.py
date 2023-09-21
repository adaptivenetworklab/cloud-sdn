# Provide centralized environment settings
#
# Feel free to customize all the settings 
# to match the testbed environment

import os

# LEFT Slice
LEFT_MIDDLEWARE = str(os.environ['LEFT_MIDDLEWARE']) + ":8080"
LEFT_FLOWMOD_ACTIVE = False