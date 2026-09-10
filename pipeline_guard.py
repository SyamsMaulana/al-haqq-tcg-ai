import os
import shutil
import logging
from pathlib import Path

SOURCE_DIR = Path("./assets/images")
BACKUP_DIR = Path("./assets/backup")
LOG_FILE = Path("./automation.log")

def setup_logger():
    logger = logging.getLogger("TermuxPipeline")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def create_backup(file_path: Path, backup_root: Path) -> bool:
    try:
        backup_root.mkdir(parents=True, exist_ok=True)
        dest_path = backup_root / file_path.name
        shutil.copy2(file_path, dest_path)
        logger.info(f"Backup created successfully: {dest_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create backup for {file_path.name}: {e}")
        return False

def process_pipeline():
    logger.info("Initializing Termux automation pipeline...")
    if not SOURCE_DIR.exists():
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    processed_count, error_count = 0, 0
    for file_path in SOURCE_DIR.iterdir():
        if file_path.is_dir():
            continue
        try:
            if file_path.suffix.lower() not in allowed_extensions:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            if not create_backup(file_path, BACKUP_DIR):
                raise RuntimeError(f"Backup failed for {file_path.name}")
            processed_count += 1
            logger.info(f"Successfully processed: {file_path.name}")
        except ValueError as ve:
            error_count += 1
            logger.warning(f"Skipped {file_path.name}: {ve}")
        except Exception as e:
            error_count += 1
            logger.error(f"Error processing {file_path.name}: {e}", exc_info=True)
    logger.info(f"Finished. Processed: {processed_count}, Errors: {error_count}")

if __name__ == "__main__":
    process_pipeline()
