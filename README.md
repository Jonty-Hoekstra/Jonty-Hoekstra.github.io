# Jonty Hoekstra — Game & Level Designer

The portfolio website of Jonty Hoekstra, a senior game designer and level designer. It is a static site (plain HTML, CSS and JavaScript, no build step), hosted on GitHub Pages.

## View it locally

Open `index.html` in a browser. Everything works from the file system.

## Publish on GitHub Pages

1. Push this folder to a GitHub repository. The folders `content/`, `concepts/` and `screenshots/` are in `.gitignore` and stay on your PC.
2. On GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to *Deploy from a branch*, the branch to `main`, and the folder to `/ (root)`. Select **Save**.
4. After a minute or two, the site is live at `https://jonty-hoekstra.github.io/` (repository name `jonty-hoekstra.github.io`). In general, the address is `https://<username>.github.io/<repository>/`. If the repository is named `<username>.github.io`, the site is at `https://<username>.github.io/`.

- All links and image paths are relative, so the site works at either address.
- `.nojekyll` tells GitHub Pages to serve the files as they are.
- `404.html` is the page that GitHub Pages shows for an address that does not exist.

## Content still needed

The site uses only the information in `content/ReadMe.txt`, Jonty's LinkedIn profile and the files in `content/`. Search the HTML for `TODO` to find each gap.

- [ ] **NDA title screenshots** — `ReadMe.txt` mentions them, but the folder is not in `content/` yet.
- [ ] **Cathedral Scene** — a short description of the project (`projects/cathedral-scene.html`).
- [ ] **Showreel** — optional. If there is one, host it on YouTube or Vimeo and link it from the Featured section.

## Add or change a project

1. Put the original images in `content/<Project Name>/`.
2. Add the files to the lists at the top of `tools/optimise_images.py`, then run `tools\Optimise-Images.bat`. It writes web-sized WebP images to `assets/img/<project-slug>/` and prints their sizes. Animated GIFs become animated WebP files with a still poster.
3. Copy an existing page in `projects/` to `projects/<project-slug>.html` and change the text and images. Use the printed sizes for each image's `width` and `height`.
4. Add a card for it in the Projects section of `index.html`, and update the previous/next links at the bottom of the project pages.
5. Run `tools\Capture-Devices.bat index.html projects\<project-slug>.html` and check the screenshots.

## Project structure

```
index.html               Home page: splash, featured, about, experience, projects, contact
projects/                One page per project
404.html                 "Page not found" page for GitHub Pages
assets/css/              tokens.css, base.css, layout.css, components.css
assets/js/               One script per behaviour (motion, splash, panel, reveal, tilt, lightbox)
assets/img/              Optimised images, one folder per project
assets/fonts/            Self-hosted fonts (see assets/fonts/README.md)
docs/                    Coding standards and device support
tools/                   Image optimiser and device screenshot scripts
```

## Standards

- [Coding Standards](docs/CodingStandards.md)
- [Device Support](docs/DeviceSupport.md)
