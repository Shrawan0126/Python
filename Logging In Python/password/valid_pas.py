## Without logging (using print)
# def check_password(password):
#     print("Checking password...")

#     if len(password) < 8:
#         print("Password too short")
#         return False

#     if not any(char.isdigit() for char in password):
#         print("Password must contain a number")
#         return False

#     print("Password is valid")
#     return True


# check_password("abc") 


# Problems here
    # All messages look the same
    # No severity (error? info? who knows)
    # Not saved anywhere
    # Hard to debug in large apps







## Using Logging

import logging

# Configure logging
logging.basicConfig(
    filename='app.log',  # Save logs to file
    filemode= 'a',       # append mode
    level=logging.DEBUG,  # Capture all levels
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_password(password):
    logger.info("Password validation started")

    try:
        # Debug: show received password (in real apps, avoid logging full password!)
        logger.debug(f"Received password: {password}")

        # Check length
        if len(password) < 8:
            logger.warning("Password too short")
            return False

        # Check if contains digit
        if not any(char.isdigit() for char in password):
            logger.warning("Password must contain at least one number")
            return False

        # Check if contains uppercase letter
        if not any(char.isupper() for char in password):
            logger.warning("Password must contain at least one uppercase letter")
            return False

        logger.info("Password is valid")
        return True

    except Exception as e:
        # Catch unexpected errors
        logger.error(f"Error during password validation: {e}")
        return False


# Test cases
check_password("abc")        # too short
check_password("abcdefgh")   # no number, no uppercase
check_password("abcd1234")   # no uppercase
check_password("Abcd1234")   # valid


# Real Insight
# Imagine this in a real app:
    # 1000 users login
    # Some passwords fail

# With logging:
    # You can track how many failures, why failures happen

# With print:
    # Everything is lost once program ends