"""Tiny dependency-free YAML-style frontmatter parser.

Supports the constrained subset AgroManch KB docs use:
- a leading ``---`` ... ``---`` block
- ``key: value`` scalars
- block lists::

      keywords:
        - paddy
        - dhaan

- inline lists: ``keywords: [paddy, dhaan]``

Returns (metadata dict, body). No third-party dependency.
"""

from __future__ import annotations


def _coerce(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _inline_list(value: str) -> list[str]:
    inner = value.strip()[1:-1]
    return [_coerce(x) for x in inner.split(",") if x.strip()]


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Split ``text`` into (metadata, body).

    If there is no frontmatter block, returns ({}, text).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    # Find the closing '---'.
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text

    meta: dict[str, object] = {}
    current_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        # List item under the current key.
        if stripped.startswith("- ") and current_key is not None:
            meta.setdefault(current_key, [])
            lst = meta[current_key]
            if isinstance(lst, list):
                lst.append(_coerce(stripped[2:]))
            continue
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            meta[key] = []  # a block list is expected to follow
        elif value.startswith("[") and value.endswith("]"):
            meta[key] = _inline_list(value)
        else:
            meta[key] = _coerce(value)

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return meta, body
