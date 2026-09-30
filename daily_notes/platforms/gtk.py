"""GTK-specific window cosmetics for pywebview on Linux."""

import gi

# pywebview's Linux backend relies on WebKit2, which uses GTK 3.
# GTK 3 and GTK 4 C-libraries cannot coexist in the same process.
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def set_custom_header(window, bg_color="#2c3e5", text_color="#ff00ff"):
    """
    Configures a unique header bar style for a specific window instance.
    """

    # Create GTK header bar
    header_bar = Gtk.HeaderBar()
    header_bar.set_show_close_button(True)
    # header_bar.set_title(window.get_title())

    # Give this specific header bar a unique programmatic name
    header_bar.set_name("isolated-window-header")

    # Set icon
    icon_image = Gtk.Image.new_from_icon_name("daily-notes", Gtk.IconSize.BUTTON)
    icon_image.set_pixel_size(24)
    header_bar.pack_start(icon_image)

    title_label = Gtk.Label(label=" Daily Notes Markdown") # Optional leading space for separation
    title_label.set_xalign(0.0)
    header_bar.pack_start(title_label)

    # Dynamically build the CSS string from input parameters
    css_data = f"""
        #isolated-window-header {{
            background: {bg_color};
            color: {text_color};
            box-shadow: none;
            border-bottom: 1px solid rgba(0, 0, 0, 0.2);
            font-size: 12pt;
        }}
        #isolated-window-header label {{
            color: {text_color};
            font-size: 10px;
            font-weight: 600;
        }}
        #isolated-window-header button {{
            background-color: rgba(255, 255, 255, 0.1);
            color: #2c3e50;
        }}
    """

    # Load the css provider
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css_data.encode())

    # Apply the provider strictly to this header bar's context
    context = header_bar.get_style_context()
    context.add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # Add headerbar to the window
    window.set_titlebar(header_bar)
    window.show_all()


def setup_window_cosmetics(window, bg_color: str, title_color: str) -> None:
    """Hooks GTK native styling to the pywebview window's realize event."""

    # Attach to the before_show event because gtk window is instantiated then
    def _on_before_show():
        gtk_win = window.native
        if gtk_win:
            gtk_win.connect(
                "realize",
                lambda widget: set_custom_header(widget, bg_color, title_color),
            )

    window.events.before_show += _on_before_show
