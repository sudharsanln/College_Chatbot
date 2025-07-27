import os
import zipfile
import fitz  # PyMuPDF
from weasyprint import HTML

# === CONFIG ===
zip_file = r"C:\\Users\\USER\\Downloads\\ilovepdf_split.zip"
extract_to = r"C:\\Users\\USER\\Downloads\\pdf_split"
output_html = r"C:\\Users\\USER\\Downloads\\college_book.html"
output_pdf = r"C:\\Users\\USER\\Downloads\\college_book.zip"

with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

pdf_folder = extract_to

# === Extract and clean text ===
def extract_all_texts(folder):
    content_by_file = []
    for file in sorted(os.listdir(folder), key=lambda x: int(x.split("-")[1].split(".")[0])):
        if file.endswith(".pdf"):
            doc = fitz.open(os.path.join(folder, file))
            text = "\n".join([page.get_text() for page in doc])
            content_by_file.append((file.replace(".pdf", ""), text))
    return content_by_file

# === Convert to styled HTML ===
def build_html(content_by_file):
    html = [
        "<html><head><title>College Book</title><style>",
        "body { font-family: Arial; line-height: 1.6; padding: 40px; }",
        "h1 { color: #1a237e; border-bottom: 2px solid #ccc; }",
        "h2 { color: #3949ab; margin-top: 30px; }",
        "p { margin: 10px 0; }",
        "</style></head><body>"
    ]

    html.append("<h1>Index</h1><ul>")
    for title, _ in content_by_file:
        html.append(f'<li><a href="#{title}">{title}</a></li>')
    html.append("</ul><hr>")

    used_titles = set()
    for title, text in content_by_file:
        clean_title = title.strip().title()
        if clean_title.lower() in used_titles:
            continue
        used_titles.add(clean_title.lower())

        html.append(f'<h1 id="{title}">{clean_title}</h1>')

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if len(line) <= 80 and line.istitle():
                html.append(f"<h2>{line}</h2>")
            elif line.startswith("•") or line.startswith("-"):
                html.append(f"<ul><li>{line.lstrip('•- ').strip()}</li></ul>")
            else:
                html.append(f"<p>{line}</p>")

    html.append("</body></html>")
    return "\n".join(html)

# === Run everything ===
content = extract_all_texts(pdf_folder)
html_data = build_html(content)

# Save HTML
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_data)

# Convert to PDF
HTML(output_html).write_pdf(output_pdf)
print(f"Done! PDF saved to {output_pdf}")
