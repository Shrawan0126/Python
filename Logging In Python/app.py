import logging  # Import logging module

# Configure the root logging system
logging.basicConfig(
    level=logging.DEBUG,  # Capture all logs from DEBUG and above
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    
    # Handlers define where logs go
    handlers=[
        logging.FileHandler("app1.log"),   # Save logs to file
        logging.StreamHandler()            # Show logs in console
    ]
)

# Create a named logger
logger = logging.getLogger("ArithmeticApp")

def add(a, b):
    result = a + b
    logger.debug(f"Adding {a} + {b} = {result}")  # ✅ correct method
    return result

def subtract(a, b):
    result = a - b
    logger.debug(f"Subtracting {a} - {b} = {result}")
    return result

def multiply(a, b):
    result = a * b
    logger.debug(f"Multiplying {a} * {b} = {result}")
    return result

def divide(a, b):
    try:
        result = a / b
        logger.debug(f"Dividing {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error("Division by zero error")  # Log error properly
        return None

# Call functions
add(2, 7)
subtract(5, 2)
multiply(3, 4)
divide(6, 4)