"""
Parse TRSE Turbo Rascal unit files (.tru) for procedure/function declarations
and preceding block comments. Heuristic lexer — sufficient for shipped units/.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Decl:
    kind: str  # "procedure" | "function"
    name: str
    signature: str  # full line(s) including kind, name, params, modifiers, trailing ;
    doc: str  # comment body before declaration, stripped


def _strip_asm_blocks(s: str) -> str:
    """Replace asm(" ... "); regions with spaces (same length) to hide inner keywords."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if i + 4 <= n and s[i : i + 4].lower() == "asm(":
            j = i + 4
            while j < n and s[j] in " \t\n\r":
                j += 1
            if j < n and s[j] == '"':
                start = i
                j += 1
                while j < n:
                    if s[j] == "\\" and j + 1 < n:
                        j += 2
                        continue
                    if s[j] == '"' and j + 1 < n and s[j + 1] == ")":
                        end = j + 2
                        out.append(" " * (end - start))
                        i = end
                        break
                    j += 1
                else:
                    out.append(s[i])
                    i += 1
            else:
                out.append(s[i])
                i += 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _strip_strings(s: str) -> str:
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == '"':
            start = i
            i += 1
            while i < n:
                if s[i] == "\\" and i + 1 < n:
                    i += 2
                    continue
                if s[i] == '"':
                    i += 1
                    break
                i += 1
            out.append(" " * (i - start))
            continue
        if ch == "'":
            start = i
            i += 1
            while i < n:
                if s[i] == "\\" and i + 1 < n:
                    i += 2
                    continue
                if s[i] == "'":
                    i += 1
                    break
                i += 1
            out.append(" " * (i - start))
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _strip_line_and_block_comments(s: str) -> str:
    """Remove // line comments and replace /* */ blocks with spaces (preserve length)."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if i + 1 < n and s[i : i + 2] == "//":
            start = i
            i += 2
            while i < n and s[i] != "\n":
                i += 1
            out.append(" " * (i - start))
            continue
        if i + 1 < n and s[i : i + 2] == "/*":
            start = i
            i += 2
            while i + 1 < n and s[i : i + 2] != "*/":
                i += 1
            if i + 1 < n and s[i : i + 2] == "*/":
                i += 2
            out.append(" " * (i - start))
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def _is_doc_comment_body(body: str) -> bool:
    """Heuristic: skip block comments that are commented-out code, not documentation."""
    b = body.strip()
    if not b:
        return False
    low = b.lower()
    if 'asm("' in low or "asm('" in low:
        return False
    # Whole commented-out procedure / function
    if re.match(r"^\s*procedure\s+\w", low) or re.match(r"^\s*function\s+\w", low):
        return False
    if "begin" in low and "procedure" in low:
        return False
    return True


def _preceding_block_comment(text: str, proc_start: int) -> str:
    """If a /* */ block ends immediately before proc_start, return inner text."""
    i = proc_start - 1
    while i >= 0 and text[i] in " \t\n\r":
        i -= 1
    if i < 1:
        return ""
    if text[i] != "/" or text[i - 1] != "*":
        return ""
    close_star = i - 1
    j = close_star - 1
    while j > 0:
        if text[j - 1 : j + 1] == "/*":
            body = text[j + 1 : close_star - 1]
            body = body.strip()
            if _is_doc_comment_body(body):
                return body
            return ""
        j -= 1
    return ""


def _parse_signature(text: str, kw_start: int) -> tuple[str, int]:
    """
    From start of 'procedure' or 'function', read until the ';' that ends
    the declaration (after optional modifiers like inline).
    Returns (signature stripped one-line or multi, end index after ';').
    """
    i = kw_start
    n = len(text)
    depth = 0
    started = False
    while i < n:
        c = text[i]
        if c == "(":
            depth += 1
            started = True
        elif c == ")" and depth > 0:
            depth -= 1
        elif c == ";" and depth == 0:
            sig = text[kw_start : i + 1].strip()
            # normalize internal whitespace for display
            sig = re.sub(r"\s+", " ", sig)
            return sig, i + 1
        i += 1
    sig = text[kw_start:].strip()
    sig = re.sub(r"\s+", " ", sig)
    return sig, n


_KEYWORD_RE = re.compile(r"\b(procedure|function)\s+([A-Za-z_][A-Za-z0-9_]*)")


def extract_decls(source: str) -> list[Decl]:
    """
    Extract procedure/function declarations from .tru source.
    Comments (// and /* */) are blanked before matching so commented-out code is ignored.
    """
    cleaned = _strip_asm_blocks(source)
    cleaned = _strip_strings(cleaned)
    cleaned_nocomment = _strip_line_and_block_comments(cleaned)

    decls: list[Decl] = []
    for m in _KEYWORD_RE.finditer(cleaned_nocomment):
        kind, name = m.group(1), m.group(2)
        pos = m.start()
        sig, _end = _parse_signature(cleaned_nocomment, pos)
        doc = _preceding_block_comment(source, pos)
        decls.append(Decl(kind=kind, name=name, signature=sig, doc=doc))

    return decls


def doc_to_markdown(doc: str) -> str:
    """Turn /** */ body into a short markdown-safe line or block."""
    if not doc:
        return ""
    t = doc.replace("**/", "").strip()
    t = re.sub(r"^/\*\*?\s*", "", t)
    t = re.sub(r"\s*\*/$", "", t)
    lines = []
    for line in t.splitlines():
        s = line.strip()
        if s.startswith("*"):
            s = s[1:].strip()
        lines.append(s)
    t = "\n".join(lines).strip()
    # Strip simple HTML tags for plain text summary
    t = re.sub(r"</?p>", "", t, flags=re.I)
    t = re.sub(r"<code>([^<]*)</code>", r"`\1`", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    # Collapse to single line for table cells; keep newlines as space for block quotes
    t = re.sub(r"[\r\n]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = t.replace("|", "\\|")
    return t
