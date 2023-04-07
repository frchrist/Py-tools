import functools
import logging
import sys



# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler to write log messages to the console
console_handler = logging.StreamHandler(sys.stdout)


console_handler.setLevel(logging.DEBUG)

console_handler.setFormatter(formatter)

# Add the console handler to the logger object
logger.addHandler(console_handler)

# If we are in production, also add a file handler to write log messages to a file
if not __debug__:
    file_handler = logging.FileHandler('logging.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log(message, logger=logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a logger object for the function

            # Log the message before calling the function
            logger.info(message)

            # Call the function and log its execution
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} returned {result}")
            # Return the result
            return result
        return wrapper
    return decorator
