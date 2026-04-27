This repository controls the lab website, which uses the Rust-based [Zola](https://www.getzola.org/) static-site generator, combined with the [Vonge](https://www.getzola.org/themes/vonge/) theme/template. It uses a GitHub Action (`.github/workflows/deploy.yml`) to automatically rebuild and publish the website when changed are pushed to `main`.

## Local edits with live view
For spot-fixes, it would be simple to edit the repo directly, but for more involved editing, the preferred way to
edit this website would be making changes and viewing the live edits using `zola` on your system. 

### 1. Install zola
##### macOS
```bash
brew install zola
```
##### Windows
```shell
winget install getzola.zola
```
##### Linux
See the [official installation instructions](https://www.getzola.org/documentation/getting-started/installation/) for
the command that would work for your OS.

### 2. Clone this repo
This requires `git` to be installed on your machine
```bash
git clone --recursive https://github.com/therkildsen-lab/therkildsen-lab.github.io.git
```
The `--recursive` part is **critical** so that it also includes the theme/template.

### 3. Live-view
You can live-view changes with a locally-served site via
```bash
zola serve
```


## Organization
- `scripts/update_publications.py`: python script to use the Semantic Scholar API to get Nina's publications and and write a new `publications.md` file.
  - `.github/workflows/update-publications.yml` runs this once every 4 months, so manual intervention is unlikely
- `themes/` contains the site theme `vonge`
- `templates/` contains the modified versions of the base `vonge` template to remove some stuff like the newsletter, and adds a `custom_md.html` template for allowing basic markdown pages (like `publications.md`)
- `content/posts` is the home of blog/news posts
- `content/projects` is the home of the individual project pages
- `content/testimonial` is the home of the lab members' info pages, which get populated into the homepage row. The name `testimonials` is a holdover from the `vonge` template and changing the internals would be more effort than it's worth
- `config.toml` is the website configuration, including the structure of the home page, nav bar, etc.
- `static/` contains all the static content like images. It's the folder zola looks into when you point paths to images
  - specifying `images/file.jpg` in a page actually points to `static/images/file.jpg`
- `.github/workflows/deploy.yml` is the GitHub Actions workflow that builds and publishes the webiste on pushes to `main`
