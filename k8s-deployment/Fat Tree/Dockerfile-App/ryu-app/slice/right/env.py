# Provide centralized environment settings
#
# Feel free to customize all the settings 
# to match the testbed environment

import os

# Center Slice
RIGHT_MIDDLEWARE = str(os.environ['RIGHT_MIDDLEWARE']) + ":8080"
RIGHT_FLOWMOD_ACTIVE = True