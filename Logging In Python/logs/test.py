import logging   # Import logging module
import logger    # Import logger.py to apply configuration

# Create a logger specific to this file
logger_obj = logging.getLogger(__name__)

def add(a, b):
    # Log when the addition operation starts
    logger_obj.debug("The addition operation is taking place")
    return a + b

# Log before calling the function
logger_obj.debug("The addition function is called")

add(10, 5)  # Call the function