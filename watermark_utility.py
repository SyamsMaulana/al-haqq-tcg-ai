




# watermark_utility.py - Al-Haqq Protocol Digital Watermark Injector
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def apply_alhaqq_watermark(
    input_image_path, output_image_path, card_id, creator="Syams Maulana (ICAM)"
):
  try:
    img = Image.open(input_image_path).convert("RGBA")
    txt_layer = Image.Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    watermark_text = f"ICAM-AlHaqq-Verified | {card_id} | {creator} | {timestamp}"

    # Draw immutable verification text at the bottom footer of the card asset
    draw.text((20, img.size[1] - 40), watermark_text, fill=(255, 255, 255, 200))

    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
    watermarked.save(output_image_path, "PNG")
    print(f"[SUCCESS] Watermark applied securely: {output_image_path}")
  except Exception as e:
    print(f"[ERROR] Failed to apply watermark protocol: {e}")


if __name__ == "__main__":
  print("Al-Haqq Protocol Watermark Utility Initialized.")


