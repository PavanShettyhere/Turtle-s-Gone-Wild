# Turtle-s-Gone-Wild

Pavan’s growing TurtleBot build journal: ROS 2 Jazzy, Raspberry Pi, explained terminal commands, and future experiments.

- [Interactive journal](https://PavanShettyhere.github.io/Turtle-s-Gone-Wild/)
- [Quick command cheat sheet](https://PavanShettyhere.github.io/Turtle-s-Gone-Wild/cheatsheet.html)
- [Full day-by-day document](JOURNAL.md)
- [Template for the next day](DAY-TEMPLATE.md)

## Accuracy

Day 1 milestones come from the author’s description. Detailed commands are a reference reconstruction, not recovered terminal history. Day 2 assumes a Pi installation and is explicitly awaiting confirmation. Confirmed hardware: Raspberry Pi 4B, TurtleBot Burger, and a 32 GB SanDisk microSD card. Supplied terminal evidence verifies the Pi currently runs Ubuntu 24.04.5 LTS (Noble Numbat), arm64. The original image filename, flashing sequence, dates, and ROS installation/test outputs remain unconfirmed. Official sources are linked in the journal. Robot-specific bringup is intentionally pending hardware identification.

## Add a day

Edit `docs/journal.json`, copy an existing day structure with a new unique ID, and add the actual commands, explanations, output, errors, and evidence. Then:

```bash
python3 scripts/build.py
git add docs/journal.json docs/index.html docs/JOURNAL.md JOURNAL.md
git diff --cached
git commit -m "Document the next TurtleBot day"
git push
```

The workflow rebuilds and deploys `docs/` to GitHub Pages. Configure **Settings → Pages → Source → GitHub Actions** if setting up a new copy.

## Preview

```bash
python3 scripts/build.py
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. No npm packages, external fonts, or runtime services are needed. Search, collapsible steps, copy buttons, local reading progress, reduced-motion support, and print-to-PDF are included. Reading progress stays in the current browser; it is not shared with GitHub.

## Files

`docs/journal.json` is the content source. `scripts/template.html` and `docs/style.css` define the presentation. `docs/app.js` handles interactions. `scripts/build.py` generates both document formats. Do not edit generated files directly.

## Visual guide

The midnight-blue, cyan, and coral design includes original SVG hardware illustrations, switchable SSH/ROS message explanations, and a miniature TurtleBot animation. The animation is a browser demonstration, not robot control. Pause animations with the on-page control; system reduced-motion preferences are respected. Assets are local to `docs/assets/`.

The separate cheat sheet lives in `docs/cheatsheet.html`, with search/filter/copy behavior in `docs/cheatsheet.js`. Edit these directly; the journal generator preserves them.
