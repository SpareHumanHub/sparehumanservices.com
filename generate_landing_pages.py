#!/usr/bin/env python3
"""Generate service area landing pages for beach municipalities near Largo, FL."""

import json
import os

# City data — will be populated from sub-agent research
CITIES = [
    {
        "slug": "clearwater-beach",
        "name": "Clearwater Beach",
        "short": "Clearwater Beach",
        "distance": "15 minutes",
        "vibe": "tourist",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
    {
        "slug": "indian-rocks-beach",
        "name": "Indian Rocks Beach",
        "short": "Indian Rocks Beach",
        "distance": "10 minutes",
        "vibe": "residential",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
    {
        "slug": "treasure-island",
        "name": "Treasure Island",
        "short": "Treasure Island",
        "distance": "12 minutes",
        "vibe": "tourist",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
    {
        "slug": "belleair",
        "name": "Belleair",
        "short": "Belleair",
        "distance": "8 minutes",
        "vibe": "affluent",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
    {
        "slug": "st-pete-beach",
        "name": "St. Pete Beach",
        "short": "St. Pete Beach",
        "distance": "20 minutes",
        "vibe": "tourist",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
    {
        "slug": "redington-beach",
        "name": "Redington Beach & Redington Shores",
        "short": "Redington Beach",
        "distance": "12 minutes",
        "vibe": "residential",
        "landmarks": [],
        "parks": [],
        "vets": [],
        "body_paragraphs": [],
    },
]

NAV_HTML = """    <a href="/#services">Services</a>
        <a href="/#why">Why Us</a>
        <a href="/blog/">Blog</a>
        <a href="/#reviews">Reviews</a>
        <a href="/review.html" style="color:#5eead4;">Review</a>
        <a href="/#faq">FAQ</a>
        <a href="/story.html">My Story</a>
        <a href="/intake.html" style="color:#5eead4;">New Clients</a>"""

FOOTER_HTML = """  <footer>
    <img src="/logo.jpg" alt="Spare Human Services" style="height:56px;width:56px;object-fit:contain;border-radius:10px;background:white;padding:4px;margin:0 auto 16px;display:block;" />
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/#services">Services</a>
      <a href="/blog/">Blog</a>
      <a href="/#reviews">Reviews</a>
      <a href="/review.html">Review</a>
      <a href="/#faq">FAQ</a>
      <a href="/story.html">My Story</a>
      <a href="/intake.html">New Clients</a>
      <a href="https://www.instagram.com/sparehumanserviceslargo/">Instagram</a>
      <a href="https://www.facebook.com/profile.php?id=61578634487102">Facebook</a>
      <a href="https://www.youtube.com/@sparehumanserviceslargo">YouTube</a>
      <a href="https://www.google.com/maps/search/?api=1&query=spare+human+services+largo+fl">Google</a>
    </div>
    <p>Spare Human Services · Largo, FL · <a href="tel:7273866349">727-386-6349</a> · <a href="mailto:ryan@sparehumanservices.com">ryan@sparehumanservices.com</a> · Licensed &amp; Insured</p>
  </footer>"""

TAWK_SCRIPT = """<!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/6a4ac51e731e1b1d41fab0a9/1jsq1404f';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
<!--End of Tawk.to Script-->"""


def generate_page(city):
    slug = city["slug"]
    name = city["name"]
    short = city["short"]
    distance = city["distance"]

    title = f"Dog Walking & Pet Sitting in {name} | Spare Human Services"
    desc = f"Licensed & insured dog walking, pet sitting, drop-in visits, and overnight care in {name}, FL. GPS-tracked walks, photo updates, and availability starting at 6am. Book online."
    h1 = f"Dog Walking & Pet Sitting in <span class=\"teal\">{short}</span>"

    # Build body content
    body_html = ""
    for para in city.get("body_paragraphs", []):
        body_html += f"      <p>{para}</p>\n"

    # Build landmarks list
    landmarks_html = ""
    for lm in city.get("landmarks", []):
        landmarks_html += f"          <li>{lm}</li>\n"

    # Build parks list
    parks_html = ""
    for park in city.get("parks", []):
        parks_html += f"          <li>{park}</li>\n"

    # Schema
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Spare Human Services",
        "description": f"Licensed and insured dog walking and pet sitting in {name}, FL.",
        "url": f"https://sparehumanservices.com/{slug}.html",
        "telephone": "727-386-6349",
        "priceRange": "$$",
        "areaServed": {
            "@type": "City",
            "name": name
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Largo",
            "addressRegion": "FL",
            "addressCountry": "US"
        },
        "sameAs": [
            "https://www.instagram.com/sparehumanserviceslargo/",
            "https://www.facebook.com/profile.php?id=61578634487102",
            "https://www.youtube.com/@sparehumanserviceslargo",
            "https://www.rover.com/sit/ryanr08753"
        ]
    }, indent=2)

    breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://sparehumanservices.com/"},
            {"@type": "ListItem", "position": 2, "name": short, "item": f"https://sparehumanservices.com/{slug}.html"}
        ]
    }, indent=2)

    # Services list
    services = [
        ("Dog Walking", "30 min $18 · 60 min $33 · +$5/additional dog", "Daily walks with GPS tracking and photo updates."),
        ("Drop-In Visits", "15 min $16 · 30 min $24", "Quick check-ins for feeding, potty breaks, and playtime."),
        ("In-Home Pet Sitting", "$20/hr · $18/hr for 4+ hour bundles", "Extended care while you're at work or away for the day."),
        ("Overnight Care", "$100 flat · 10pm–6am", "Your pet stays comfortable at home overnight."),
        ("Pet Taxi", "$20 each way (under 5 miles)", "Vet appointments, grooming, or the park."),
    ]

    services_html = ""
    for svc_name, svc_price, svc_desc in services:
        services_html += f"""        <div class="svc-card">
          <div class="svc-name">{svc_name}</div>
          <div class="svc-price">{svc_price}</div>
          <div class="svc-desc">{svc_desc}</div>
        </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-2LPSWZJV8T"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-2LPSWZJV8T');
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://sparehumanservices.com/{slug}.html" />
  <link rel="icon" href="/logo.jpg" />
  <link rel="apple-touch-icon" href="/logo.jpg" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://sparehumanservices.com/{slug}.html" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://media.base44.com/images/public/69b358bf8e7e209b630af346/ce840434c_ColorLogo.jpg" />
  <meta property="og:site_name" content="Spare Human Services" />
  <meta property="og:locale" content="en_US" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://media.base44.com/images/public/69b358bf8e7e209b630af346/ce840434c_ColorLogo.jpg" />

  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; background: #0a1628; color: #e8eef5; line-height: 1.7; }}
    a {{ text-decoration: none; color: inherit; }}

    /* Nav */
    .nav-wrap {{ position: sticky; top: 0; z-index: 100; background: rgba(10,22,40,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(94,234,212,0.12); }}
    .nav {{ max-width: 1200px; margin: 0 auto; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; }}
    .nav-logo {{ font-weight: 800; font-size: 1.25rem; color: #5eead4; display: flex; align-items: center; gap: 8px; }}
    .nav-links {{ display: flex; gap: 28px; align-items: center; }}
    .nav-links a {{ font-size: 0.88rem; font-weight: 600; color: #8ba3c0; }}
    .nav-links a:hover {{ color: #5eead4; }}
    .nav-phone {{ background: #5eead4; color: #0a1628; padding: 10px 22px; border-radius: 100px; font-weight: 800; font-size: 0.88rem; }}

    /* Hero */
    .hero {{ text-align: center; padding: 64px 24px 40px; max-width: 900px; margin: 0 auto; }}
    .hero-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(94,234,212,0.12); border: 1px solid rgba(94,234,212,0.3); color: #5eead4; padding: 8px 18px; border-radius: 100px; font-size: 0.78rem; font-weight: 700; margin-bottom: 20px; }}
    .hero h1 {{ font-size: clamp(2rem, 4.5vw, 2.8rem); font-weight: 800; line-height: 1.15; color: #fff; margin-bottom: 14px; }}
    .hero h1 .teal {{ color: #5eead4; }}
    .hero p {{ font-size: 1.1rem; color: #8ba3c0; line-height: 1.6; max-width: 600px; margin: 0 auto; }}

    /* Content */
    .content {{ max-width: 800px; margin: 0 auto; padding: 20px 24px 60px; }}
    .content p {{ font-size: 1.05rem; color: #c8d6e5; line-height: 1.85; margin-bottom: 20px; }}

    /* Local highlights */
    .highlights {{ max-width: 800px; margin: 0 auto; padding: 0 24px 60px; }}
    .highlight-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(94,234,212,0.12); border-radius: 20px; padding: 28px; margin-bottom: 20px; }}
    .highlight-card h3 {{ font-size: 1.15rem; font-weight: 700; color: #5eead4; margin-bottom: 12px; }}
    .highlight-card ul {{ list-style: none; }}
    .highlight-card li {{ font-size: 0.95rem; color: #c8d6e5; padding: 6px 0 6px 20px; position: relative; }}
    .highlight-card li::before {{ content: '▸'; position: absolute; left: 0; color: #5eead4; }}

    /* Services */
    .services {{ max-width: 800px; margin: 0 auto; padding: 0 24px 60px; }}
    .services h2 {{ font-size: 1.6rem; font-weight: 800; color: #fff; margin-bottom: 24px; text-align: center; }}
    .svc-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
    .svc-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; transition: all 0.2s; }}
    .svc-card:hover {{ background: rgba(94,234,212,0.06); border-color: rgba(94,234,212,0.2); }}
    .svc-name {{ font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 6px; }}
    .svc-price {{ font-size: 0.95rem; font-weight: 700; color: #5eead4; margin-bottom: 8px; }}
    .svc-desc {{ font-size: 0.88rem; color: #8ba3c0; }}

    /* CTA */
    .cta {{ text-align: center; max-width: 700px; margin: 0 auto 80px; padding: 0 24px; }}
    .cta-card {{ background: linear-gradient(135deg, rgba(94,234,212,0.08), rgba(15,52,96,0.3)); border: 1px solid rgba(94,234,212,0.2); border-radius: 28px; padding: 48px 36px; }}
    .cta-card h2 {{ font-size: 1.8rem; font-weight: 800; color: #fff; margin-bottom: 12px; }}
    .cta-card p {{ color: #8ba3c0; margin-bottom: 28px; font-size: 1rem; }}
    .cta-btn {{ display: inline-block; background: #5eead4; color: #0a1628; padding: 16px 40px; border-radius: 100px; font-weight: 800; font-size: 1.05rem; box-shadow: 0 8px 32px rgba(94,234,212,0.25); transition: transform 0.15s; }}
    .cta-btn:hover {{ transform: translateY(-2px); }}
    .cta-btn-outline {{ display: inline-block; border: 1px solid rgba(94,234,212,0.4); color: #5eead4; padding: 16px 36px; border-radius: 100px; font-weight: 700; font-size: 1rem; margin-left: 12px; }}
    @media (max-width: 640px) {{ .cta-btn-outline {{ margin-left: 0; margin-top: 12px; }} }}

    /* Footer */
    footer {{ background: #050d1a; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; padding: 40px 24px; font-size: 0.85rem; }}
    footer a {{ color: #5eead4; }}
    .footer-links {{ margin-bottom: 16px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
    .footer-links a {{ color: #8ba3c0; font-weight: 600; font-size: 0.85rem; }}
    footer p {{ color: #6b829e; }}

    /* Mobile */
    @media (max-width: 768px) {{
      .nav-links {{ display: none; }}
      .hero {{ padding: 48px 20px 32px; }}
      .cta-card {{ padding: 32px 24px; }}
    }}
  </style>
  <script type="application/ld+json">
  {schema}
  </script>
  <script type="application/ld+json">
  {breadcrumb}
  </script>
</head>
<body>

  <div class="nav-wrap">
    <div class="nav">
      <a href="/" class="nav-logo"><img src="/logo.jpg" alt="Spare Human Services" style="height:44px;width:44px;object-fit:contain;border-radius:8px;background:white;padding:3px;" /> Spare Human Services</a>
      <div class="nav-links">
{NAV_HTML}
      </div>
      <a class="nav-phone" href="/book.html">Book Now</a>
    </div>
  </div>

  <div class="hero">
    <div class="hero-badge">📍 Serving {short} · {distance} from Largo</div>
    <h1>{h1}</h1>
    <p>Professional, licensed, and insured pet care serving {short} and nearby barrier island communities in Pinellas County. GPS-tracked walks, photo updates, and reliable scheduling — whether you're a year-round resident or visiting for the season.</p>
  </div>

  <div class="content">
{body_html}
  </div>

  <div class="highlights">
    <div class="highlight-card">
      <h3>Pet-Friendly Spots in {short}</h3>
      <ul>
{parks_html}
      </ul>
    </div>
    <div class="highlight-card">
      <h3>Local Landmarks & Community</h3>
      <ul>
{landmarks_html}
      </ul>
    </div>
  </div>

  <div class="services">
    <h2>Services Available in {short}</h2>
    <div class="svc-grid">
{services_html}
    </div>
  </div>

  <div class="cta">
    <div class="cta-card">
      <h2>Ready to Book in {short}?</h2>
      <p>Every new client starts with a free 15-minute meet &amp; greet. Pick a time that works — instant confirmation, no phone tag.</p>
      <a href="/book.html" class="cta-btn">Book a Free Meet &amp; Greet</a>
      <a href="/intake.html" class="cta-btn-outline">New Client Intake</a>
    </div>
  </div>

{FOOTER_HTML}

{TAWK_SCRIPT}
</body>
</html>"""

    return html


# Main
if __name__ == "__main__":
    for city in CITIES:
        html = generate_page(city)
        filename = f"{city['slug']}.html"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"✅ Generated {filename}")
    print(f"\nGenerated {len(CITIES)} landing pages.")
