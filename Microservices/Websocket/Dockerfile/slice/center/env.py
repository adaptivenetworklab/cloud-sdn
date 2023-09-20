# Provide centralized environment settings
#
# Feel free to customize all the settings 
# to match the testbed environment

import os

# Center Slice
CENTER_MIDDLEWARE = str(os.environ['CENTER_MIDDLEWARE']) + ":8080"
CENTER_FLOWMOD_ACTIVE = True