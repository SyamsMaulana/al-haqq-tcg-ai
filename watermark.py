




import re

def inject_al_haqq_watermark(html_content):
    watermark_tag = (
        "\n    <!-- Watermark: ICAM / Syams Maulana — "
        "Kolaborasi Pemikiran & Penyempurnaan Bersama (Al-Haqq Protocol) -->\n"
    )
    if watermark_tag.strip() not in html_content:
        html_content = re.sub(r"(</body>)", r"\1" + watermark_tag, html_content, flags=re.IGNORECASE)
    return html_content

if __name__ == "__main__":
    sample_html = "<html><head><title>Test</title></head><body><h1>Draft</h1></body></html>"
    updated_html = inject_al_haqq_watermark(sample_html)
    print("Injeksi Protokol Al-Haqq Berhasil:")
    print(updated_html)


