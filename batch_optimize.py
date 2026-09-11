

import os
import re

def optimize_html_files():
    watermark_tag = (
        "\n    <!-- Watermark: ICAM / Syams Maulana — "
        "Kolaborasi Pemikiran & Penyempurnaan Bersama (Al-Haqq Protocol) -->\n"
    )
    
    schema_tag = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Syams Maulana - Culinary & Cultural Storytelling",
      "url": "https://syams-alhaqq.blogspot.com",
      "author": {
        "@type": "Person",
        "name": "Syams Maulana",
        "alternateName": "ICAM"
      }
    }
    </script>
    """

    count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                modified = False
                
                # Inject Schema into head if missing
                if "application/ld+json" not in content and "</head>" in content:
                    content = content.replace("</head>", schema_tag + "\n</head>")
                    modified = True

                # Inject Watermark before body close if missing
                if watermark_tag.strip() not in content and "</body>" in content:
                    content = re.sub(r"(</body>)", r"\1" + watermark_tag, content, flags=re.IGNORECASE)
                    modified = True

                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"[Optimized] {filepath}")
                    count += 1

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    optimize_html_files()

