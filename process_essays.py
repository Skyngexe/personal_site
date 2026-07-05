import os
import re

# --- Titles, in the order they appear in essays.md ---
titles = [
    'Preface',
    'Breakfast Ritual',
    'Gifted polymorphism',
    'Coffee break',
    'Dissolution',
    'Weight or lightness',
    'Relationships',
    'Tampering',
    'Typhoon',
    'Originality, authenticity and self-identity',
    'Fantasy of my own funeral',
    'Mr Nimbus and Roger',
    'Fake tattoo',
    'Til then',
    'Chaos and comfort',
    'English Proficiency as a class indicator',
    'Pool in the city',
    'Endurance running is an abusive self-masturbatory act',
    'The optimal distance of one another',
    'The last semester, there goes my training wheels',
    'Form over functionality',
    'The anatomy of pretentious culture',
    'Attention is all we need',
    'Vitiligo',
    'We should be freakier',
    'La Vache',
    'Rain',
    'Maxxing',
    'The Art of Living',
    'Ego death is the death by Guillotine',
    'The view from (almost) fullway down',
    'Glitters of thy eyes',
    'Fortuity is the beauty of life',
    'Beyond the hype and desperation of technological acceleration',
    'Everybody hates their own country',
    'The flavour of mud and pud',
]

# --- Clean, consolidated taxonomy (8 categories, no overlaps) ---
CATEGORY_MAP = {
    'Preface': 'Philosophy & Reflection',
    'Breakfast Ritual': 'Rituals & Everyday',
    'Gifted polymorphism': 'Identity & Self',
    'Coffee break': 'Poems',
    'Dissolution': 'Philosophy & Reflection',
    'Weight or lightness': 'Philosophy & Reflection',
    'Relationships': 'Relationships',
    'Tampering': 'Poems',
    'Typhoon': 'Poems',
    'Originality, authenticity and self-identity': 'Identity & Self',
    'Fantasy of my own funeral': 'Philosophy & Reflection',
    'Mr Nimbus and Roger': 'Identity & Self',
    'Fake tattoo': 'Identity & Self',
    'Til then': 'Relationships',
    'Chaos and comfort': 'Identity & Self',
    'English Proficiency as a class indicator': 'Culture & Society',
    'Pool in the city': 'Philosophy & Reflection',
    'Endurance running is an abusive self-masturbatory act': 'Rituals & Everyday',
    'The optimal distance of one another': 'Relationships',
    'The last semester, there goes my training wheels': 'Philosophy & Reflection',
    'Form over functionality': 'Culture & Society',
    'The anatomy of pretentious culture': 'Culture & Society',
    'Attention is all we need': 'Tech & Society',
    'Vitiligo': 'Poems',
    'We should be freakier': 'Poems',
    'La Vache': 'Poems',
    'Rain': 'Poems',
    'Maxxing': 'Culture & Society',
    'The Art of Living': 'Philosophy & Reflection',
    'Ego death is the death by Guillotine': 'Short Stories',
    'The view from (almost) fullway down': 'Philosophy & Reflection',
    'Glitters of thy eyes': 'Philosophy & Reflection',
    'Fortuity is the beauty of life': 'Philosophy & Reflection',
    'Beyond the hype and desperation of technological acceleration': 'Tech & Society',
    'Everybody hates their own country': 'Culture & Society',
    'The flavour of mud and pud': 'Poems',
}

# Order categories should appear in the filter bar
CATEGORY_ORDER = [
    'Identity & Self',
    'Philosophy & Reflection',
    'Relationships',
    'Rituals & Everyday',
    'Tech & Society',
    'Culture & Society',
    'Poems',
    'Short Stories',
]

if not os.path.exists('essays.md'):
    print("essays.md not found.")
    exit()

with open('essays.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split on title lines. Allow trailing whitespace after a title (this previously
# caused 'Vitiligo ' and 'Maxxing ' to be silently dropped).
pattern = '|'.join([re.escape(t) for t in titles])
segments = re.split(f'^({pattern})[ \\t]*$', text, flags=re.MULTILINE)

essays = []
for i in range(1, len(segments), 2):
    title = segments[i].strip()
    content = segments[i + 1] if i + 1 < len(segments) else ''
    essays.append((title, content))

os.makedirs('essays', exist_ok=True)
os.makedirs('categories', exist_ok=True)

ESSAY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} — Sky</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='45' fill='%238a3324' fill-opacity='0.08' stroke='%238a3324' stroke-width='2'/><circle cx='50' cy='50' r='9' fill='%238a3324'/></svg>">
    <script>(function(){var t=localStorage.getItem('theme')||((window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light');document.documentElement.setAttribute('data-theme',t);})();</script>
</head>
<body>
    <div class="progress-bar" id="progressBar"></div>
    <div class="nav-container"><nav>
        <a href="../index.html" class="logo">Sky</a>
        <button class="theme-toggle" id="themeToggle" aria-label="Toggle day / dusk mode" title="Toggle day / dusk">
            <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.8v2.4M12 19.8v2.4M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M1.8 12h2.4M19.8 12h2.4M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>
            <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>
        </button>
    </nav></div>
    <main>
        <article class="essay-body">
            <a href="../index.html#writing" class="back-link">&larr; All writing</a>
            <span class="meta">{{CATEGORY}}</span>
            <h1>{{TITLE}}</h1>
            <div class="prose">{{CONTENT}}</div>
        </article>
    </main>
    <footer>
        <p class="colophon">Built with <strong>Claude Code</strong>.</p>
        <p class="copyright">&copy; 2026 Sky. All rights reserved.</p>
    </footer>
    <script>
    (function(){
        var root=document.documentElement, t=document.getElementById('themeToggle');
        t.addEventListener('click',function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);localStorage.setItem('theme',n);});
        var bar=document.getElementById('progressBar');
        function s(){var h=document.documentElement.scrollHeight-window.innerHeight;bar.style.width=(h>0?(window.scrollY/h)*100:0)+'%';document.querySelector('.nav-container').classList.toggle('scrolled',window.scrollY>10);}
        window.addEventListener('scroll',s,{passive:true});s();
    })();
    </script>
</body>
</html>"""

CATEGORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{CAT}} — Sky</title>
    <link rel="stylesheet" href="../styles.css">
    <script>(function(){var t=localStorage.getItem('theme')||((window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light');document.documentElement.setAttribute('data-theme',t);})();</script>
</head>
<body>
    <div class="nav-container"><nav><a href="../index.html" class="logo">Sky</a></nav></div>
    <main>
        <section class="category-page">
            <a href="../index.html#writing" class="back-link">&larr; All writing</a>
            <h1>{{CAT}}</h1>
            {{ITEMS}}
        </section>
    </main>
    <footer>
        <p class="colophon">Built with <strong>Claude Code</strong>.</p>
        <p class="copyright">&copy; 2026 Sky. All rights reserved.</p>
    </footer>
</body>
</html>"""


def get_html(md):
    """Convert plain text into HTML paragraphs.
    A sentence end followed by a capitalized new line is treated as a paragraph
    break; remaining single newlines become <br> (keeps poem line breaks)."""
    md = re.sub(r"([\.\?!][\"']?)\s*\n(?=[A-Z])", r"\1\n\n", md)
    paragraphs = re.split(r'\n\n+', md.strip())
    html = ""
    for para in paragraphs:
        if para.strip():
            para = para.strip().replace('\n', '<br>')
            html += f"<p>{para}</p>\n"
    return html


index_cards = []
categories = {}

for title, content in essays:
    if not title or not content.strip():
        continue

    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    filename = f"{slug}.html"
    category = CATEGORY_MAP.get(title, 'Philosophy & Reflection')

    # Essay page
    page = (ESSAY_TEMPLATE
            .replace('{{TITLE}}', title)
            .replace('{{CONTENT}}', get_html(content))
            .replace('{{CATEGORY}}', category))
    with open(os.path.join('essays', filename), 'w', encoding='utf-8') as f:
        f.write(page)

    # Summary for the card
    words = content.strip().split()
    wordcount = len(words)
    summary = ' '.join(words[:24]) + ('…' if wordcount > 24 else '')

    index_cards.append(
        '<article class="card" data-category="{cat}" data-words="{wc}">\n'
        '                    <span class="card-cat">{cat}</span>\n'
        '                    <h3>{title}.</h3>\n'
        '                    <p>{summary}</p>\n'
        '                    <a href="essays/{fn}" class="card-link">Continue reading &rarr;</a>\n'
        '                </article>'.format(cat=category, title=title, summary=summary, fn=filename, wc=wordcount)
    )

    categories.setdefault(category, []).append((title, filename, summary))

# --- Category landing pages ---
for cat, items in categories.items():
    cat_slug = re.sub(r'[^a-zA-Z0-9]+', '-', cat.lower()).strip('-')
    items_html = "\n".join(
        '<article class="card">\n'
        '                <span class="card-cat">{cat}</span>\n'
        '                <h3>{t}.</h3>\n'
        '                <p>{s}</p>\n'
        '                <a href="../essays/{fn}" class="card-link">Continue reading &rarr;</a>\n'
        '            </article>'.format(cat=cat, t=t, s=s, fn=fn)
        for t, fn, s in items
    )
    cat_page = CATEGORY_TEMPLATE.replace('{{CAT}}', cat).replace('{{ITEMS}}', items_html)
    with open(os.path.join('categories', f"{cat_slug}.html"), 'w', encoding='utf-8') as f:
        f.write(cat_page)

# --- Filter bar (ordered) ---
category_links = []
for cat in CATEGORY_ORDER:
    if cat not in categories:
        continue
    cat_slug = re.sub(r'[^a-zA-Z0-9]+', '-', cat.lower()).strip('-')
    category_links.append(
        '<a href="#" class="category-link" data-category="{cat}" '
        'data-page="categories/{slug}.html">{cat}</a>'.format(cat=cat, slug=cat_slug)
    )
categories_nav = '<div class="categories">' + ''.join(category_links) + '</div>'

# --- Inject into index.html writing grid ---
with open('index.html', 'r', encoding='utf-8') as f:
    orig_index = f.read()

grid_inner = (
    '\n                ' + categories_nav +
    '\n                ' + "\n                ".join(index_cards) +
    '\n            '
)

new_index = re.sub(
    r'(<section id="writing">.*?<div class="grid">)(.*?)(</div>\s*</section>)',
    lambda m: m.group(1) + grid_inner + m.group(3),
    orig_index,
    count=1,
    flags=re.DOTALL,
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index)

print(f"Done: {len(index_cards)} essays, {len(categories)} categories.")
for cat in CATEGORY_ORDER:
    if cat in categories:
        print(f"  {cat}: {len(categories[cat])}")
