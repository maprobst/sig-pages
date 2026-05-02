#!/usr/bin/env python3
"""Sends a Teams Adaptive Card notification for a commit merged into main."""

import json
import os
import urllib.error
import urllib.request
from datetime import datetime


def main() -> None:
    webhook_url = os.environ["TEAMS_WEBHOOK_URL"]
    commit_sha = os.environ["COMMIT_SHA"]
    short_sha = commit_sha[:7]
    author = os.environ["COMMIT_AUTHOR"]
    message = os.environ["COMMIT_MESSAGE"]
    first_line = message.split("\n")[0]
    timestamp = os.environ["COMMIT_TIMESTAMP"]
    commit_url = os.environ["COMMIT_URL"]
    repo_name = os.environ["REPO_NAME"]
    repo_url = os.environ["REPO_URL"]
    branch = os.environ["BRANCH_NAME"]

    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    date_str = dt.strftime("%Y-%m-%d %H:%M UTC")

    # Adaptive Card payload for Teams Workflows webhook
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"Neuer Commit in **[{repo_name}]({repo_url})** (`{branch}`)",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True,
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "Autor", "value": author},
                                {
                                    "title": "Commit",
                                    "value": f"[{short_sha}]({commit_url})",
                                },
                                {"title": "Datum", "value": date_str},
                                {"title": "Nachricht", "value": first_line},
                            ],
                        },
                    ],
                },
            }
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print(f"Teams notification sent (HTTP {resp.status}): {body}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        raise SystemExit(
            f"ERROR: Teams webhook returned HTTP {exc.code}: {body}"
        ) from exc


if __name__ == "__main__":
    main()
