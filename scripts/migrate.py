# /// script
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

"""
Legacy Daily Notes Migration Script

This script queries the legacy Daily Notes website API for a specific month's
notes (specified in YYMM format), saves a raw JSON backup, and converts the
entries into individual local Markdown files.

- Requires a .env file specifying the current Daily Notes authenticaion cookie

Usage:
    uv run migrate.py <YYMM> [--output-dir <dir>]

Example:
    uv run migrate.py 1306
"""

import argparse
import calendar
import json
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

# Load credentials from .env file
load_dotenv()

# Get authorization cookie
SACSID = os.getenv("SACSID")


def get_date_range(yymm_str):
    """Converts YYMM string (e.g. '1306') into start and end dates."""
    if len(yymm_str) != 4 or not yymm_str.isdigit():
        raise ValueError("Format must be YYMM (e.g., 1306 for June 2013)")

    yy = int(yymm_str[:2])
    mm = int(yymm_str[2:])

    year = 2000 + yy
    month = mm

    if not (1 <= month <= 12):
        raise ValueError("Month must be between 01 and 12")

    start_date = f"{year:04d}{month:02d}01"
    last_day = calendar.monthrange(year, month)[1]
    end_date = f"{year:04d}{month:02d}{last_day:02d}"

    return start_date, end_date


def main():
    parser = argparse.ArgumentParser(
        description="Download legacy daily notes from GAE web server."
    )
    parser.add_argument(
        "yymm",
        type=str,
        help="Month and year in YYMM format (e.g., 1306 for June 2013)",
    )
    parser.add_argument(
        "--output-dir",
        default="./legacy_output",
        help="Directory to save raw JSON and generated Markdown files",
    )
    args = parser.parse_args()

    try:
        start_date, end_date = get_date_range(args.yymm)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if not SACSID:
        print("Error: SACSID must be set in your .env file.")
        return

    # Query the range API
    url = f"https://daily-notes.appspot.com/api/range/{start_date}-{end_date}/limit=35"
    print(f"Fetching notes for range {start_date} to {end_date}...")
    # url="https://daily-notes.appspot.com/api/range/20260927-20261101/limit=35"
    print(f"{url=}")

    cookies = {
        "SACSID": SACSID
    }

    response = requests.get(url, cookies=cookies)
    # print(response.status_code)
    # print(response.text)
    # print(response.headers)

    if response.status_code == 401:
        print("Unauthorized (401)")
        return

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return

    data = response.json()
    # print(data)

    entry_list = data.get("range")
    if not entry_list:
        print("No range found in data")
        return

    print(f"Number of entries: {len(entry_list)}")
    for entry in entry_list:
        full_date_code = entry.get("dc")
        date_code = full_date_code[2:]
        print(date_code)

    return

    # Create output directory and save raw JSON backup
    os.makedirs(args.output_dir, exist_ok=True)
    json_path = os.path.join(args.output_dir, f"raw_{args.yymm}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved raw JSON to {json_path}")

    # Parse and write individual Markdown files
    notes = data if isinstance(data, list) else data.get("notes", [])

    if not notes:
        print(
            "No notes found or unexpected JSON structure. Inspect raw JSON file."
        )
        return

    print(f"Writing {len(notes)} markdown files to {args.output_dir}/...")
    for note in notes:
        note_date = note.get("date", "unknown-date").replace("/", "-")
        content = note.get("content", "")
        title = note.get("title", "")

        md_path = os.path.join(args.output_dir, f"{note_date}.md")
        with open(md_path, "w") as f:
            if title:
                f.write(f"# {title}\n\n")
        f.write(content)

    print("Migration batch complete!")


if __name__ == "__main__":
    main()
