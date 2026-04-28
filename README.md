This repository controls the lab website, which uses the Rust-based [Zola](https://www.getzola.org/) static-site generator, combined with the [Vonge](https://www.getzola.org/themes/vonge/) theme/template. It uses a GitHub Action (`.github/workflows/deploy.yml`) to automatically rebuild and publish the website when changed are pushed to `main`.

[See the wiki](https://github.com/therkildsen-lab/therkildsen-lab.github.io/wiki) for details on how things work and how to make changes.

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
