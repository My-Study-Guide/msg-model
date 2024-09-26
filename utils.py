import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_txt(txt_path):
    # Read input file (update required using api)
    logger.debug("Attempting to read input file 'hello.txt'")
    with open(txt_path, 'r') as file:
        text_input = file.read()
    logger.info(f"Successfully read input file. Text length: {len(text_input)} characters")

    return text_input