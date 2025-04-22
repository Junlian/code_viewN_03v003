import os
import html
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
import math

# Configuration
SNIPPET_DIR = "snippets"
OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"
FILES = [
    ("fibonacci.py", "python"),
    ("Fibonacci.java", "java"),
    ("fibonacci.cpp", "cpp"),
    ("fibonacci.go", "go"),
    ("medium_snippet.py", "python")
]
MAX_LINES = 25
# Updated values for header
CODE_AREA_HEIGHT = 656  # 900px - 200px (header) - 40px padding = 656px
FONT_SIZES = [16, 20, 24, 28, 32]  # Available font sizes (px)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to choose font size based on line count
def choose_font_size(line_count):
    if line_count == 0:
        return FONT_SIZES[-1]  # Default to largest if no lines
    max_font = (CODE_AREA_HEIGHT / 1.5) / line_count  # From (available height) / (1.5 * line_count)
    for font_size in sorted(FONT_SIZES, reverse=True):
        if font_size <= max_font:
            return font_size
    return FONT_SIZES[0]  # Fallback to smallest

# Read and process code snippets
snippets = []
for file_name, language in FILES:
    file_path = os.path.join(SNIPPET_DIR, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read().rstrip()
    lines = code.split("\n")
    line_count = len(lines)
    
    # Skip snippets with 25 or more lines
    if line_count < MAX_LINES:
        font_size = choose_font_size(line_count)
        
        # Create pairs of line numbers and code lines for the template
        line_pairs = []
        for i, line in enumerate(lines):
            line_num = str(i+1)
            # Escape HTML but preserve whitespace
            escaped_line = html.escape(line)
            line_pairs.append((line_num, escaped_line))
        
        snippets.append({
            "language": language,
            "code": code,
            "font_size": font_size,
            "file_name": os.path.splitext(file_name)[0],
            "line_pairs": line_pairs,
            "line_count": line_count  # Add line count for typewriter effect timing
        })
        print(f"Processing {file_name}: {line_count} lines, {font_size}px font")
    else:
        print(f"Skipping {file_name}: {line_count} lines (≥ {MAX_LINES})")

# Generate HTML
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("presentation.html")
html_content = template.render(snippets=snippets)

# Save HTML
html_output_path = os.path.join(OUTPUT_DIR, "presentation.html")
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated HTML: {html_output_path}")

# Generate PNGs for each slide
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"file://{os.path.abspath(html_output_path)}")
    
    for i, snippet in enumerate(snippets):
        page.evaluate(f"Reveal.slide({i}, 0);")
        
        # Wait for typewriter animation to complete
        # Initial delay (500ms) + (line count * 500ms delay per line)
        wait_time = 1000 + (snippet['line_count'] * 500)
        page.wait_for_timeout(wait_time)
        
        png_path = os.path.join(OUTPUT_DIR, f"presentation_{snippet['file_name']}_{snippet['language']}.png")
        page.screenshot(path=png_path, full_page=True)
        print(f"Generated PNG: {png_path}")
    
    browser.close()