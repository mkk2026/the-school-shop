#!/usr/bin/env python3
"""Build The School Shop site: generates logo.svg and index.html from index.template.html.

- logo.svg  : standalone, Titan One embedded as base64 (works anywhere, incl. <img>)
- index.html: template with fonts embedded and the hero logo inlined (inherits page font)
"""
import base64
import pathlib

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

# 2. instagram photo tiles (real posts, embedded so index.html stays self-contained)
TILES = [
    ("shirts", "Slim fit blue and white school shirts on our superstars"),
    ("trousers", "Grey school trousers and shorts with adjustable waists"),
    ("skirts-pleated", "Pleated school skirts with permanent pleats"),
    ("shoes", "School shoes with glitter stripe trims and gripped soles"),
    ("skirts-senior", "Senior girls two-pleat skirts"),
    ("uniforms-supplies", "Top-quality uniforms and school supplies"),
]
tiles_html = []
for name, alt in TILES:
    img_b64 = base64.b64encode((HERE / "insta" / f"{name}.sq.jpg").read_bytes()).decode()
    tiles_html.append(
        f'      <a class="tile tile--photo reveal" href="https://www.instagram.com/the_school_shop_/"'
        f' target="_blank" rel="noopener" title="{alt}">'
        f'<img src="data:image/jpeg;base64,{img_b64}" alt="{alt}" loading="lazy"></a>'
    )

template = (ROOT / "index.template.html").read_text()
hero = logo_svg(embed_font=False, extra_attrs='class="hero__logo"')
html = (template
        .replace("__FONT_TITAN__", titan_b64)
        .replace("__FONT_BALOO__", baloo_b64)
        .replace("__HERO_LOGO__", hero)
        .replace("__INSTA_TILES__", "\n".join(tiles_html)))
(ROOT / "index.html").write_text(html)
print(f"index.html               {len(html):>7,} bytes")
