# Code Snippet Presentation Generator

A tool to create Reveal.js-based HTML presentations of code snippets with a typewriter effect. The generator automatically formats code files, selects appropriate font sizes, and generates both an interactive HTML presentation and static PNG images.

## Features

- **Typewriter Effect**: Code lines appear sequentially with a typing animation (in HTML presentation)
- **Dynamic Font Sizing**: Automatically selects the optimal font size based on line count
- **Line Count Limit**: Processes only snippets with fewer than 25 lines
- **Syntax Highlighting**: Supports Python, Java, C++, and Go
- **PNG Export**: Generates static PNG images of each slide showing the final state
- **Presentation UI**: Clean, minimalist design with empty header and line numbers

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`:
  - Jinja2 (templating)
  - Playwright (HTML rendering and PNG export)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright's browser:
   ```bash
   playwright install chromium
   ```

## Usage

1. Place your code snippets in the `snippets/` directory
2. Run the generator:
   ```bash
   python generate_presentation.py
   ```
3. View the HTML presentation in your browser:
   ```bash
   open output/presentation.html
   ```
4. Navigate slides using arrow keys to see the typewriter effect

## Project Structure

```
project/
├── snippets/              # Input code files
│   ├── fibonacci.py
│   ├── Fibonacci.java
│   ├── fibonacci.cpp
│   ├── fibonacci.go
│   └── medium_snippet.py
├── templates/             # HTML templates
│   └── presentation.html
├── output/                # Generated files
│   ├── presentation.html
│   └── presentation_*.png
├── generate_presentation.py  # Main script
└── requirements.txt       # Dependencies
```

## Configuration

You can modify the following parameters in `generate_presentation.py`:

- `FILES`: List of code files to process
- `MAX_LINES`: Maximum number of lines for a snippet (default: 25)
- `FONT_SIZES`: Available font sizes in pixels (default: [16, 20, 24, 28, 32])

## Typewriter Effect

The typewriter effect is implemented using JavaScript and CSS:

- Each line appears with a 500ms delay
- The animation only runs in the HTML presentation
- PNG exports show the final state with all lines visible

To view the typewriter effect, open `output/presentation.html` in a browser and navigate through the slides using arrow keys.

## Customization

You can adjust the typewriter animation speed by modifying the timeout value in the JavaScript section of `templates/presentation.html`:

```javascript
setTimeout(typeLine, 500); // Change 500 to adjust the delay per line
```