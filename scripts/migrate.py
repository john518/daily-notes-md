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
SACSID = os.getenv("LEGACY_SACSID")


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


def fetch_data(yymm: str) -> list | None:
    try:
        start_date, end_date = get_date_range(yymm)
    except ValueError as e:
        print(f"Error: {e}")
        raise RuntimeError(f"Error processing month {yymm}")

    # Query the range API
    url = f"https://daily-notes.appspot.com/api/range/{start_date}-{end_date}/limit=35"
    print(f"Fetching notes for range {start_date} to {end_date}...")
    print(f"{url=}")

    cookies = {
        "SACSID": SACSID
    }
    print(f"{cookies=}")

    response = requests.get(url, cookies=cookies)
    # print(response.status_code)
    # print(response.text)
    # print(response.headers)

    if response.status_code == 401:
        print("Unauthorized (401)")
        return None

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None

    data = response.json()
    # print(data)

    entry_list = data.get("range")
    return entry_list


def write_data(entry_list: list[dict], output_dir: Path):
    """Writes entries to markdown files."""
    # print(f"Number of entries: {len(entry_list)}")
    # for entry in entry_list:
    #     full_date_code = entry.get("dc", "000000")
    #     date_code = full_date_code[2:]
    #     print(date_code)
    # Make sure directory is created
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Writing to {output_dir=}")

    for entry in entry_list:
        full_date_code = entry.get("dc", "000000")

        content = entry.get("co")
        if not content:
            print(f"Content for {full_date_code} is empty - skipping")
            continue

        date_code = full_date_code[2:]
        file_path = output_dir / f"{date_code}.md"
        with open(file_path, "w") as fp:
            fp.write(content)
            print(f"Wrote {file_path}")


def process_steps(args: argparse.Namespace):
    """Processes N months based on migration_state.csv file."""
    raise NotADirectoryError("process_steps() not yet supported")


def process_month(yymm: str, data_dir: Path) -> bool:
    """Retrieves data for 1 month from legacy system and writes to local file system."""
    entry_list = fetch_data(yymm)
    if entry_list:
        yy = yymm[:2]
        mm = yymm[2:]
        month_dir = data_dir / yy / mm
        write_data(entry_list, month_dir)
    else:
        print(f"No data found for month {yymm}")
        return False

    return True


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Download legacy daily notes from GAE web server."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Override data directory for Markdown files",
    )

    # Mutually exclusive group to specify the processing mode/sequence
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--month", metavar="yymm", help="Process a single specific month (YYMM format)")
    group.add_argument("-s", "--step", type=int, metavar="N", help="Process N months working backward from last success")

    args = parser.parse_args()

    # Make sure SACSID is defined
    if not SACSID:
        print("Error: SACSID must be set in your .env file.")
        return

    # Set data directory
    if args.data_dir is None:
        default_dir = os.getenv("DAILY_NOTES_DATA_DIR")
        if default_dir is not None:
            args.data_dir = Path(default_dir)
    if args.data_dir is None:
        raise RuntimeError("No data directory specified in CLI or .env file")
    args.data_dir.mkdir(parents=True, exist_ok=True)

    if args.step is not None:
        process_steps(args)
    elif args.month is not None:
        process_month(args.month, args.data_dir)
    else:
        print("Internal error - unrecognized CLI arguments")


if __name__ == "__main__":
    main()
