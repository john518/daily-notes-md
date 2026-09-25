from pathlib import Path
import webview

from daily_notes.api import Api

def main():
    api = Api()

    # Get absolute path to the built index.html
    dist_path = Path("client/dist/index.html").resolve().as_uri()

    webview.create_window(
        title="Daily Notes Markdown",
        url=dist_path,
        width=1024,
        height=768,
        resizable=True,
        js_api=api  # Expose Api methods to window.pywebview.api
    )
    # webview.start(debug=True)  # opens browser dev tools
    webview.start()

if __name__ == "__main__":
    main()
