import logging  # Import Python's built-in logging module

# Configure logging settings (this should be done ONLY once in the project)
logging.basicConfig(
    filename='app.log',  # Log messages will be saved in this file
    filemode='w',        # 'w' = overwrite file each time program runs
    level=logging.DEBUG, # Capture all logs from DEBUG level and above
    
    # Format of each log message
        # %(asctime)s → Timestamp
        # %(name)s → Logger name (usually "root")
        # %(levelname)s → DEBUG, INFO, etc.
        # %(message)s → Your actual message
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
    # Format of date and time in logs
    datefmt='%Y-%m-%d %H:%M:%S'
)