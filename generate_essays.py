import os
import re

# --- CONFIGURATION ---
SOURCE_DIR = "essays_source"  # Put your text/markdown files here
OUTPUT_DIR = "essays"         # This will contain the generated HTML files
TEMPLATE_FILE = "essay_template.html"

# Ensure directories exist
if not os.path.exists(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)
    print(f"Created {SOURCE_DIR} folder. Please place your essay files inside.")
    exit()

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- THE TEMPLATE ---
# We use the styling from your minimal, warm essays.html
with open("essays.html", "r", encoding="utf-8") as f:
    full_html = f.read()
    # Extract the template parts (header and footer)
    # This is a bit brittle, but works for this specific setup
    parts = re.split(r'<!-- CONTENT START -->|<!-- CONTENT END -->', full_html)
    if len(parts) < 3:
        # If markers are missing, create a manual template
        TEMPLATE_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Sky's Thought Hub</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .essay-body { max-width: 750px; margin: 6rem auto 10rem; padding: 0 2rem; }
        .essay-body h1 { font-size: 3.5rem; line-height: 1.1; margin-bottom: 3rem; }
        .meta { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em; color: #8b5e3c; margin-bottom: 2rem; display: block; }
        .prose { font-family: 'Lora', serif; font-size: 1.25rem; line-height: 1.8; color: #1c1c1c; }
        .prose p { margin-bottom: 2rem; }
        .prose h3 { margin: 3rem 0 1.5rem; }
        .back-link { display: inline-block; margin-bottom: 3rem; color: #5e5e5e; text-decoration: none; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; }
    </style>
</head>
<body>
    <div class="nav-container"><nav><a href="../index.html" class="logo">SKY.LOG</a></nav></div>
    <main><article class="essay-body"><a href="../index.html" class="back-link">&larr; Back to Home</a>
    <span class="meta">{{DATE}} | Perspective</span>
    <h1>{{TITLE}}</h1>
    <div class="prose">{{CONTENT}}</div></article></main>
    <footer><p>&copy; 2026 Sky. All rights reserved.</p></footer>
</body></html>"""
    else:
        # Use existing page as template
        TEMPLATE_CONTENT = parts[0] + "{{CONTENT}}" + parts[2]

# --- THE REGENERATOR ---
def markdown_to_html(text):
    # Very basic parser for paragraphs and headers if no library
    lines = text.split('\n')
    html = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_paragraph:
                html.append("</p>")
                in_paragraph = False
            continue
        
        if line.startswith('### '):
            if in_paragraph: html.append("</p>"); in_paragraph = False
            html.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith('## '):
            if in_paragraph: html.append("</p>"); in_paragraph = False
            html.append(f"<h2>{line[3:]}</h2>")
        else:
            if not in_paragraph:
                html.append("<p>")
                in_paragraph = True
            html.append(line)
            
    if in_paragraph:
        html.append("</p>")
        
    return "\n".join(html)

def process_essays():
    links = []
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            with open(os.path.join(SOURCE_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
            
            title = filename.rsplit('.', 1)[0].replace('-', ' ').title()
            slug = filename.rsplit('.', 1)[0].lower().replace(' ', '-') + ".html"
            
            html_content = markdown_to_html(content)
            
            final_page = TEMPLATE_CONTENT.replace("{{TITLE}}", title)
            final_page = final_page.replace("{{CONTENT}}", html_content)
            final_page = final_page.replace("{{DATE}}", "2026") # Or extract from filename/file date
            
            with open(os.path.join(OUTPUT_DIR, slug), "w", encoding="utf-8") as f:
                f.write(final_page)
            
            links.append((title, f"essays/{slug}"))
            print(f"Generated: {slug}")

    # Now update index.html 'The Hub' area?
    # (Optional, but very helpful)
    print("\nExtraction complete. You can now link these in your index.html.")

if __name__ == "__main__":
    process_essays()
