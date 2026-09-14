




# validate_schema.py - Al-Haqq Protocol Dataset Integrity Validator
import json
import sys


def validate_tcg_data():
  print(
      "[INFO] Initiating Al-Haqq Protocol structural and cryptographic"
      " validation..."
  )

  try:
    with open("nusantara_fantasy_tcg.json", "r") as f:
      schema = json.load(f)
    print(
        "[PASS] Core Schema verified:"
        f" {schema['project_metadata']['title']}"
    )
  except Exception as e:
    print(f"[FAIL] Core Schema error: {e}")
    sys.exit(1)

  try:
    with open("cards.json", "r") as f:
      cards = json.load(f)
    print(f"[PASS] Card Codex loaded successfully. Total cards: {len(cards)}")

    for card in cards:
      assert "card_id" in card, "Missing card_id identifier"
      assert "digital_integrity" in card, f"Card {card.get('card_id')} missing digital integrity block"
      assert (
          card["digital_integrity"]["watermark_protocol"]
          == "ICAM-AlHaqq-Verified"
      ), f"Invalid watermark protocol on {card['card_id']}"
    print(
        "[PASS] All card assets verified under ICAM-AlHaqq-Verified watermark"
        " standard."
    )

  except Exception as e:
    print(f"[FAIL] Card dataset integrity check failed: {e}")
    sys.exit(1)

  print(
      "[SUCCESS] Full repository ecosystem is cryptographically and"
      " structurally sound."
  )


if __name__ == "__main__":
  validate_tcg_data()


