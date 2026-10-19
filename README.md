# leisuregensoul.github.io

LeisureGensoul's personal website.

[Architecture](docs/ARCHITECTURE.md) · [Environment](docs/ENVIRONMENT.md)

## Build

With Python 3.12 and a virtual environment activated:

```sh
python -m pip install -r requirements.txt
python -m generator
python -m http.server 8000 --directory dist
```

Open http://localhost:8000/ to preview the site.

## Structure

```text
content/          Markdown content
docs/             Internal documentation
templates/        HTML templates
assets/           Stylesheets and images
generator/        Site generator
dist/             Generated output, excluded from Git
requirements.txt  Python dependencies
```
