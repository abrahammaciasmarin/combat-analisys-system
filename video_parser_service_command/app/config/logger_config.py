import logging
from app.config.config_loader import load_config

config = load_config()
logging_config = config["logging"]

def setup_logger():
    logging.basicConfig(
        level=logging_config["level"],
        format=logging_config["format"],
        filename=logging_config["file_path"]
    )