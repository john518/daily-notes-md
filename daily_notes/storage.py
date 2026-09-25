import os
from pathlib import Path

class Storage:
    class Storage:
        """Manages local filesystem persistence for daily notes markdown entries.

        Handles reading, writing, and listing of journal entries organized in a
        hierarchical YY/MM/YYMMDD.md structure beneath a configurable DATA_DIR.
        The root data directory is resolved from the environment configuration file
        at ~/.config/john.daily-notes/env, supporting environment variable expansion
        like ${HOME}, with a fallback default for development testing.
        """
    def __init__(self, config_path: str = "~/.config/john.daily-notes/env"):
        self.data_dir = self._resolve_data_dir(config_path)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_data_dir(self, config_path: str) -> Path:
        """Reads DATA_DIR from the env file, expanding variables like ${HOME}."""
        expanded_config = Path(config_path).expanduser()

        if expanded_config.exists():
            try:
                with open(expanded_config, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("DATA_DIR="):
                            raw_path = line.split("=", 1)[1].strip()
                            # Expand environment variables like ${HOME} or $HOME
                            resolved_path = os.path.expandvars(raw_path)
                            return Path(resolved_path).expanduser()
            except Exception as e:
                print(f"Warning: Failed to parse config file {expanded_config}: {e}")

        # Fallback default if config file doesn't exist yet
        fallback = Path("~/temp/daily-notes-test-data").expanduser()
        print(f"No config found or DATA_DIR not specified. Using fallback: {fallback}")
        return fallback

    def _get_file_path(self, year: int, month: int, day: int) -> Path:
        """Constructs the path: DATA_DIR / YY / MM / YYMMDD.md"""
        yy = f"{year % 100:02d}"
        mm = f"{month:02d}"
        dd = f"{day:02d}"
        filename = f"{yy}{mm}{dd}.md"
        return self.data_dir / yy / mm / filename

    def read_entry(self, year: int, month: int, day: int) -> str:
        """Reads markdown content for a given date, returning empty string if not found."""
        file_path = self._get_file_path(year, month, day)
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return ""

    def write_entry(self, year: int, month: int, day: int, content: str) -> None:
        """Writes markdown content, creating YY/MM parent directories automatically."""
        file_path = self._get_file_path(year, month, day)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            raise

    def get_month_entries(self, year: int, month: int) -> dict:
        """
        Scans the YY/MM directory and returns a dictionary mapping
        day numbers to their markdown content.
        """
        yy = f"{year % 100:02d}"
        mm = f"{month:02d}"
        month_dir = self.data_dir / yy / mm

        entries = {}
        if month_dir.exists() and month_dir.is_dir():
            for file_path in month_dir.glob("*.md"):
                # Filename format is YYMMDD.md, extract DD
                stem = file_path.stem
                if len(stem) == 6:
                    try:
                        day_num = int(stem[4:])
                        entries[day_num] = self.read_entry(year, month, day_num)
                    except ValueError:
                        continue
        return entries
