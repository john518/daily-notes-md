from pathlib import Path
import webview

from daily_notes.api import Api

def main():
    api = Api()

    # Get absolute path to the built index.html
    dist_path = Path("client/dist/index.html").resolve().as_uri()

    webview.create_window(
        title="Daily Notes MD - Production Build",
        url=dist_path,
        width=1024,
        height=768,
        resizable=True,
        js_api=api  # Expose Api methods to window.pywebview.api
    )
    webview.start(debug=True)

if __name__ == "__main__":
    main()
