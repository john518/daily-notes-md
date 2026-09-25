import webview

def main():
    # Simple inline HTML to test the webview rendering
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Notes MD - Test</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f9;
                color: #333;
            }
            .card {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Daily Notes Markdown</h1>
            <p>pywebview is up and running successfully!</p>
        </div>
    </body>
    </html>
    """

    # Create the native window
    webview.create_window(
        title="Daily Notes Markdown - Test",
        html=html,
        width=800,
        height=600,
        resizable=True
    )

    # Start the application event loop
    webview.start()

if __name__ == "__main__":
    main()
