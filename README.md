# The School Shop — Website

Playful one-page website for **The School Shop** (@the_school_shop_ on Instagram),
manufacturer and supplier of quality uniforms for schools and organisations.

## Files

| File | What it is |
|---|---|
| `index.html` | The website — **fully self-contained** (fonts + logo embedded). This is the only file you need to deploy. |
| `index.template.html` | Editable source. Edit this, then rebuild (see below). |
| `assets/build_site.py` | Rebuilds `index.html` and `assets/logo.svg` from the template. |
| `assets/logo.svg` | Standalone vector logo (font embedded — works anywhere, scales to any size). |
| `assets/logo-on-black.png` | PNG export of the logo on black, 1000×1000 (for WhatsApp/profile pictures). |
| `assets/*.woff2` | The two fonts (Titan One, Baloo 2), embedded into the pages at build time. |
| `assets/insta/` | Real product photos pulled from the Instagram feed (`*.sq.jpg` are the square web versions, embedded into the Instagram section at build time). |

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

- **Netlify Drop** — drag `index.html` onto https://app.netlify.com/drop → instant live URL.
- **GitHub Pages** — push this folder to a repo, enable Pages in Settings.
- Any static host works; `index.html` has zero external dependencies.
