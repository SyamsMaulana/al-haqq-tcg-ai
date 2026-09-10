import json
import logging
from pathlib import Path

ASSET_DIR = Path("./assets/narratives")
LOG_FILE = Path("./narrative_pipeline.log")

def setup_logger():
    logger = logging.getLogger("NarrativePipeline")
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

def generate_al_haqq_metadata(asset_name: str, category: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "DigitalDocument",
        "name": asset_name,
        "genre": "Culinary-Cultural Storytelling",
        "creator": {
            "@type": "Person",
            "name": "Syams Maulana (ICAM)",
            "alternateName": "GOD•MauL"
        },
        "collaborator": {
            "@type": "Organization",
            "name": "Collaborative AI Intelligence Engine"
        },
        "copyrightNotice": "Authentic Al-Haqq-Protocol Digital Provenance & Collaborative Core",
        "category": category,
        "license": "https://github.com/SyamsMaulana/Al-Haqq-Protocol"
    }

def process_narrative_assets():
    logger.info("Initializing Narrative & Provenance Pipeline...")
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    assets = [
        {"name": "nasi_goreng_garasi_campaign", "category": "Culinary Production & Pre-Order"},
        {"name": "csr_indonesia_awards_entry", "category": "Cultural Storytelling & CSR"}
    ]
    success_count, error_count = 0, 0
    for item in assets:
        filename = ASSET_DIR / f"{item['name']}_provenance.json"
        metadata = generate_al_haqq_metadata(item['name'], item['category'])
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
            success_count += 1
            logger.info(f"Successfully generated provenance sidecar: {filename.name}")
        except Exception as e:
            error_count += 1
            logger.error(f"Failed to write provenance for {item['name']}: {e}")
    logger.info(f"Pipeline finished. Generated sidecars: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    process_narrative_assets()
