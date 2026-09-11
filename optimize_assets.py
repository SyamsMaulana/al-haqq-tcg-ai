






import os
from PIL import Image

def convert_to_webp(directory="."):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(root, file)
                webp_path = os.path.splitext(img_path)[0] + ".webp"
                if not os.path.exists(webp_path):
                    try:
                        with Image.open(img_path) as img:
                            img.save(webp_path, "WEBP", quality=80)
                        print(f"[WebP Converted] {webp_path}")
                        count += 1
                    except Exception as e:
                        print(f"[Error] {img_path}: {e}")
    print(f"Total images converted to WebP: {count}")

if __name__ == "__main__":
    convert_to_webp()

