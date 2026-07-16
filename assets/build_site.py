#!/usr/bin/env python3
"""Build The School Shop site: generates logo.svg and index.html from index.template.html.

- logo.svg  : standalone, Titan One embedded as base64 (works anywhere, incl. <img>)
- index.html: template with fonts embedded and the hero logo inlined (inherits page font)
"""
import base64
import pathlib
import re
import sys
from urllib.parse import quote

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent

PURPLE = "#8C1FA8"
PINK = "#FF2E64"
YELLOW = "#FFDD15"
CYAN = "#35DDF2"
GREEN = "#3FDE8A"
INK = "#111116"

titan_b64 = base64.b64encode((HERE / "TitanOne-400.woff2").read_bytes()).decode()
baloo_b64 = base64.b64encode((HERE / "Baloo2-500.woff2").read_bytes()).decode()

WORD_ATTRS = ('font-family="Titan One, Arial Black, sans-serif" '
              'text-anchor="middle" letter-spacing="4"')


def logo_svg(embed_font: bool, extra_attrs: str = "") -> str:
    font_style = ""
    if embed_font:
        font_style = f'''
    <style>
      @font-face {{
        font-family: 'Titan One';
        src: url(data:font/woff2;base64,{titan_b64}) format('woff2');
        font-weight: 400;
        font-style: normal;
      }}
    </style>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 900" role="img" aria-label="The School Shop logo" {extra_attrs}>
  <defs>{font_style}
    <g id="kid">
      <circle cx="8" cy="-78" r="42" fill="{PINK}"/>
      <path d="M 2 8 L -78 -68" stroke="{PINK}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <path d="M 6 4 L 88 -50" stroke="{PINK}" stroke-width="30" stroke-linecap="round" fill="none"/>
      <path d="M 4 -12 C -30 30 -52 90 -60 152 C -20 172 30 168 58 138 C 44 80 26 24 4 -12 Z" fill="{PINK}"/>
    </g>
  </defs>

  <!-- house -->
  <rect x="375" y="248" width="250" height="270" rx="16" fill="{PURPLE}"/>
  <path d="M 330 235 L 500 115 L 670 235" stroke="{PURPLE}" stroke-width="46" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <g fill="{INK}">
    <rect x="449" y="294" width="44" height="44" rx="10"/>
    <rect x="507" y="294" width="44" height="44" rx="10"/>
    <rect x="449" y="352" width="44" height="44" rx="10"/>
    <rect x="507" y="352" width="44" height="44" rx="10"/>
  </g>

  <!-- celebrating kids -->
  <use href="#kid" transform="translate(280 330)"/>
  <use href="#kid" transform="translate(720 330) scale(-1 1)"/>

  <!-- cloud -->
  <g fill="{PURPLE}">
    <circle cx="250" cy="590" r="145"/>
    <circle cx="375" cy="525" r="140"/>
    <circle cx="625" cy="525" r="140"/>
    <circle cx="750" cy="590" r="145"/>
    <circle cx="500" cy="640" r="200"/>
    <circle cx="360" cy="730" r="115"/>
    <circle cx="640" cy="730" r="115"/>
    <circle cx="500" cy="760" r="120"/>
  </g>

  <!-- pink parentheses swooshes -->
  <g stroke="{PINK}" stroke-width="20" stroke-linecap="round" fill="none">
    <path d="M 244 556 Q 226 586 222 622"/>
    <path d="M 222 652 Q 228 694 254 726"/>
    <path d="M 748 692 Q 768 726 771 764"/>
    <path d="M 769 794 Q 763 830 738 856"/>
  </g>

  <!-- wordmark -->
  <text {WORD_ATTRS} x="500" y="540" font-size="95" fill="{YELLOW}" rotate="-5 2 5" dy="0 -8 14">THE</text>
  <text {WORD_ATTRS} x="500" y="660" font-size="126" fill="{CYAN}" rotate="-4 3 -3 4 -4 3" dy="0 -10 16 -14 12 -8">SCHOOL</text>
  <text {WORD_ATTRS} x="500" y="782" font-size="126" fill="{GREEN}" rotate="-4 4 -3 4" dy="0 -12 18 -12">SHOP</text>
</svg>'''


# 1. standalone logo
standalone = logo_svg(embed_font=True)
(HERE / "logo.svg").write_text(standalone)
print(f"assets/logo.svg          {len(standalone):>7,} bytes")

# 2. photos: sources in assets/insta/, web versions generated into assets/web/
from PIL import Image

WEB = HERE / "web"
WEB.mkdir(exist_ok=True)

# order defines the gallery flow
GALLERY = [
    ("kids-group", "Our superstars in The School Shop blue and white"),
    ("trousers-grey", "Grey regular-fit school trousers with Teflon® finish"),
    ("shoes-lol", "L.O.L Surprise character sneakers"),
    ("shirts-blue", "Slim-fit blue short-sleeve school shirts"),
    ("skirt-navy-2pleat", "Navy two-pleat senior girls skirt"),
    ("kid-boy", "Blue short-sleeve shirt and navy shorts — ready for class"),
    ("shoes-black-leather", "Classic black leather school shoes"),
    ("shirts-white", "Non-iron white school shirts — zero ironing needed"),
    ("skirt-navy-pleated", "Navy pleated skirt with permanent pleats"),
    ("girl-stain-resistant", "Stain-resistant shirts, tested on real school days"),
    ("shorts-navy", "Navy school shorts in a new slimmer cut"),
    ("polos-red", "Pure cotton polo shirts — stain resistant"),
    ("shoes-black-canvas", "Black lace-up canvas shoes with gripped soles"),
]
CAT_PHOTOS = ["shirts-white", "trousers-grey", "skirt-navy-2pleat",
              "shoes-black-leather", "polos-red"]

# showroom: individual products a customer can browse & order.
# (photo slug in assets/insta/, product name, one short detail line, category)
# category order below defines the order of the filter chips.
SHOWROOM = [
    ("shirts-white", "Non-Iron White Shirt", "Zero ironing · slim & regular fit", "Shirts"),
    ("shirts-blue", "Blue Short-Sleeve Shirt", "Cool & breathable for warm days", "Shirts"),
    ("polos-red", "Red Cotton Polo", "Pure cotton · stain resistant", "Shirts"),
    ("blouse-embroidered", "Girls Embroidered Collar Blouse", "Limited edition · pack of 2", "Shirts"),
    ("trousers-grey", "Grey School Trousers", "Teflon® finish · adjustable waist", "Trousers"),
    ("shorts-navy", "Navy School Shorts", "New slimmer, comfier cut", "Trousers"),
    ("shorts-navy-elastic", "Boys Half-Elasticated Shorts", "Elasticated back waist · ages 3–4 to 11–12", "Trousers"),
    ("shorts-navy-smart", "Boys Navy Shorts", "Smart belt loops · pack of 2", "Trousers"),
    ("skirt-navy-2pleat", "Navy Two-Pleat Skirt", "Permanent pleats · senior girls", "Skirts"),
    ("skirt-navy-pleated", "Navy Pleated Skirt", "Crease-resistant · adjustable waist", "Skirts"),
    ("skirt-navy-permanent", "Navy Permanent Pleats Skirt", "Permanent pleats · pack of 2", "Skirts"),
    ("skirt-navy-bow", "Girls Junior Bow Skirt", "Bow detail · ages 3–4 to 11–12", "Skirts"),
    ("skirt-navy-senior", "Senior Girls Pleated Skirt", "Pack of 2 · ages 11–12 to 14–15", "Skirts"),
    ("skirt-navy-flare", "Junior Girls Pleated Flare Skirt", "Pack of 2 · ages 3–4 to 11–12", "Skirts"),
    ("shoes-black-leather", "Black Leather Shoes", "Classic smart lace-ups", "Shoes"),
    ("shoes-black-canvas", "Black Canvas Shoes", "Gripped soles · lace-up", "Shoes"),
    ("shoes-lol", "L.O.L Character Sneakers", "Fun character kicks for little ones", "Shoes"),
]

for slug, _ in GALLERY:
    im = Image.open(HERE / "insta" / f"{slug}.jpg").convert("RGB")
    w, h = im.size
    if max(w, h) > 800:
        scale = 800 / max(w, h)
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.save(WEB / f"gal-{slug}.jpg", "JPEG", quality=80, optimize=True)

for slug in CAT_PHOTOS:
    im = Image.open(HERE / "insta" / f"{slug}.jpg").convert("RGB")
    w, h = im.size
    tw, th = (w, round(w * 3 / 4)) if h >= w * 3 / 4 else (round(h * 4 / 3), h)
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w + tw) // 2, (h + th) // 2))
    if im.width > 720:
        im = im.resize((720, 540), Image.LANCZOS)
    im.save(WEB / f"cat-{slug}.jpg", "JPEG", quality=80, optimize=True)

# showroom product covers (4:3, same crop as category cards)
for slug, *_ in SHOWROOM:
    im = Image.open(HERE / "insta" / f"{slug}.jpg").convert("RGB")
    w, h = im.size
    tw, th = (w, round(w * 3 / 4)) if h >= w * 3 / 4 else (round(h * 4 / 3), h)
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w + tw) // 2, (h + th) // 2))
    if im.width > 640:
        im = im.resize((640, 480), Image.LANCZOS)
    im.save(WEB / f"shop-{slug}.jpg", "JPEG", quality=80, optimize=True)

gallery_html = "\n".join(
    f'      <figure class="reveal"><img src="__IMG:gal-{slug}__" alt="{alt}" loading="lazy"></figure>'
    for slug, alt in GALLERY
)


def wa_order(name: str) -> str:
    """WhatsApp deep link pre-filled with the product name."""
    msg = f"Hello The School Shop! I'd like to order: {name}"
    return f"https://wa.me/23276602248?text={quote(msg)}"


showroom_html = "\n".join(
    f'      <article class="prod" data-cat="{cat}">'
    f'<div class="prod__media"><img src="__IMG:shop-{slug}__" alt="{name}" loading="lazy"></div>'
    f'<div class="prod__body"><h3>{name}</h3><p>{note}</p>'
    f'<a class="btn btn--green btn--sm" href="{wa_order(name)}" target="_blank" rel="noopener">Order on WhatsApp</a>'
    f'</div></article>'
    for slug, name, note, cat in SHOWROOM
)
chip_cats = list(dict.fromkeys(cat for *_, cat in SHOWROOM))
chips_html = '      <button class="chip is-active" data-filter="all">All</button>\n' + "\n".join(
    f'      <button class="chip" data-filter="{c}">{c}</button>' for c in chip_cats
)

template = (ROOT / "index.template.html").read_text()
hero = logo_svg(embed_font=False, extra_attrs='class="hero__logo"')
page = (template
        .replace("__FONT_TITAN__", titan_b64)
        .replace("__FONT_BALOO__", baloo_b64)
        .replace("__HERO_LOGO__", hero)
        .replace("__GALLERY__", gallery_html)
        .replace("__SHOWROOM_CHIPS__", chips_html)
        .replace("__SHOWROOM__", showroom_html))

# index.html references the generated files (fast, cacheable)
html = re.sub(r"__IMG:([a-z0-9-]+)__", r"assets/web/\1.jpg", page)
(ROOT / "index.html").write_text(html)
print(f"index.html               {len(html):>7,} bytes")

# optional artifact build: same page with photos inlined as data URIs
if len(sys.argv) > 1 and sys.argv[1] == "--artifact":
    def embed(m):
        data = base64.b64encode((WEB / f"{m.group(1)}.jpg").read_bytes()).decode()
        return f"data:image/jpeg;base64,{data}"
    full = re.sub(r"__IMG:([a-z0-9-]+)__", embed, page)
    style = re.search(r"<style>(.*?)</style>", full, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", full, re.S).group(1)
    out = ("<title>The School Shop — Quality school uniforms, made properly</title>\n"
           '<script>document.documentElement.classList.add("js")</script>\n'
           f"<style>{style}</style>\n{body}")
    path = pathlib.Path(sys.argv[2])
    path.write_text(out)
    print(f"{path.name:24} {len(out):>7,} bytes")
