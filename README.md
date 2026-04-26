# Static Site Generator

A custom-built, lightweight static site generator written in Python. This project converts Markdown files into a fully functional HTML website, handling everything from nested directory structures to inline formatting and static asset management.

## Features

- **Markdown Parsing:** Full support for block-level elements (headings, blockquotes, code blocks, ordered/unordered lists) and inline elements (bold, italic, code, links, images).
- **Template System:** Uses a centralized `template.html` to ensure consistent styling and layout across the entire site.
- **Recursive Generation:** Automatically crawls the `content/` directory and mirrors the folder structure in the output directory.
- **Static Asset Management:** Recursively copies CSS and images from the `static/` folder to the production build.
- **GitHub Pages Support:** Includes `basepath` logic and production build scripts specifically configured for deployment via the `docs/` folder.

## Project Structure

- `src/`: The core Python engine (logic for HTML nodes, markdown parsing, and site generation).
- `content/`: Where your Markdown source files live.
- `static/`: Your CSS, images, and other static assets.
- `docs/`: The generated production website (configured for GitHub Pages).
- `template.html`: The base HTML structure used for every page.

## Usage

### Local Development
To build the site locally and see your changes:
```bash
./main.sh
```

### Production Build
To generate a build with a specific base path (useful for GitHub Pages sub-directories):
```bash
./build.sh
```

### Testing
To run the automated unit test suite:
```bash
./test.sh
```

## How It Works

1. **Clean & Copy:** The generator first wipes the `docs/` directory and recursively copies all files from `static/` to ensure a clean build.
2. **Crawl:** It then recursively walks through the `content/` directory.
3. **Convert:** Each `.md` file is parsed into a tree of HTML nodes, which are then rendered into an HTML string.
4. **Wrap:** The generator extracts the title from the Markdown and injects both the title and the content into the `template.html`.
5. **Deploy:** Links are automatically updated with the correct `basepath` to ensure they work correctly in your hosted environment.
