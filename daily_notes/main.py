from pathlib import Path
import webview

from daily_notes.api import Api
from daily_notes.storage import Storage

from daily_notes.platforms import setup_window_cosmetics


def get_target_window_size(scale=0.8):
    """Calculates window size as a percentage of the primary monitor resolution."""
    screen = webview.screens[0]
    width = int(screen.width * scale)
    height = int(screen.height * scale)

    return width, height


def main():
    storage = Storage()
    api = Api(storage=storage)

    win_width, win_height = get_target_window_size(scale=0.8)

    # Get absolute path to the built index.html
    dist_path = Path("client/dist/index.html").resolve().as_uri()

    window = webview.create_window(
        title="Daily Notes Markdown",
        url=dist_path,
        width=win_width,
        height=win_height,
        resizable=True,
        js_api=api  # Expose Api methods to window.pywebview.api
    )

    # Apply window styling
    slate_teal_gray = "#8c969b"
    setup_window_cosmetics(window, bg_color=slate_teal_gray, title_color="white")

    # webview.start(debug=True)  # opens browser dev tools
    webview.start()

if __name__ == "__main__":
    main()
