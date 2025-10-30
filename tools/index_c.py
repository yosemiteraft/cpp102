#!/usr/bin/env python3
"""
Tiny C indexer: scans .c/.h files to build a lightweight symbol and call graph.
Outputs JSON with functions per file, their outgoing calls, and a callers map.

Usage:
  python3 tools/index_c.py <root> [<output_json>]

Defaults:
  root = current working directory
  output_json = .vscode/code-index.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


KW_EXCLUDE_CALL = {
    "if", "for", "while", "switch", "return", "sizeof", "case", "do"
}

KW_NOT_FUNC_NAMES = KW_EXCLUDE_CALL | {"typedef", "struct", "enum", "union"}


def strip_comments_and_strings(code: str) -> str:
    # Remove // and /* */ comments and string/char literals to reduce false positives
    def replacer(match: re.Match[str]) -> str:
        s = match.group(0)
        if s.startswith('/'):
            return ' ' * len(s)
        # string/char literal -> keep length to preserve positions
        return '"' + (' ' * (len(s) - 2)) + '"' if len(s) >= 2 else ''

    pattern = re.compile(
        r"//.*?$|/\*.*?\*/|'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"",
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, code)


def find_function_defs(code: str) -> List[Tuple[str, int, int]]:
    """
    Find function definitions: returns list of (name, body_start_index, body_end_index)
    Very heuristic but good enough for small C samples.
    """
    stripped = strip_comments_and_strings(code)
    # Regex: return_type qualifiers optional, then name(...){
    func_pat = re.compile(
        r"(^|\n)\s*(?:[A-Za-z_][\w\s\*\[\]]+?\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;{}]*)\)\s*\{",
        re.MULTILINE,
    )
    defs: List[Tuple[str, int, int]] = []
    for m in func_pat.finditer(stripped):
        name = m.group(2)
        # Filter out likely non-function constructs
        if name in KW_NOT_FUNC_NAMES:
            continue
        body_start = m.end() - 1  # position at '{'
        # Find matching closing brace to get body end
        depth = 0
        i = body_start
        n = len(stripped)
        while i < n:
            ch = stripped[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    defs.append((name, body_start + 1, i))
                    break
            i += 1
    return defs


def find_calls(body: str) -> List[str]:
    calls: List[str] = []
    # Look for identifiers followed by '('; exclude control keywords
    call_pat = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    for m in call_pat.finditer(body):
        name = m.group(1)
        if name in KW_EXCLUDE_CALL:
            continue
        calls.append(name)
    return calls


def index_file(path: Path) -> Dict:
    text = path.read_text(encoding='utf-8', errors='ignore')
    defs = find_function_defs(text)
    functions = []
    for name, bstart, bend in defs:
        body = strip_comments_and_strings(text[bstart:bend])
        calls = find_calls(body)
        functions.append({
            "name": name,
            "returnType": "?",
            "params": [],
            "calls": calls,
        })
    return {"path": str(path.name), "functions": functions}


def walk_sources(root: Path) -> List[Path]:
    ex_dirs = {".git", "build", "dist", "out", "node_modules", "venv", "__pycache__"}
    paths: List[Path] = []
    for p in root.rglob('*'):
        if p.is_dir():
            if p.name in ex_dirs:
                # Skip descending into excluded dirs
                for _ in p.rglob('*'):
                    pass
                continue
        elif p.suffix in ('.c', '.h'):
            paths.append(p)
    return paths


def build_callers(files: List[Dict]) -> Dict[str, List[str]]:
    callers: Dict[str, Set[str]] = {}
    for f in files:
        for fn in f.get("functions", []):
            fname = fn["name"]
            callers.setdefault(fname, set())
    for f in files:
        for fn in f.get("functions", []):
            src = fn["name"]
            for callee in fn.get("calls", []):
                if callee not in callers:
                    callers[callee] = set()
                callers[callee].add(src)
    return {k: sorted(v) for k, v in sorted(callers.items())}


def main(argv: List[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    out_path = Path(argv[2]) if len(argv) > 2 else root / '.vscode' / 'code-index.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    files_idx: List[Dict] = []
    for src in walk_sources(root):
        files_idx.append(index_file(src))

    callers = build_callers(files_idx)
    data = {
        "generatedAt": __import__('datetime').datetime.utcnow().isoformat() + 'Z',
        "language": "c",
        "files": files_idx,
        "callers": callers,
    }
    out_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f"Wrote index to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
