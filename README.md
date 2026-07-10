# The School Shop — Website

Playful one-page website for **The School Shop** (@the_school_shop_ on Instagram),
manufacturer and supplier of quality uniforms for schools and organisations.

## Files

| File | What it is |
|---|---|
| `index.html` | The website (fonts + logo embedded; photos referenced from `assets/web/`). Deploy the whole folder. |
| `index.template.html` | Editable source. Edit this, then rebuild (see below). |
| `assets/build_site.py` | Rebuilds `index.html`, `assets/logo.svg` and the web-sized photos in `assets/web/`. |
| `assets/logo.svg` | Standalone vector logo (font embedded — works anywhere, scales to any size). |
| `assets/logo-on-black.png` | PNG export of the logo on black, 1000×1000 (for WhatsApp/profile pictures). |
| `assets/*.woff2` | The two fonts (Titan One, Baloo 2), embedded into the pages at build time. |
| `assets/insta/` | Original product photos pulled from the Instagram feed (source images). |
| `assets/web/` | Generated web-sized photos: `cat-*` for category cards, `gal-*` for the gallery. |

To add a photo to the gallery: drop the image in `assets/insta/`, add a line to the
`GALLERY` list in `assets/build_site.py` (slug + caption), and rebuild.

## View it

Just open `index.html` in any browser — no server needed.

## Contact details (already filled in)

- WhatsApp/mobile: **+232 76 602 248** (`wa.me/23276602248`)
- Email: **info@theschoolshop.org**
- Address: **29B Kingharman Road, Freetown, Sierra Leone**

To change any of these (or add opening hours), edit `index.template.html` and rebuild:

```bash
python3 assets/build_site.py
```

## Deploy (free options)

- **Vercel** — import the GitHub repo at vercel.com/new, Framework Preset "Other", no build command.
- **Netlify Drop** — drag the whole project folder onto https://app.netlify.com/drop.
- **GitHub Pages** — enable Pages in the repo Settings.
- Any static host works; there are no external dependencies and no build step required to serve it.
