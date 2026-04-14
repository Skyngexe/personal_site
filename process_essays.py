import os
import re

titles = [
    'Preface', 'Breakfast Ritual', 'Gifted polymorphism', 'Coffee break', 
    'Dissolution', 'Weight or lightness', 'Relationships', 'Tampering', 'Typhoon', 
    'Originality, authenticity and self-identity', 
    'Fantasy of my own funeral', 'Mr Nimbus and Roger', 'Fake tattoo', 'Til then', 
    'Chaos and comfort', 'English Proficiency as a class indicator', 'Pool in the city', 
    'Endurance running is an abusive self-masturbatory act', 'The optimal distance of one another', 
    'The last semester, there goes my training wheels', 'Form over functionality', 
    'The anatomy of pretentious culture', 'Attention is all we need', 'Vitiligo', 
    'We should be freakier', 'La Vache', 'Rain', 'Maxxing', 'The Art of Living'
]

# Auto-assigned categories for each title (fallback to 'Misc')
CATEGORY_MAP = {
    'Preface': 'Personal / Identity',
    'Breakfast Ritual': 'Rituals & Everyday',
    'Gifted polymorphism': 'Personal / Identity',
    'Coffee break': 'Rituals & Everyday',
    'Dissolution': 'Philosophy & Reflection',
    'Weight or lightness': 'Philosophy & Reflection',
    'Relationships': 'Relationships',
    'Tampering': 'Culture & Society',
    'Typhoon': 'Place & Weather',
    'Originality, authenticity and self-identity': 'Identity & Self',
    'Fantasy of my own funeral': 'Philosophy & Reflection',
    'Mr Nimbus and Roger': 'Identity & Self',
    'Fake tattoo': 'Identity & Self',
    'Til then': 'Relationships',
    'Chaos and comfort': 'Art of Living & Misc',
    'English Proficiency as a class indicator': 'AI & Technology',
    'Pool in the city': 'Place & Weather',
    'Endurance running is an abusive self-masturbatory act': 'Rituals & Everyday',
    'The optimal distance of one another': 'Relationships',
    'The last semester, there goes my training wheels': 'Relationships',
    'Form over functionality': 'Art of Living & Misc',
    'The anatomy of pretentious culture': 'AI & Technology',
    'Attention is all we need': 'AI & Technology',
    'Vitiligo': 'Art of Living & Misc',
    'We should be freakier': 'Art of Living & Misc',
    'La Vache': 'Art of Living & Misc',
    'Rain': 'Place & Weather',
    'Maxxing': 'Culture & Society',
    'The Art of Living': 'Art of Living & Misc'
}
if not os.path.exists('essays.md'):
    print("essays.md not found.")
    exit()

with open('essays.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to find titles on standalone lines
pattern = '|'.join([re.escape(t) for t in titles])
# Using a lookahead to split and keep the title
segments = re.split(f'^({pattern})$', text, flags=re.MULTILINE)

# The result of re.split is [text_before, title1, content1, title2, content2, ...]
essays = []
if segments[0].strip():
    essays.append(('Untitled', segments[0]))

for i in range(1, len(segments), 2):
    title = segments[i]
    content = segments[i+1] if i+1 < len(segments) else ''
    essays.append((title, content))

os.makedirs('essays', exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Sky's Thought Hub</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .essay-body { max-width: 750px; margin: 6rem auto 10rem; padding: 0 2rem; }
        .essay-body h1 { font-size: 3.5rem; line-height: 1.1; margin-bottom: 3rem; color: #1c1c1c; }
        .meta { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em; color: #8b5e3c; margin-bottom: 2rem; display: block; }
        .prose { font-family: 'Lora', serif; font-size: 1.25rem; line-height: 1.8; color: #333; }
        .prose p { margin-bottom: 2rem; }
        .prose h3 { margin: 3rem 0 1.5rem; font-family: 'Lora', serif; font-weight: 600; color: #1c1c1c; }
        .back-link { display: inline-block; margin-bottom: 3rem; color: #5e5e5e; text-decoration: none; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; transition: color 0.3s; }
        .back-link:hover { color: #1c1c1c; }
    </style>
</head>
<body>
    <div class="nav-container"><nav><a href="../index.html" class="logo">SKY.LOG</a></nav></div>
    <main><article class="essay-body">
    <a href="../index.html" class="back-link">&larr; Back to Home</a>
    <span class="meta">2026 | Perspective</span>
    <span class="category">{{CATEGORY}}</span>
    <h1>{{TITLE}}</h1>
    <div class="prose">{{CONTENT}}</div></article></main>
    <footer><p>&copy; 2026 Sky. All rights reserved.</p></footer>
</body></html>"""

def get_html(md):
    """
    Converts markdown content into HTML paragraphs.
    Splits content by double newlines to identify paragraphs.
    Preserves single newlines within paragraphs as <br> tags.
    """
    # If a single newline likely represents a paragraph break (e.g. sentence end
    # followed by a capitalized line), normalize it to a double newline so the
    # paragraph splitter will treat it as a new paragraph.
    md = re.sub(r"([\.\?!][\"']?)\s*\n(?=[A-Z])", r"\1\n\n", md)

    paragraphs = re.split(r'\n\n+', md.strip())  # Split by double newlines or more
    html = ""
    for para in paragraphs:
        if para.strip():
            # Replace single newlines within a paragraph with <br> tags
            para = para.replace('\n', '<br>')
            html += f"<p>{para.strip()}</p>\n"
    return html

index_links = []
categories = {}
for title, content in essays:
    if not title.strip() or not content.strip(): continue
    
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    filename = f"{slug}.html"
    
    html_content = get_html(content)
    category = CATEGORY_MAP.get(title, 'Misc')
    page = TEMPLATE.replace('{{TITLE}}', title).replace('{{CONTENT}}', html_content).replace('{{CATEGORY}}', category)
    
    with open(os.path.join('essays', filename), 'w', encoding='utf-8') as f:
        f.write(page)
    
    # Summary for index
    words = content.strip().split()
    summary = ' '.join(words[:20]) + "..." if len(words) > 20 else content.strip()
    
    index_links.append(f"""<article class=\"card\" data-category=\"{category}\">\n                    <h3>{title}.</h3>\n                    <p>{summary}</p>\n                    <a href=\"essays/{filename}\" class=\"card-link\">Continue reading &rarr;</a>\n                </article>""")
    # collect categories
    categories.setdefault(category, []).append((title, filename, summary))

# Update index.html Hub section
with open('index.html', 'r', encoding='utf-8') as f:
    orig_index = f.read()

# Replace the grid content
grid_replacement = "\n                ".join(index_links)
# Write category pages
os.makedirs('categories', exist_ok=True)
category_links = []
for cat, items in categories.items():
    cat_slug = re.sub(r'[^a-zA-Z0-9]+', '-', cat.lower()).strip('-')
    cat_filename = f"{cat_slug}.html"
    items_html = "\n".join([f'<article class="card">\n  <h3>{t}.</h3>\n  <p>{s}</p>\n  <a href="../essays/{fn}" class="card-link">Continue reading &rarr;</a>\n</article>' for t, fn, s in items])
    cat_page = f"""<!DOCTYPE html>
<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<title>{cat} | Sky's Thought Hub</title>\n<link rel=\"stylesheet\" href=\"../styles.css\">\n</head>\n<body>\n<div class=\"nav-container\"><nav><a href=\"../index.html\" class=\"logo\">SKY.LOG</a></nav></div>\n<main><section class=\"category-page\">\n<h1>{cat}</h1>\n{items_html}\n</section></main>\n<footer><p>&copy; 2026 Sky. All rights reserved.</p></footer>\n</body>\n</html>"""
    with open(os.path.join('categories', cat_filename), 'w', encoding='utf-8') as f:
        f.write(cat_page)
    # make category links act as client-side filters (href '#' so they don't navigate)
    # but keep the category page url in data-page for optional use
    category_links.append(f'<a href="#" class="category-link" data-category="{cat}" data-page="categories/{cat_filename}">{cat}</a>')

# build categories nav html
categories_nav = '<div class="categories">' + ' | '.join(category_links) + '</div>'
# Replace the entire grid block inside the writing section (up to the section end)
new_index = re.sub(
    r'(<section id="writing">.*?<div class="grid">)(.*?)(</div>\s*</section>)',
    lambda m: m.group(1) + '\n                ' + categories_nav + '\n                ' + grid_replacement + '\n            ' + m.group(3),
    orig_index,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index)

print(f"Migration complete: {len(index_links)} essays processed.")
