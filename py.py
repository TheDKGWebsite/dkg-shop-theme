#!/usr/bin/env python3
"""
DKG Shop Theme - Mobile Homepage Collection Plate Inspector

READ-ONLY inspector for WooCommerce / WordPress theme mobile homepage overhaul.

Run from theme repo root:
    python inspect_mobile_homepage_overhaul.py

Outputs:
    _dkg_mobile_homepage_inspection_YYYY-MM-DD_HH-MM-SS/
        inspection_report.md
        findings.json
        all_matched_snippets.txt
        likely_dom_structure.md

Uses only Python standard library.
Makes no edits.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


# -----------------------------
# Configuration
# -----------------------------

TEXT_EXTENSIONS = {
    ".php", ".css", ".js", ".json", ".html", ".htm", ".txt", ".md",
    ".scss", ".sass", ".less", ".xml", ".inc", ".twig"
}

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "vendor",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "cache",
    ".cache",
    "coverage",
}

CORE_FILES = [
    "functions.php",
    "assets/css/front-page.css",
    "assets/js/dkg-mobile-main-homepage-plates.js",
    "front-page.php",
    "header.php",
    "page-mobile-shop.php",
]

MOBILE_MARKERS = [
    "DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES",
    "dkg-mobile-main-homepage-plates",
    "dkg-mobile-carousel-viewport",
    "dkg-mobile-product-track",
    "dkg-mobile-product-item",
    "dkg-mobile-original-product-source",
    "dkg-mobile-original-track-source",
    "dkg-mobile-product-clone",
]

MOBILE_REDIRECT_TERMS = [
    "dkg_redirect_mobile_shop_visitors",
    "template_redirect",
    "wp_is_mobile",
    "/mobile-shop/",
    "mobile-shop",
    "page-mobile-shop.php",
]

COLLECTION_DOM_TERMS = [
    "collections-stack",
    "collection-link",
    "collection-box",
    "collection-bg",
    "collection-label",
    "product-image",
    "ul.products",
    "products",
    "product",
    "woocommerce",
]

CSS_SELECTORS_OF_INTEREST = [
    ".collections-stack",
    ".collection-link",
    ".collection-box",
    ".collection-bg",
    ".collection-label",
    ".product-image",
    "ul.products",
    ".products",
    ".product",
    ".dkg-mobile-carousel-viewport",
    ".dkg-mobile-product-track",
    ".dkg-mobile-product-item",
    ".dkg-mobile-original-product-source",
    ".dkg-mobile-original-track-source",
    ".dkg-mobile-product-clone",
    ".mobile-shop",
]

CSS_PROPERTIES_OF_INTEREST = [
    "background",
    "background-image",
    "background-size",
    "background-position",
    "background-repeat",
    "overflow",
    "position",
    "transform",
    "translate",
    "z-index",
    "object-fit",
    "display",
    "grid",
    "flex",
    "width",
    "height",
    "max-width",
    "min-width",
    "left",
    "right",
    "top",
    "bottom",
    "margin",
    "padding",
    "gap",
    "justify-content",
    "align-items",
    "visibility",
    "opacity",
]

JS_TERMS_OF_INTEREST = [
    "collection",
    "collections-stack",
    "collection-box",
    "collection-bg",
    "collection-label",
    "product",
    "product-image",
    "dkg-mobile",
    "carousel",
    "viewport",
    "track",
    "clone",
    "setInterval",
    "setTimeout",
    "requestAnimationFrame",
    "transform",
    "translateX",
    "scroll",
    "classList",
    "querySelector",
    "querySelectorAll",
    "appendChild",
    "insertBefore",
    "remove",
    "style.",
    "matchMedia",
    "innerWidth",
    "resize",
    "DOMContentLoaded",
]

ENQUEUE_TERMS = [
    "wp_enqueue_script",
    "wp_enqueue_style",
    "dkg-mobile-main-homepage-plates",
    "front-page.css",
    "mobile-shop",
]

BACKGROUND_TERMS = [
    "collection-bg",
    "background",
    "background-image",
    "background-size",
    "background-position",
    "background-repeat",
]


# -----------------------------
# Data containers
# -----------------------------

@dataclass
class MatchRecord:
    file: str
    line: int
    term: str
    category: str
    snippet: str


@dataclass
class FileSummary:
    path: str
    exists: bool
    line_count: int = 0
    size_bytes: int = 0
    marker_counts: Dict[str, int] = None
    redirect_counts: Dict[str, int] = None
    collection_term_counts: Dict[str, int] = None


# -----------------------------
# Utility functions
# -----------------------------

def safe_read_text(path: Path) -> Optional[str]:
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    for enc in encodings:
        try:
            return path.read_text(encoding=enc, errors="replace")
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def is_probably_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def iter_repo_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIR_NAMES and not d.startswith("_dkg_mobile_homepage_inspection_")
        ]
        current = Path(dirpath)
        for filename in filenames:
            path = current / filename
            if is_probably_text_file(path):
                files.append(path)
    return sorted(files)


def line_number_for_index(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def get_lines(text: str) -> List[str]:
    return text.splitlines()


def snippet_around_line(text: str, line_no: int, context: int = 8) -> str:
    lines = get_lines(text)
    start = max(1, line_no - context)
    end = min(len(lines), line_no + context)

    out = []
    for n in range(start, end + 1):
        marker = ">>" if n == line_no else "  "
        line = lines[n - 1] if n - 1 < len(lines) else ""
        out.append(f"{marker} {n:5d}: {line}")
    return "\n".join(out)


def count_occurrences_case_insensitive(text: str, term: str) -> int:
    return len(re.findall(re.escape(term), text, flags=re.IGNORECASE))


def find_matches(
    root: Path,
    files: List[Path],
    terms: List[str],
    category: str,
    context: int = 8,
) -> List[MatchRecord]:
    records: List[MatchRecord] = []

    for path in files:
        text = safe_read_text(path)
        if text is None:
            continue

        for term in terms:
            for match in re.finditer(re.escape(term), text, flags=re.IGNORECASE):
                line_no = line_number_for_index(text, match.start())
                records.append(
                    MatchRecord(
                        file=relpath(path, root),
                        line=line_no,
                        term=term,
                        category=category,
                        snippet=snippet_around_line(text, line_no, context=context),
                    )
                )

    return records


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", errors="replace")


def make_heading(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}\n\n"


def fence(text: str, language: str = "") -> str:
    return f"```{language}\n{text.rstrip()}\n```\n\n"


def compact_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# -----------------------------
# CSS analysis
# -----------------------------

def extract_css_blocks(text: str) -> List[Tuple[int, str, str]]:
    """
    Lightweight CSS block extractor.
    Returns tuples:
        line_number, selector_text, block_text
    Handles @media blocks imperfectly but usefully for inspection.
    """
    blocks: List[Tuple[int, str, str]] = []

    i = 0
    n = len(text)

    while i < n:
        brace = text.find("{", i)
        if brace == -1:
            break

        selector_start = max(text.rfind("}", 0, brace), text.rfind(";", 0, brace), text.rfind("\n\n", 0, brace))
        selector = text[selector_start + 1:brace].strip()

        if not selector:
            i = brace + 1
            continue

        depth = 1
        j = brace + 1
        in_string: Optional[str] = None
        escaped = False

        while j < n and depth > 0:
            ch = text[j]

            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == in_string:
                    in_string = None
            else:
                if ch in ("'", '"'):
                    in_string = ch
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
            j += 1

        block = text[brace + 1:j - 1] if j <= n else text[brace + 1:]
        line_no = line_number_for_index(text, max(0, selector_start + 1))
        blocks.append((line_no, selector, block))
        i = j

    return blocks


def css_block_matches(selector: str, block: str) -> bool:
    selector_lower = selector.lower()
    block_lower = block.lower()

    selector_hit = any(sel.lower() in selector_lower for sel in CSS_SELECTORS_OF_INTEREST)
    prop_hit = any(prop.lower() in block_lower for prop in CSS_PROPERTIES_OF_INTEREST)
    background_hit = "background" in block_lower and any(
        term.lower() in selector_lower or term.lower() in block_lower
        for term in ["collection", "product", "plate", "mobile", "homepage", "front-page"]
    )
    media_hit = "@media" in selector_lower or "@media" in block_lower

    return (selector_hit and prop_hit) or background_hit or (media_hit and (selector_hit or "dkg-mobile" in block_lower))


def analyze_css_files(root: Path, files: List[Path]) -> List[Dict[str, Any]]:
    css_findings: List[Dict[str, Any]] = []

    for path in files:
        if path.suffix.lower() not in {".css", ".scss", ".sass", ".less", ".php"}:
            continue

        text = safe_read_text(path)
        if not text:
            continue

        blocks = extract_css_blocks(text)
        for line_no, selector, block in blocks:
            if css_block_matches(selector, block):
                css_findings.append({
                    "file": relpath(path, root),
                    "line": line_no,
                    "selector": selector.strip(),
                    "block": block.strip(),
                    "properties_detected": sorted([
                        prop for prop in CSS_PROPERTIES_OF_INTEREST
                        if re.search(rf"(^|[\s{{;]){re.escape(prop)}\s*:", block, flags=re.IGNORECASE)
                    ]),
                    "contains_media": "@media" in selector.lower() or "@media" in block.lower(),
                    "contains_background": "background" in block.lower(),
                    "contains_mobile_marker": "dkg mobile" in block.lower() or "dkg-mobile" in block.lower(),
                })

    return css_findings


# -----------------------------
# JS analysis
# -----------------------------

def extract_js_functionish_blocks(text: str) -> List[Tuple[int, str]]:
    """
    Lightweight JS block extractor around important terms.
    This is intentionally broad and line based.
    """
    lines = text.splitlines()
    hits: List[int] = []

    for i, line in enumerate(lines, start=1):
        low = line.lower()
        if any(term.lower() in low for term in JS_TERMS_OF_INTEREST):
            hits.append(i)

    # Merge nearby hits
    ranges: List[Tuple[int, int]] = []
    for line_no in hits:
        start = max(1, line_no - 12)
        end = min(len(lines), line_no + 18)
        if ranges and start <= ranges[-1][1] + 3:
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
        else:
            ranges.append((start, end))

    blocks = []
    for start, end in ranges:
        block_lines = [f"{n:5d}: {lines[n - 1]}" for n in range(start, end + 1)]
        blocks.append((start, "\n".join(block_lines)))

    return blocks


def analyze_js_files(root: Path, files: List[Path]) -> List[Dict[str, Any]]:
    js_findings: List[Dict[str, Any]] = []

    for path in files:
        if path.suffix.lower() not in {".js", ".php"}:
            continue

        text = safe_read_text(path)
        if not text:
            continue

        lower = text.lower()
        if not any(term.lower() in lower for term in JS_TERMS_OF_INTEREST + MOBILE_MARKERS):
            continue

        blocks = extract_js_functionish_blocks(text)
        for line_no, block in blocks:
            js_findings.append({
                "file": relpath(path, root),
                "line": line_no,
                "terms_detected": sorted([
                    term for term in JS_TERMS_OF_INTEREST + MOBILE_MARKERS
                    if term.lower() in block.lower()
                ]),
                "block": block,
            })

    return js_findings


# -----------------------------
# PHP / DOM analysis
# -----------------------------

CLASS_ATTR_RE = re.compile(r'class\s*=\s*([\'"])(.*?)\1', re.IGNORECASE | re.DOTALL)
ID_ATTR_RE = re.compile(r'id\s*=\s*([\'"])(.*?)\1', re.IGNORECASE | re.DOTALL)
HTML_TAG_RE = re.compile(r'<([a-zA-Z0-9:-]+)([^>]*)>', re.DOTALL)


def extract_classes_and_ids(root: Path, files: List[Path]) -> Dict[str, Any]:
    class_map: Dict[str, List[Dict[str, Any]]] = {}
    id_map: Dict[str, List[Dict[str, Any]]] = {}

    for path in files:
        if path.suffix.lower() not in {".php", ".html", ".htm", ".js"}:
            continue

        text = safe_read_text(path)
        if not text:
            continue

        for m in CLASS_ATTR_RE.finditer(text):
            raw = compact_ws(m.group(2))
            line_no = line_number_for_index(text, m.start())
            for cls in raw.split():
                if not cls:
                    continue
                class_map.setdefault(cls, []).append({
                    "file": relpath(path, root),
                    "line": line_no,
                    "raw_class_attribute": raw,
                })

        for m in ID_ATTR_RE.finditer(text):
            raw = compact_ws(m.group(2))
            line_no = line_number_for_index(text, m.start())
            id_map.setdefault(raw, []).append({
                "file": relpath(path, root),
                "line": line_no,
            })

    return {"classes": class_map, "ids": id_map}


def extract_relevant_html_snippets(root: Path, files: List[Path]) -> List[Dict[str, Any]]:
    snippets: List[Dict[str, Any]] = []

    interesting = [
        "collections-stack",
        "collection-link",
        "collection-box",
        "collection-bg",
        "collection-label",
        "product-image",
        "woocommerce",
        "products",
        "product",
        "mobile-shop",
    ]

    for path in files:
        if path.suffix.lower() not in {".php", ".html", ".htm"}:
            continue

        text = safe_read_text(path)
        if not text:
            continue

        lower = text.lower()
        if not any(term.lower() in lower for term in interesting):
            continue

        lines = text.splitlines()
        hit_lines = []
        for i, line in enumerate(lines, start=1):
            if any(term.lower() in line.lower() for term in interesting):
                hit_lines.append(i)

        # Merge nearby ranges
        ranges = []
        for line_no in hit_lines:
            start = max(1, line_no - 10)
            end = min(len(lines), line_no + 18)
            if ranges and start <= ranges[-1][1] + 5:
                ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
            else:
                ranges.append((start, end))

        for start, end in ranges:
            block = "\n".join(f"{n:5d}: {lines[n - 1]}" for n in range(start, end + 1))
            snippets.append({
                "file": relpath(path, root),
                "line": start,
                "block": block,
                "terms_detected": sorted([
                    term for term in interesting
                    if term.lower() in block.lower()
                ]),
            })

    return snippets


def infer_dom_structure(html_snippets: List[Dict[str, Any]], css_findings: List[Dict[str, Any]], js_findings: List[Dict[str, Any]]) -> str:
    out: List[str] = []
    out.append("# Likely DOM Structure Reconstruction\n")
    out.append("This is an evidence-based reconstruction from PHP/HTML snippets, CSS selectors, and JS selectors. It may not perfectly match runtime DOM if WooCommerce hooks or JS mutate the page after load.\n\n")

    key_classes = [
        "collections-stack",
        "collection-link",
        "collection-box",
        "collection-bg",
        "collection-label",
        "product-image",
        "products",
        "product",
        "dkg-mobile-carousel-viewport",
        "dkg-mobile-product-track",
        "dkg-mobile-product-item",
        "dkg-mobile-original-product-source",
        "dkg-mobile-original-track-source",
        "dkg-mobile-product-clone",
    ]

    out.append("## Classes Found in Relevant Evidence\n\n")
    evidence_by_class: Dict[str, Dict[str, List[str]]] = {cls: {"html": [], "css": [], "js": []} for cls in key_classes}

    for snip in html_snippets:
        block = snip["block"]
        for cls in key_classes:
            if cls in block:
                evidence_by_class[cls]["html"].append(f'{snip["file"]}: line {snip["line"]}')

    for css in css_findings:
        combined = css["selector"] + "\n" + css["block"]
        for cls in key_classes:
            if cls in combined:
                evidence_by_class[cls]["css"].append(f'{css["file"]}: line {css["line"]}')

    for js in js_findings:
        block = js["block"]
        for cls in key_classes:
            if cls in block:
                evidence_by_class[cls]["js"].append(f'{js["file"]}: line {js["line"]}')

    for cls in key_classes:
        ev = evidence_by_class[cls]
        if ev["html"] or ev["css"] or ev["js"]:
            out.append(f"### `.{cls}`\n\n")
            if ev["html"]:
                out.append("- HTML/PHP evidence:\n")
                for item in sorted(set(ev["html"])):
                    out.append(f"  - {item}\n")
            if ev["css"]:
                out.append("- CSS evidence:\n")
                for item in sorted(set(ev["css"])):
                    out.append(f"  - {item}\n")
            if ev["js"]:
                out.append("- JS evidence:\n")
                for item in sorted(set(ev["js"])):
                    out.append(f"  - {item}\n")
            out.append("\n")

    out.append("## Probable Collection Plate Shape\n\n")
    out.append("Based on requested selectors and common homepage structure, inspect whether the actual snippets below confirm or contradict this shape:\n\n")
    out.append("```text\n")
    out.append(".collections-stack\n")
    out.append("  .collection-link\n")
    out.append("    .collection-box\n")
    out.append("      .collection-bg                  <-- should be background/decor only if possible\n")
    out.append("      .collection-label               <-- title/tab should not be inside moving carousel track\n")
    out.append("      original product row / products <-- location must be confirmed\n")
    out.append("      .dkg-mobile-carousel-viewport   <-- Step 7 clone layer, if present\n")
    out.append("        .dkg-mobile-product-track\n")
    out.append("          .dkg-mobile-product-item / .dkg-mobile-product-clone\n")
    out.append("```\n\n")

    out.append("## High-Risk Structure Questions to Confirm from Report\n\n")
    out.append("- Is the original product row inside `.collection-bg`? If yes, hiding the original row with a broad parent selector may also damage the background.\n")
    out.append("- Is `.collection-bg` receiving cloned products or a track? If yes, the background may repeat/glitch because the decorative layer is being used as a content container.\n")
    out.append("- Is `.collection-label` inside a transformed or cloned element? If yes, the title/tab can shift or duplicate during carousel setup.\n")
    out.append("- Are mobile carousel wrappers inserted more than once on resize or repeated initialization? If yes, backgrounds/titles/products may duplicate.\n")
    out.append("- Are old mobile-shop selectors still matching the normal homepage? If yes, old mobile rules can fight the new responsive homepage rules.\n\n")

    out.append("## Relevant HTML/PHP Evidence Blocks\n\n")
    if not html_snippets:
        out.append("No relevant PHP/HTML snippets found.\n\n")
    else:
        for snip in html_snippets:
            out.append(f'### {snip["file"]} around line {snip["line"]}\n\n')
            out.append(f'Terms: {", ".join(snip["terms_detected"])}\n\n')
            out.append(fence(snip["block"], ""))

    return "".join(out)


# -----------------------------
# Deeper heuristics
# -----------------------------

def detect_duplicate_marker_blocks(root: Path, files: List[Path]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    for marker in MOBILE_MARKERS:
        occurrences = []
        for path in files:
            text = safe_read_text(path)
            if not text:
                continue
            for m in re.finditer(re.escape(marker), text, flags=re.IGNORECASE):
                occurrences.append({
                    "file": relpath(path, root),
                    "line": line_number_for_index(text, m.start())
                })
        result[marker] = {
            "count": len(occurrences),
            "occurrences": occurrences,
            "appears_more_than_once": len(occurrences) > 1,
        }

    return result


def detect_enqueues(root: Path, files: List[Path]) -> Dict[str, Any]:
    enqueues: List[Dict[str, Any]] = []

    enqueue_re = re.compile(
        r'wp_enqueue_(script|style)\s*\((.*?)\)\s*;',
        flags=re.IGNORECASE | re.DOTALL
    )

    for path in files:
        if path.suffix.lower() != ".php":
            continue

        text = safe_read_text(path)
        if not text:
            continue

        for m in enqueue_re.finditer(text):
            call = m.group(0)
            if any(term.lower() in call.lower() for term in ENQUEUE_TERMS):
                enqueues.append({
                    "file": relpath(path, root),
                    "line": line_number_for_index(text, m.start()),
                    "type": m.group(1).lower(),
                    "call": compact_ws(call),
                    "snippet": snippet_around_line(text, line_number_for_index(text, m.start()), context=8),
                })

    handle_counts: Dict[str, int] = {}
    for item in enqueues:
        call = item["call"]
        handle_match = re.search(r'wp_enqueue_(?:script|style)\s*\(\s*([\'"])(.*?)\1', call, flags=re.IGNORECASE)
        if handle_match:
            handle = handle_match.group(2)
            handle_counts[handle] = handle_counts.get(handle, 0) + 1

    return {
        "enqueues": enqueues,
        "handle_counts": handle_counts,
        "potential_duplicate_handles": {
            handle: count for handle, count in handle_counts.items() if count > 1
        },
        "dkg_mobile_js_enqueue_count": sum(
            1 for e in enqueues
            if "dkg-mobile-main-homepage-plates" in e["call"].lower()
        ),
    }


def detect_mobile_redirects(root: Path, files: List[Path]) -> List[Dict[str, Any]]:
    redirects: List[Dict[str, Any]] = []

    for path in files:
        if path.suffix.lower() != ".php":
            continue

        text = safe_read_text(path)
        if not text:
            continue

        lower = text.lower()
        if not any(term.lower() in lower for term in MOBILE_REDIRECT_TERMS):
            continue

        lines = text.splitlines()
        hit_lines = []
        for i, line in enumerate(lines, start=1):
            if any(term.lower() in line.lower() for term in MOBILE_REDIRECT_TERMS):
                hit_lines.append(i)

        ranges = []
        for line_no in hit_lines:
            start = max(1, line_no - 12)
            end = min(len(lines), line_no + 18)
            if ranges and start <= ranges[-1][1] + 5:
                ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
            else:
                ranges.append((start, end))

        for start, end in ranges:
            block = "\n".join(f"{n:5d}: {lines[n - 1]}" for n in range(start, end + 1))
            redirects.append({
                "file": relpath(path, root),
                "line": start,
                "terms_detected": sorted([
                    term for term in MOBILE_REDIRECT_TERMS
                    if term.lower() in block.lower()
                ]),
                "block": block,
            })

    return redirects


def detect_mobile_shop_influence(root: Path, files: List[Path]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    terms = ["mobile-shop", "page-mobile-shop", "/mobile-shop/", "is_page('mobile-shop')", 'is_page("mobile-shop")']

    for path in files:
        text = safe_read_text(path)
        if not text:
            continue

        lower = text.lower()
        if not any(term.lower() in lower for term in terms):
            continue

        for term in terms:
            for m in re.finditer(re.escape(term), text, flags=re.IGNORECASE):
                line_no = line_number_for_index(text, m.start())
                findings.append({
                    "file": relpath(path, root),
                    "line": line_no,
                    "term": term,
                    "snippet": snippet_around_line(text, line_no, context=10),
                })

    return findings


def detect_collection_bg_as_container(html_snippets: List[Dict[str, Any]], js_findings: List[Dict[str, Any]], css_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence = {
        "html_collection_bg_near_products": [],
        "js_collection_bg_targeting": [],
        "css_collection_bg_layout_rules": [],
        "risk_summary": [],
    }

    for snip in html_snippets:
        block_lower = snip["block"].lower()
        if "collection-bg" in block_lower and any(term in block_lower for term in ["product", "products", "product-image", "woocommerce"]):
            evidence["html_collection_bg_near_products"].append({
                "file": snip["file"],
                "line": snip["line"],
                "block": snip["block"],
            })

    for js in js_findings:
        block_lower = js["block"].lower()
        if "collection-bg" in block_lower:
            evidence["js_collection_bg_targeting"].append({
                "file": js["file"],
                "line": js["line"],
                "terms_detected": js["terms_detected"],
                "block": js["block"],
            })

    for css in css_findings:
        combined = (css["selector"] + "\n" + css["block"]).lower()
        if "collection-bg" in combined and any(prop in combined for prop in ["display", "position", "overflow", "transform", "z-index", "background"]):
            evidence["css_collection_bg_layout_rules"].append({
                "file": css["file"],
                "line": css["line"],
                "selector": css["selector"],
                "properties_detected": css["properties_detected"],
                "block": css["block"],
            })

    if evidence["js_collection_bg_targeting"]:
        evidence["risk_summary"].append("JS targets `.collection-bg`; verify it is not appending carousel nodes into the decorative background layer.")
    if evidence["html_collection_bg_near_products"]:
        evidence["risk_summary"].append("HTML/PHP evidence places `.collection-bg` near product markup; verify parent/child relationship before hiding original rows.")
    if evidence["css_collection_bg_layout_rules"]:
        evidence["risk_summary"].append("CSS layout/background rules affect `.collection-bg`; broad mobile overrides may cause repeated/glitchy background rendering.")

    return evidence


def detect_images_vs_backgrounds(root: Path, files: List[Path]) -> Dict[str, Any]:
    result = {
        "img_tags_near_product_or_collection": [],
        "background_image_rules_or_inline_styles": [],
    }

    img_re = re.compile(r'<img\b[^>]*>', flags=re.IGNORECASE | re.DOTALL)
    bg_re = re.compile(r'(background(?:-image)?\s*:\s*[^;}{]+|style\s*=\s*["\'][^"\']*background[^"\']*["\'])', flags=re.IGNORECASE | re.DOTALL)

    for path in files:
        if path.suffix.lower() not in {".php", ".html", ".htm", ".css", ".js"}:
            continue

        text = safe_read_text(path)
        if not text:
            continue

        for m in img_re.finditer(text):
            tag = compact_ws(m.group(0))
            if any(term in tag.lower() for term in ["product", "collection", "woocommerce", "image", "src"]):
                line_no = line_number_for_index(text, m.start())
                result["img_tags_near_product_or_collection"].append({
                    "file": relpath(path, root),
                    "line": line_no,
                    "tag": tag[:500],
                    "snippet": snippet_around_line(text, line_no, context=5),
                })

        for m in bg_re.finditer(text):
            rule = compact_ws(m.group(0))
            context_text = text[max(0, m.start() - 300): min(len(text), m.end() + 300)]
            if any(term in context_text.lower() for term in ["collection", "product", "plate", "mobile", "front-page", "homepage"]):
                line_no = line_number_for_index(text, m.start())
                result["background_image_rules_or_inline_styles"].append({
                    "file": relpath(path, root),
                    "line": line_no,
                    "rule": rule[:500],
                    "snippet": snippet_around_line(text, line_no, context=6),
                })

    return result


def find_woocommerce_template_files(root: Path, files: List[Path]) -> List[str]:
    candidates = []

    for path in files:
        rp = relpath(path, root)
        low = rp.lower()
        if (
            "woocommerce" in low
            or "wc-" in low
            or "product" in low
            or "archive-product" in low
            or "content-product" in low
            or "single-product" in low
        ):
            candidates.append(rp)

    return sorted(set(candidates))


def summarize_core_files(root: Path) -> List[FileSummary]:
    summaries: List[FileSummary] = []

    for rel in CORE_FILES:
        path = root / rel
        exists = path.exists()
        summary = FileSummary(
            path=rel,
            exists=exists,
            marker_counts={},
            redirect_counts={},
            collection_term_counts={},
        )

        if exists:
            text = safe_read_text(path) or ""
            summary.line_count = len(text.splitlines())
            try:
                summary.size_bytes = path.stat().st_size
            except OSError:
                summary.size_bytes = 0
            summary.marker_counts = {
                term: count_occurrences_case_insensitive(text, term)
                for term in MOBILE_MARKERS
            }
            summary.redirect_counts = {
                term: count_occurrences_case_insensitive(text, term)
                for term in MOBILE_REDIRECT_TERMS
            }
            summary.collection_term_counts = {
                term: count_occurrences_case_insensitive(text, term)
                for term in COLLECTION_DOM_TERMS
            }

        summaries.append(summary)

    return summaries


# -----------------------------
# Report generation
# -----------------------------

def generate_markdown_report(findings: Dict[str, Any]) -> str:
    out: List[str] = []

    out.append("# DKG Mobile Homepage Collection Plate Inspection Report\n\n")
    out.append(f"Generated: `{findings['generated_at']}`\n\n")
    out.append(f"Repo root: `{findings['repo_root']}`\n\n")
    out.append("This report is read-only evidence collection. It does not apply fixes.\n\n")

    out.append(make_heading("Executive Summary", 2))

    duplicate_markers = {
        k: v for k, v in findings["duplicate_marker_blocks"].items()
        if v["appears_more_than_once"]
    }
    duplicate_enqueues = findings["enqueue_analysis"]["potential_duplicate_handles"]
    dkg_js_enqueue_count = findings["enqueue_analysis"]["dkg_mobile_js_enqueue_count"]

    out.append(f"- Files scanned: **{findings['file_count']}**\n")
    out.append(f"- Mobile marker matches: **{len(findings['mobile_marker_matches'])}**\n")
    out.append(f"- Mobile redirect matches: **{len(findings['mobile_redirect_matches'])}**\n")
    out.append(f"- CSS blocks of interest: **{len(findings['css_findings'])}**\n")
    out.append(f"- JS blocks of interest: **{len(findings['js_findings'])}**\n")
    out.append(f"- WooCommerce/product-related template candidates: **{len(findings['woocommerce_template_files'])}**\n")
    out.append(f"- `dkg-mobile-main-homepage-plates` enqueue count: **{dkg_js_enqueue_count}**\n")
    if duplicate_markers:
        out.append(f"- Duplicate mobile marker terms detected: **{len(duplicate_markers)}**\n")
    else:
        out.append("- Duplicate mobile marker terms detected: **none based on exact marker search**\n")
    if duplicate_enqueues:
        out.append(f"- Potential duplicate enqueue handles: **{', '.join(duplicate_enqueues.keys())}**\n")
    else:
        out.append("- Potential duplicate enqueue handles: **none based on handle extraction**\n")
    out.append("\n")

    out.append(make_heading("Core File Summary", 2))
    out.append("| File | Exists | Lines | Size | Mobile marker hits | Redirect hits | Collection term hits |\n")
    out.append("|---|---:|---:|---:|---:|---:|---:|\n")
    for fs in findings["core_file_summaries"]:
        marker_hits = sum(fs["marker_counts"].values()) if fs["marker_counts"] else 0
        redirect_hits = sum(fs["redirect_counts"].values()) if fs["redirect_counts"] else 0
        collection_hits = sum(fs["collection_term_counts"].values()) if fs["collection_term_counts"] else 0
        out.append(
            f"| `{fs['path']}` | {fs['exists']} | {fs['line_count']} | {fs['size_bytes']} | "
            f"{marker_hits} | {redirect_hits} | {collection_hits} |\n"
        )
    out.append("\n")

    out.append(make_heading("Likely High-Risk Areas", 2))
    risks = []

    bg_risks = findings["collection_bg_container_analysis"]["risk_summary"]
    risks.extend(bg_risks)

    if findings["duplicate_marker_blocks"]:
        for marker, info in findings["duplicate_marker_blocks"].items():
            if info["appears_more_than_once"]:
                risks.append(f"Marker `{marker}` appears {info['count']} times; previous updater blocks may be duplicated or overlapping.")

    if dkg_js_enqueue_count > 1:
        risks.append("The mobile homepage JS appears to be enqueued more than once.")

    if findings["mobile_shop_influence"]:
        risks.append("References to `mobile-shop` still exist; verify these are not loading CSS/JS or body classes that affect the normal homepage.")

    if not risks:
        risks.append("No obvious duplicate/enqueue/background-container risk was detected by the heuristic checks. Review snippets below for exact structure.")

    for r in risks:
        out.append(f"- {r}\n")
    out.append("\n")

    out.append(make_heading("Recommended Next-Step Strategy", 2))
    out.append(
        "No updater should be written until the report confirms the real runtime structure. "
        "Based on the current symptom, the next fix will probably need to separate three responsibilities cleanly:\n\n"
    )
    out.append("1. **Background layer**: `.collection-bg` should remain decorative only and should not become a carousel/product container.\n")
    out.append("2. **Title/tab layer**: `.collection-label` should stay outside any moving/cloned/translated track and should have a stable centering rule.\n")
    out.append("3. **Product layer**: mobile carousel should operate in its own viewport/track wrapper, with the original product source hidden only at the safest narrow selector level.\n\n")
    out.append(
        "After reviewing this report, the fix should target the smallest confirmed selectors instead of broad mobile rules. "
        "Special attention should go to whether previous Step 7 clone wrappers are being inserted repeatedly and whether hiding the original row is also hiding or moving the plate background/title.\n\n"
    )

    out.append(make_heading("Duplicate Marker Analysis", 2))
    for marker, info in findings["duplicate_marker_blocks"].items():
        out.append(f"### `{marker}`\n\n")
        out.append(f"- Count: **{info['count']}**\n")
        out.append(f"- Appears more than once: **{info['appears_more_than_once']}**\n")
        if info["occurrences"]:
            for occ in info["occurrences"]:
                out.append(f"  - `{occ['file']}` line {occ['line']}\n")
        out.append("\n")

    out.append(make_heading("Enqueue Analysis", 2))
    out.append(f"- `dkg-mobile-main-homepage-plates` enqueue count: **{dkg_js_enqueue_count}**\n\n")
    if findings["enqueue_analysis"]["handle_counts"]:
        out.append("### Enqueue Handle Counts\n\n")
        for handle, count in sorted(findings["enqueue_analysis"]["handle_counts"].items()):
            out.append(f"- `{handle}`: {count}\n")
        out.append("\n")

    for item in findings["enqueue_analysis"]["enqueues"]:
        out.append(f"### `{item['file']}` line {item['line']}\n\n")
        out.append(f"- Type: `{item['type']}`\n")
        out.append(f"- Call: `{item['call']}`\n\n")
        out.append(fence(item["snippet"], ""))

    out.append(make_heading("Mobile Redirect and `/mobile-shop/` Analysis", 2))
    if not findings["mobile_redirect_blocks"]:
        out.append("No mobile redirect blocks found from the configured search terms.\n\n")
    else:
        for block in findings["mobile_redirect_blocks"]:
            out.append(f"### `{block['file']}` around line {block['line']}\n\n")
            out.append(f"Terms: {', '.join(block['terms_detected'])}\n\n")
            out.append(fence(block["block"], ""))

    out.append(make_heading("Old Mobile-Shop Influence", 2))
    if not findings["mobile_shop_influence"]:
        out.append("No `mobile-shop` influence matches found beyond configured redirect scan.\n\n")
    else:
        for item in findings["mobile_shop_influence"]:
            out.append(f"### `{item['file']}` line {item['line']} — `{item['term']}`\n\n")
            out.append(fence(item["snippet"], ""))

    out.append(make_heading("Collection Background Container Risk Check", 2))
    bg = findings["collection_bg_container_analysis"]

    out.append("### Risk Summary\n\n")
    if bg["risk_summary"]:
        for r in bg["risk_summary"]:
            out.append(f"- {r}\n")
    else:
        out.append("- No direct `.collection-bg` container risk detected by heuristics.\n")
    out.append("\n")

    for section_key, section_title in [
        ("html_collection_bg_near_products", "HTML/PHP `.collection-bg` Near Products"),
        ("js_collection_bg_targeting", "JS Targeting `.collection-bg`"),
        ("css_collection_bg_layout_rules", "CSS Layout Rules Affecting `.collection-bg`"),
    ]:
        out.append(f"### {section_title}\n\n")
        items = bg[section_key]
        if not items:
            out.append("No matches.\n\n")
        else:
            for item in items:
                out.append(f"#### `{item['file']}` line {item['line']}\n\n")
                if "selector" in item:
                    out.append(f"Selector: `{item['selector']}`\n\n")
                    out.append(f"Properties: `{', '.join(item.get('properties_detected', []))}`\n\n")
                    out.append(fence(item["block"], "css"))
                else:
                    out.append(fence(item["block"], ""))

    out.append(make_heading("Product Images: `<img>` Tags vs Background Images", 2))
    imgs = findings["image_vs_background_analysis"]

    out.append("### `<img>` Tags Near Product/Collection Markup\n\n")
    if not imgs["img_tags_near_product_or_collection"]:
        out.append("No relevant `<img>` tags found by heuristic scan.\n\n")
    else:
        for item in imgs["img_tags_near_product_or_collection"][:80]:
            out.append(f"#### `{item['file']}` line {item['line']}\n\n")
            out.append(f"Tag: `{item['tag']}`\n\n")
            out.append(fence(item["snippet"], ""))

    out.append("### Background Image Rules or Inline Background Styles\n\n")
    if not imgs["background_image_rules_or_inline_styles"]:
        out.append("No relevant background image rules/inline styles found by heuristic scan.\n\n")
    else:
        for item in imgs["background_image_rules_or_inline_styles"][:120]:
            out.append(f"#### `{item['file']}` line {item['line']}\n\n")
            out.append(f"Rule: `{item['rule']}`\n\n")
            out.append(fence(item["snippet"], ""))

    out.append(make_heading("CSS Blocks of Interest", 2))
    if not findings["css_findings"]:
        out.append("No CSS blocks matched the configured selectors/properties.\n\n")
    else:
        for css in findings["css_findings"]:
            out.append(f"### `{css['file']}` line {css['line']}\n\n")
            out.append(f"Selector:\n\n```css\n{css['selector']}\n```\n\n")
            out.append(f"Properties detected: `{', '.join(css['properties_detected'])}`\n\n")
            if css["contains_media"]:
                out.append("Contains media-related context: **yes**\n\n")
            if css["contains_background"]:
                out.append("Contains background rule: **yes**\n\n")
            out.append(fence(css["block"], "css"))

    out.append(make_heading("JS Blocks of Interest", 2))
    if not findings["js_findings"]:
        out.append("No JS blocks matched the configured carousel/product/mobile terms.\n\n")
    else:
        for js in findings["js_findings"]:
            out.append(f"### `{js['file']}` around line {js['line']}\n\n")
            out.append(f"Terms: `{', '.join(js['terms_detected'])}`\n\n")
            out.append(fence(js["block"], "js"))

    out.append(make_heading("Full Mobile Marker Matches", 2))
    if not findings["mobile_marker_matches"]:
        out.append("No exact mobile overhaul marker matches found.\n\n")
    else:
        for m in findings["mobile_marker_matches"]:
            out.append(f"### `{m['file']}` line {m['line']} — `{m['term']}`\n\n")
            out.append(fence(m["snippet"], ""))

    out.append(make_heading("Collection / Product DOM Term Matches", 2))
    if not findings["collection_dom_matches"]:
        out.append("No collection/product DOM term matches found.\n\n")
    else:
        for m in findings["collection_dom_matches"]:
            out.append(f"### `{m['file']}` line {m['line']} — `{m['term']}`\n\n")
            out.append(fence(m["snippet"], ""))

    out.append(make_heading("WooCommerce / Product Template Candidate Files", 2))
    if not findings["woocommerce_template_files"]:
        out.append("No WooCommerce/product template candidate files found.\n\n")
    else:
        for path in findings["woocommerce_template_files"]:
            out.append(f"- `{path}`\n")
        out.append("\n")

    out.append(make_heading("Relevant HTML/PHP Snippets", 2))
    if not findings["html_snippets"]:
        out.append("No relevant HTML/PHP snippets found.\n\n")
    else:
        for snip in findings["html_snippets"]:
            out.append(f"### `{snip['file']}` around line {snip['line']}\n\n")
            out.append(f"Terms: `{', '.join(snip['terms_detected'])}`\n\n")
            out.append(fence(snip["block"], ""))

    out.append(make_heading("Class and ID Inventory: Relevant Subset", 2))
    classes = findings["class_id_inventory"]["classes"]
    ids = findings["class_id_inventory"]["ids"]

    relevant_classes = sorted([
        cls for cls in classes.keys()
        if any(term.lower() in cls.lower() for term in [
            "collection", "product", "woocommerce", "mobile", "carousel", "track", "viewport", "label", "image"
        ])
    ])

    out.append("### Relevant Classes\n\n")
    if not relevant_classes:
        out.append("No relevant classes found.\n\n")
    else:
        for cls in relevant_classes:
            out.append(f"#### `.{cls}`\n\n")
            for loc in classes[cls][:20]:
                out.append(f"- `{loc['file']}` line {loc['line']} — class attr: `{loc['raw_class_attribute']}`\n")
            if len(classes[cls]) > 20:
                out.append(f"- ...and {len(classes[cls]) - 20} more occurrences\n")
            out.append("\n")

    relevant_ids = sorted([
        idv for idv in ids.keys()
        if any(term.lower() in idv.lower() for term in [
            "collection", "product", "woocommerce", "mobile", "carousel", "track", "viewport"
        ])
    ])

    out.append("### Relevant IDs\n\n")
    if not relevant_ids:
        out.append("No relevant IDs found.\n\n")
    else:
        for idv in relevant_ids:
            out.append(f"#### `#{idv}`\n\n")
            for loc in ids[idv][:20]:
                out.append(f"- `{loc['file']}` line {loc['line']}\n")
            if len(ids[idv]) > 20:
                out.append(f"- ...and {len(ids[idv]) - 20} more occurrences\n")
            out.append("\n")

    return "".join(out)


def generate_all_snippets_text(findings: Dict[str, Any]) -> str:
    out: List[str] = []
    out.append("DKG Mobile Homepage Collection Plate Inspector - All Matched Snippets\n")
    out.append(f"Generated: {findings['generated_at']}\n")
    out.append(f"Repo root: {findings['repo_root']}\n")
    out.append("=" * 100 + "\n\n")

    groups = [
        ("MOBILE MARKER MATCHES", findings["mobile_marker_matches"]),
        ("MOBILE REDIRECT MATCHES", findings["mobile_redirect_matches"]),
        ("COLLECTION DOM MATCHES", findings["collection_dom_matches"]),
    ]

    for title, records in groups:
        out.append(title + "\n")
        out.append("-" * len(title) + "\n\n")
        if not records:
            out.append("No matches.\n\n")
            continue

        for r in records:
            out.append(f"[{r['category']}] {r['file']}:{r['line']} term={r['term']}\n")
            out.append(r["snippet"])
            out.append("\n\n" + "-" * 100 + "\n\n")

    out.append("CSS FINDINGS\n")
    out.append("------------\n\n")
    for css in findings["css_findings"]:
        out.append(f"{css['file']}:{css['line']} selector={css['selector']}\n")
        out.append(css["block"])
        out.append("\n\n" + "-" * 100 + "\n\n")

    out.append("JS FINDINGS\n")
    out.append("-----------\n\n")
    for js in findings["js_findings"]:
        out.append(f"{js['file']}:{js['line']} terms={', '.join(js['terms_detected'])}\n")
        out.append(js["block"])
        out.append("\n\n" + "-" * 100 + "\n\n")

    return "".join(out)


# -----------------------------
# Main
# -----------------------------

def main() -> int:
    root = Path.cwd().resolve()

    # Basic sanity check.
    if not (root / "functions.php").exists():
        print("WARNING: functions.php was not found in the current directory.")
        print("This script is intended to run from the root of the WordPress theme repo.")
        print(f"Current directory: {root}")
        print("Continuing anyway...\n")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = root / f"_dkg_mobile_homepage_inspection_{timestamp}"
    report_dir.mkdir(parents=True, exist_ok=False)

    files = iter_repo_files(root)

    print(f"Scanning repo: {root}")
    print(f"Text files found: {len(files)}")
    print(f"Report folder: {report_dir}")

    mobile_marker_matches = find_matches(root, files, MOBILE_MARKERS, "mobile_marker", context=10)
    mobile_redirect_matches = find_matches(root, files, MOBILE_REDIRECT_TERMS, "mobile_redirect", context=10)
    collection_dom_matches = find_matches(root, files, COLLECTION_DOM_TERMS, "collection_dom", context=8)

    css_findings = analyze_css_files(root, files)
    js_findings = analyze_js_files(root, files)
    html_snippets = extract_relevant_html_snippets(root, files)
    class_id_inventory = extract_classes_and_ids(root, files)

    duplicate_marker_blocks = detect_duplicate_marker_blocks(root, files)
    enqueue_analysis = detect_enqueues(root, files)
    mobile_redirect_blocks = detect_mobile_redirects(root, files)
    mobile_shop_influence = detect_mobile_shop_influence(root, files)
    image_vs_background_analysis = detect_images_vs_backgrounds(root, files)
    woocommerce_template_files = find_woocommerce_template_files(root, files)
    core_file_summaries = summarize_core_files(root)

    collection_bg_container_analysis = detect_collection_bg_as_container(
        html_snippets=html_snippets,
        js_findings=js_findings,
        css_findings=css_findings,
    )

    findings: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(root),
        "file_count": len(files),
        "scanned_files": [relpath(p, root) for p in files],
        "core_file_summaries": [asdict(x) for x in core_file_summaries],
        "mobile_marker_matches": [asdict(x) for x in mobile_marker_matches],
        "mobile_redirect_matches": [asdict(x) for x in mobile_redirect_matches],
        "collection_dom_matches": [asdict(x) for x in collection_dom_matches],
        "css_findings": css_findings,
        "js_findings": js_findings,
        "html_snippets": html_snippets,
        "class_id_inventory": class_id_inventory,
        "duplicate_marker_blocks": duplicate_marker_blocks,
        "enqueue_analysis": enqueue_analysis,
        "mobile_redirect_blocks": mobile_redirect_blocks,
        "mobile_shop_influence": mobile_shop_influence,
        "collection_bg_container_analysis": collection_bg_container_analysis,
        "image_vs_background_analysis": image_vs_background_analysis,
        "woocommerce_template_files": woocommerce_template_files,
    }

    report_md = generate_markdown_report(findings)
    all_snippets_txt = generate_all_snippets_text(findings)
    dom_md = infer_dom_structure(html_snippets, css_findings, js_findings)

    write_text(report_dir / "inspection_report.md", report_md)
    write_text(report_dir / "all_matched_snippets.txt", all_snippets_txt)
    write_text(report_dir / "likely_dom_structure.md", dom_md)

    with (report_dir / "findings.json").open("w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    print("\nDone. Created:")
    print(f"  {report_dir / 'inspection_report.md'}")
    print(f"  {report_dir / 'findings.json'}")
    print(f"  {report_dir / 'all_matched_snippets.txt'}")
    print(f"  {report_dir / 'likely_dom_structure.md'}")

    print("\nBest next step:")
    print("  Paste/upload inspection_report.md and likely_dom_structure.md first.")
    print("  If the report is huge, start with Executive Summary, High-Risk Areas,")
    print("  Collection Background Container Risk Check, CSS Blocks, and JS Blocks.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())