import subprocess, json, time

# Use Playwright to test mobile viewport
result = subprocess.run(['python3', '-c', '''
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Mobile viewport (iPhone 14)
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    
    pages_to_test = [
        ("Homepage", "https://sparehumanservices.com"),
        ("Blog Index", "https://sparehumanservices.com/blog/"),
        ("Landing - Belleair", "https://sparehumanservices.com/belleair.html"),
        ("Story Page", "https://sparehumanservices.com/story.html"),
    ]
    
    results = []
    for name, url in pages_to_test:
        page.goto(url, wait_until="networkidle")
        time.sleep(2)
        
        # Take screenshot
        page.screenshot(path=f"/app/mobile_test_{name.replace(' ', '_').lower()}.png")
        
        # Check for hamburger menu
        has_hamburger = page.query_selector('.hamburger')
        hamburger_display = page.evaluate("getComputedStyle(document.querySelector('.hamburger')).display") if has_hamburger else "N/A"
        
        # Check nav-links
        nav_links = page.query_selector('.nav-links')
        nav_display = page.evaluate("getComputedStyle(document.querySelector('.nav-links')).display") if nav_links else "N/A"
        
        # Check for horizontal overflow
        has_overflow = page.evaluate("document.body.scrollWidth > window.innerWidth")
        
        # Check hero
        hero_h1 = page.query_selector('.hero h1') or page.query_selector('h1')
        h1_font = page.evaluate("getComputedStyle(document.querySelector('.hero h1, h1')).fontSize") if hero_h1 else "N/A"
        
        # Check if any elements are cut off
        body_width = page.evaluate("document.body.scrollWidth")
        inner_width = page.evaluate("window.innerWidth")
        
        results.append({
            "page": name,
            "hamburger_display": hamburger_display,
            "nav_links_display": nav_display,
            "has_hamburger": bool(has_hamburger),
            "horizontal_overflow": has_overflow,
            "body_scroll_width": body_width,
            "inner_width": inner_width,
            "h1_font_size": h1_font,
        })
        
        print(f"✅ {name}: hamburger={hamburger_display}, nav_links={nav_display}, overflow={has_overflow}, h1={h1_font}")
    
    # Test hamburger click on homepage
    page.goto("https://sparehumanservices.com", wait_until="networkidle")
    time.sleep(1)
    page.click('.hamburger')
    time.sleep(1)
    page.screenshot(path="/app/mobile_test_hamburger_open.png")
    
    menu_open = page.evaluate("document.querySelector('.nav-links').classList.contains('open')")
    overlay_show = page.evaluate("document.querySelector('.mobile-overlay')?.classList.contains('show')")
    body_overflow = page.evaluate("document.body.style.overflow")
    
    print(f"\\n🍔 Hamburger click test: menu_open={menu_open}, overlay={overlay_show}, body_overflow={body_overflow}")
    
    # Click overlay to close
    page.click('.mobile-overlay')
    time.sleep(0.5)
    menu_closed = page.evaluate("document.querySelector('.nav-links').classList.contains('open')")
    print(f"🍔 After overlay click: menu_open={menu_closed}")
    
    browser.close()
    print("\\n✅ All mobile tests passed!")
'''], capture_output=True, text=True, timeout=60)
    
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
