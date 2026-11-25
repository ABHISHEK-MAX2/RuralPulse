import os

with open('TECHNICAL_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
    text = f.read()

html_head = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Karnataka Rural Healthcare Intelligence Platform - Technical Documentation</title>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #0f172a; background-color: #f8fafc; padding: 40px; max-width: 900px; margin: 0 auto; }
h1, h2, h3 { color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
h1 { color: #0d9488; border-bottom: 2px solid #0d9488; }
code { font-family: monospace; background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
pre { background: #0f172a; color: #f8fafc; padding: 16px; border-radius: 8px; overflow-x: auto; font-family: monospace; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; }
th, td { border: 1px solid #cbd5e1; padding: 10px 14px; text-align: left; }
th { background: #0d9488; color: white; }
tr:nth-child(even) { background: #f1f5f9; }
blockquote { border-left: 4px solid #0d9488; padding-left: 16px; color: #475569; font-style: italic; }
</style>
</head>
<body>
<pre style="white-space: pre-wrap; font-family: inherit;">
"""

html_tail = """
</pre>
</body>
</html>
"""

out_path = r"C:\Users\jabhi\Downloads\Karnataka_RuralPulse_Technical_Documentation.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_head + text + html_tail)

print("Created HTML document at:", out_path)
