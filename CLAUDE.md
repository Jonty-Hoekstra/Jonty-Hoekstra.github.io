# Jonty Portfolio — Guidance for Claude Code

This is a portfolio website for **Jonty, a game and level designer**. It shows Jonty's projects, level design process, experience and contact details to studios and recruiters. It is a static site: plain HTML, CSS and JavaScript, with no framework and no build step. It is **hosted on GitHub Pages**, so every path is relative and the site must also work when opened from disk.

The design is concept `02e` ("Menu Dock + About"): a full-screen splash menu that hands over to a docked side panel, with scroll-driven reveal animations. `README.md` lists the content that Jonty still has to supply.

## Standards (authoritative)

- **[Coding Standards](docs/CodingStandards.md)** — follow these for all site code. Key points: mobile first with `min-width` breakpoints; no horizontal scroll from 320px to 2560px; all colours, fonts and spacing as tokens in `tokens.css`; semantic HTML, one `<h1>`, links for navigation and buttons for actions; light BEM class names and `data-` hooks for JS; hover effects in `@media (hover: hover)` and nothing behind hover only; 44px touch targets and visible focus; images with `srcset`, `width`, `height`, `alt` and lazy loading; `prefers-reduced-motion` respected; plain JavaScript, one file per behaviour; WCAG 2.2 AA.
- **[Device Support](docs/DeviceSupport.md)** — the browsers and device sizes we support and how to check a change. Key points: last two versions of Chrome, Edge, Firefox, Safari and Samsung Internet; nine check sizes from 320 × 568 to 2560 × 1440; run `tools\Capture-Devices.bat` and look at every image before you call a change done.

## Project layout

- `index.html`, `projects/`, `404.html` — the live site pages.
- `assets/` — CSS, JS, optimised images, fonts and PDFs. See [Coding Standards → Project Structure](docs/CodingStandards.md#project-structure).
- `content/` — Jonty's original media and `ReadMe.txt`, the source of every project fact. Not published. Run `tools\Optimise-Images.bat` after a change here.
- `concepts/` — layout concepts. `concepts/index.html` compares them. They are reference designs with made-up content, not the live site. Not published.
- `docs/` — the coding standards and device support docs.
- `tools/` — developer scripts. `tools/README.md` lists them.
- `screenshots/` — output of `Capture-Devices`. Do not publish it.

## Building and checking

- **There is no build.** Open `index.html` in a browser, or run `python -m http.server 8000` and open `http://localhost:8000`.
- **Check each change on the device sizes.** Run `tools\Capture-Devices.bat <changed pages>` and look at each screenshot before you report the change as done. Report what you checked and anything that looked wrong.

## Commits

- **Commit only when the user asks.**
- **Short messages.** One imperative title line that says what the commit does. Add a few bullet points only if the change needs them.

## Decisions

- **A design choice is asked, not made.** When a request leaves more than one reasonable approach open, give the options and a recommendation, and wait for the user to choose. Routine calls that the standards already settle are not design choices.
- **A new library, framework, build tool or third-party service is always a design choice.**
- **Content is Jonty's.** Do not invent project facts, studios, dates, numbers or quotes for the live site. Take facts only from `content/ReadMe.txt`, Jonty's CV, Jonty's LinkedIn profile and what the images show. Never publish the CV's home address, phone number or references. Mark each gap with a `TODO` comment, add it to the "Content still needed" list in `README.md`, and list it in the report.

## Writing style

- **Plain English, British spelling** in docs, comments, commit messages and site text.
- **Short sentences, active voice.** One instruction per sentence in the docs.
- **Site text speaks as Jonty,** in the first person: friendly and confident, not jokey. Avoid gamer slang in navigation and headings; plain labels (Projects, About, Contact) are easier for recruiters to scan.

---

When a request touches code, use the conventions above, not generic defaults. Where this file and a doc disagree, the doc wins.
