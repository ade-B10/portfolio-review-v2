"""
Post-process the StaticCrypt index.html to apply Base10 branding to the
password-prompt landing page.

Preserves all StaticCrypt JS (decryption logic) and the form element IDs
that the JS wires to (#staticrypt-password, #staticrypt-form,
#staticrypt-remember, #staticrypt-remember-label, #staticrypt_loading,
#staticrypt_content). Only the CSS and the visual markup around the form
are replaced.

Run this after every `./update.sh`. Or wire it into update.sh as the final
step.
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "index.html"
html = INDEX.read_text()


# ----- 1. Replace the <style>...</style> block in <head> -----
BASE10_LANDING_CSS = """
<style>
    :root {
        --b10-blue: #45AEEB;
        --b10-blue-hover: #26A6ED;
        --b10-black: #1A1A1A;
        --bg: #FFFFFF;
        --surface-2: #F4F8FB;
        --border: #E5E9EE;
        --text: #1A1A1A;
        --text-dim: #4B5563;
        --text-muted: #6C757D;
    }
    * { box-sizing: border-box; }
    html, body {
        margin: 0; padding: 0; height: 100%;
        background: var(--bg); color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    .staticrypt-top-bar { height: 6px; background: var(--b10-blue); }
    .staticrypt-content {
        min-height: calc(100% - 6px);
        display: flex; align-items: center; justify-content: center;
        padding: 40px 20px;
    }
    .staticrypt-page { width: 100%; max-width: 420px; }
    .staticrypt-brand {
        text-align: center;
        margin-bottom: 28px;
    }
    .staticrypt-brand-name {
        font-weight: 800; font-size: 22px; letter-spacing: -0.4px; color: var(--text);
    }
    .staticrypt-brand-name sup { color: var(--b10-blue); font-weight: 800; font-size: 0.72em; }
    .staticrypt-brand-sub {
        margin-top: 6px; font-size: 12px; color: var(--text-muted);
        letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600;
    }
    .staticrypt-form {
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 32px 28px;
    }
    .staticrypt-instructions {
        margin-bottom: 18px;
        text-align: center;
    }
    .staticrypt-title {
        font-size: 18px; font-weight: 700; letter-spacing: -0.3px;
        color: var(--text); margin: 0 0 6px 0;
    }
    .staticrypt-instructions p:last-child {
        font-size: 13px; color: var(--text-dim); margin: 0; line-height: 1.5;
    }
    .staticrypt-hr {
        border: 0; border-top: 1px solid var(--border);
        margin: 18px 0;
    }
    .staticrypt-password-container {
        position: relative;
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 8px;
        margin: 0 0 14px 0;
        transition: border-color 0.15s ease;
    }
    .staticrypt-password-container:focus-within {
        border-color: var(--b10-blue);
    }
    .staticrypt-form input[type="password"],
    .staticrypt-form input[type="text"] {
        background: transparent;
        border: 0;
        outline: 0;
        font-size: 14px;
        font-family: inherit;
        color: var(--text);
        padding: 14px 44px 14px 14px;
        width: 100%;
    }
    .staticrypt-toggle-password-visibility {
        cursor: pointer;
        height: 18px; width: 18px;
        opacity: 0.5;
        padding: 13px;
        position: absolute;
        right: 0; top: 50%;
        transform: translateY(-50%);
    }
    .staticrypt-toggle-password-visibility:hover { opacity: 0.8; }
    label.staticrypt-remember {
        display: flex; align-items: center; gap: 10px;
        font-size: 13px; color: var(--text-dim);
        margin: 0 0 16px 0; cursor: pointer;
    }
    .staticrypt-remember input[type="checkbox"] {
        accent-color: var(--b10-blue);
        width: 16px; height: 16px;
        margin: 0;
    }
    .staticrypt-decrypt-button {
        width: 100%;
        background: var(--b10-blue);
        color: #FFFFFF;
        border: 0;
        border-radius: 8px;
        padding: 14px;
        font-family: inherit;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        cursor: pointer;
        transition: background-color 0.15s ease;
    }
    .staticrypt-decrypt-button:hover,
    .staticrypt-decrypt-button:active,
    .staticrypt-decrypt-button:focus {
        background: var(--b10-blue-hover);
    }
    .staticrypt-footer {
        text-align: center;
        margin-top: 24px;
        font-size: 11px;
        color: var(--text-muted);
        letter-spacing: 0.3px;
    }
    .hidden { display: none !important; }
    .staticrypt-spinner-container {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .staticrypt-spinner {
        display: inline-block;
        width: 2rem; height: 2rem;
        border: 0.25em solid var(--border);
        border-right-color: var(--b10-blue);
        border-radius: 50%;
        animation: spinner-border 0.75s linear infinite;
    }
    @keyframes spinner-border {
        100% { transform: rotate(360deg); }
    }
    @media (max-width: 480px) {
        .staticrypt-form { padding: 24px 20px; }
        .staticrypt-content { padding: 20px 12px; }
    }
</style>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
"""

html = re.sub(
    r"<style>.*?</style>",
    BASE10_LANDING_CSS.strip(),
    html,
    count=1,
    flags=re.DOTALL,
)


# ----- 2. Replace the body content between <body...> and the first <script> -----
# We need to preserve the form structure (IDs + button) and the password-toggle <img> exactly,
# so we extract the existing password toggle <img> tag and inject it into the new markup.

img_match = re.search(r'<img\s+class="staticrypt-toggle-password-visibility"[^>]*?/>', html, re.DOTALL)
toggle_img = img_match.group(0) if img_match else '<img class="staticrypt-toggle-password-visibility" />'

# Pull out the dynamic instructions/label that staticrypt injected (so we keep them)
title_match = re.search(r'<p class="staticrypt-title">([^<]*)</p>', html)
title_text = title_match.group(1) if title_match else "Base10 Portfolio Review"

instr_match = re.search(r'<div class="staticrypt-instructions">\s*<p class="staticrypt-title">[^<]*</p>\s*<p>([^<]*)</p>\s*</div>', html)
instr_text = instr_match.group(1) if instr_match else ""


BASE10_BODY = f"""<body class="staticrypt-body">
    <div id="staticrypt_loading" class="staticrypt-spinner-container">
        <div class="staticrypt-spinner"></div>
    </div>

    <div id="staticrypt_content" class="staticrypt-content hidden">
        <div class="staticrypt-top-bar"></div>
        <div class="staticrypt-page">
            <div class="staticrypt-brand">
                <div class="staticrypt-brand-name">Base<sup>10</sup> Partners</div>
                <div class="staticrypt-brand-sub">Confidential · Portfolio Review</div>
            </div>
            <div class="staticrypt-form">
                <div class="staticrypt-instructions">
                    <p class="staticrypt-title">{title_text}</p>
                    <p>{instr_text}</p>
                </div>

                <hr class="staticrypt-hr" />

                <form id="staticrypt-form" action="#" method="post">
                    <div class="staticrypt-password-container">
                        <input
                            id="staticrypt-password"
                            type="password"
                            name="password"
                            placeholder="Password"
                            autofocus
                        />
                        {toggle_img}
                    </div>

                    <label id="staticrypt-remember-label" class="staticrypt-remember hidden">
                        <input id="staticrypt-remember" type="checkbox" name="remember" />
                        Remember me on this device for 14 days
                    </label>

                    <input type="submit" class="staticrypt-decrypt-button" value="Unlock" />
                </form>
            </div>
            <div class="staticrypt-footer">© Base10 Partners</div>
        </div>
    </div>
"""

# Replace the body content up to the first <script> (which carries the StaticCrypt JS)
html = re.sub(
    r'<body class="staticrypt-body">.*?(<script>)',
    BASE10_BODY + r"\n    \1",
    html,
    count=1,
    flags=re.DOTALL,
)

# The top-bar is also visible during loading; move it outside the hidden content.
# But actually loading is on body without content visible — the top bar is fine inside #staticrypt_content
# Keep the current approach.

# ----- 3. Bonus: also style the spinner top-bar visible during load -----
html = html.replace(
    '<div id="staticrypt_loading" class="staticrypt-spinner-container">',
    '<div class="staticrypt-top-bar"></div>\n        <div id="staticrypt_loading" class="staticrypt-spinner-container">',
    1,
)

INDEX.write_text(html)
print(f"OK — wrote {len(html):,} bytes")
print(f"Brand block present: {'Base<sup>10</sup> Partners' in html}")
print(f"B10 blue color present: {'#45AEEB' in html}")
print(f"Form IDs preserved: " + ", ".join([f"#{i}" for i in ("staticrypt-form","staticrypt-password","staticrypt-remember","staticrypt-remember-label","staticrypt_content","staticrypt_loading") if f'id="{i}"' in html]))
