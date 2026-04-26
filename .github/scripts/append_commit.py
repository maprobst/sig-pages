#!/usr/bin/env python3
"""Appends one commit entry as a Markdown table row to docs/commits.md."""
import os
from datetime import datetime

COMMITS_MD = "docs/commits.md"
MARKER = "<!-- COMMITS_END -->"

INITIAL_CONTENT = """\
# Commit Log

> Wird bei jedem Push automatisch aktualisiert.

| Datum | Autor | Branch | Commit | Nachricht |
|:------|:------|:-------|:-------|:----------|
<!-- COMMITS_END -->
"""


def escape_cell(text: str) -> str:
    """Escape pipe characters so they don't break the Markdown table."""
    return text.replace("|", "&#124;").replace("\n", " ")


def main() -> None:
    commit_sha = os.environ["COMMIT_SHA"]
    short_sha  = commit_sha[:7]
    author     = escape_cell(os.environ["COMMIT_AUTHOR"])
    message    = escape_cell(os.environ["COMMIT_MESSAGE"].split("\n")[0])
    timestamp  = os.environ["COMMIT_TIMESTAMP"]
    commit_url = os.environ["COMMIT_URL"]
    branch     = escape_cell(os.environ["BRANCH_NAME"])

    dt       = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    date_str = dt.strftime("%Y-%m-%d %H:%M UTC")

    os.makedirs("docs", exist_ok=True)

    if not os.path.exists(COMMITS_MD):
        with open(COMMITS_MD, "w", encoding="utf-8") as f:
            f.write(INITIAL_CONTENT)

    with open(COMMITS_MD, "r", encoding="utf-8") as f:
        content = f.read()

    if MARKER not in content:
        raise SystemExit(f"ERROR: marker {MARKER!r} not found in {COMMITS_MD}")

    new_row = (
        f"| {date_str} | {author} | `{branch}` "
        f"| [{short_sha}]({commit_url}) | {message} |\n"
    )
    content = content.replace(MARKER, new_row + MARKER)

    with open(COMMITS_MD, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Appended commit {short_sha} ({branch}) by {author}")


if __name__ == "__main__":
    main()
