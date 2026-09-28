"""UI platform abstraction layer for Bucket Ledger UI."""

import sys


def setup_window_cosmetics(window, bg_color: str, title_color: str) -> None:
    """Applies native window cosmetics if running on a supported platform (Linux/GTK)."""

    # Only attempt GTK styling on Linux
    print(f"{sys.platform=}")
    if sys.platform.startswith("linux"):
        try:
            from .gtk import setup_window_cosmetics as apply_gtk_cosmetics

            apply_gtk_cosmetics(window, bg_color, title_color)
        except (ImportError, ValueError) as e:
            # GTK or PyGObject bindings not installed; pass silently
            print(f"[UI] GTK cosmetics bypassed: {e}")
    else:
        # On Windows (win32) / macOS (darwin), pywebview handles titlebars natively
        pass
