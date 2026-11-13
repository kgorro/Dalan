"""Assembles web/sugbo-guide.html, a self-contained page (router and knowledge base inline).

    python web/build_page.py
"""
from pathlib import Path

WEB = Path(__file__).parent
ROOT = WEB.parent
page = (WEB / "page.html").read_text(encoding="utf-8")
page = (page.replace("/*__ROUTER__*/", (WEB / "router.js").read_text(encoding="utf-8"))
            .replace("/*__KB__*/null", (ROOT / "kb" / "kb.json").read_text(encoding="utf-8")))
(WEB / "sugbo-guide.html").write_text(page, encoding="utf-8")
print("wrote web/sugbo-guide.html", len(page) // 1024, "KB")
