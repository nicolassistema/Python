import os
import logging
from datetime import datetime
from colorama import Fore, Style, init


def configurar_logger(nombre_base: str = "log_coto"):
    """
    Configura logger con:
    - Archivo rotativo por timestamp
    - Colores en consola
    - Carpeta Log automática
    """

    init(autoreset=True)

    # Crear carpeta Log si no existe
    os.makedirs("Log", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    log_filename = f"{nombre_base}_{timestamp}.log"
    log_path = os.path.join("Log", log_filename)

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            message = record.getMessage()

            if record.levelname == "INFO":
                message = f"{Fore.GREEN}{message}{Style.RESET_ALL}"
            elif record.levelname == "ERROR":
                message = f"{Fore.RED}{message}{Style.RESET_ALL}"

            record.message = message
            return f"{self.formatTime(record)} - {record.levelname} - {record.message}"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 🔥 IMPORTANTE: evitar duplicación de handlers si se llama más de una vez
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler archivo
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Handler consola con color
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger