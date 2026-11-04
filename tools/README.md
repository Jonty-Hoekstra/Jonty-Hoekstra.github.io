# Tools

Developer scripts for the portfolio site. Each script has a `.bat` file that runs it, so you can double-click it or run it from any shell.

| Script | What it does |
|---|---|
| `Capture-Devices` | Takes a screenshot of one or more pages at each standard device size, with headless Chrome or Edge. The images go to `screenshots\<page>\<device>.png`. Name the pages after the script, separated by spaces: `Capture-Devices.bat index.html projects\x.html` (default: `index.html`). `-FullPage` also takes an 8000px tall image. |

- `Capture-Devices` needs Chrome or Edge installed in the usual folder.
- The device list in the script matches the table in [docs/DeviceSupport.md](../docs/DeviceSupport.md#device-sizes). Change both together.
- To view the site locally, open `index.html` in a browser. If a feature needs a web server (for example, `fetch` of a local file), run `python -m http.server 8000` in the project folder and open `http://localhost:8000`.
