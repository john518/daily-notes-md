from pathlib import Path
import webview

def main():
    # Get absolute path to the built index.html
    dist_path = Path("client/dist/index.html").resolve().as_uri()

    webview.create_window(
        title="Daily Notes MD - Production Build",
        url=dist_path,
        width=1024,
        height=768,
        resizable=True
    )
    webview.start()

if __name__ == "__main__":
    main()
