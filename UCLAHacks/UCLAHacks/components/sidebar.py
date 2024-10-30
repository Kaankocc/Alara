"""Sidebar component for the app."""

from UCLAHacks import styles

import reflex as rx



def sidebar_header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.
    """
    return rx.hstack(
        # The logo.
        rx.image(src="/Alara_White.png", height="4em"),
        rx.spacer(),
        rx.link(
            rx.button(
                rx.icon("github"),
                color_scheme="gray",
                variant="soft",
            ),
            href="https://github.com/reflex-dev/reflex",
        ),
        align="center",
        width="100%",
        border_bottom=styles.border,
        padding_x="1em",
        padding_y="2em",
    )


def sidebar_footer() -> rx.Component:
    """Sidebar footer.

    Returns:
        The sidebar footer component.
    """
    return rx.hstack(
        rx.spacer(),
        rx.link(
            rx.text("Docs"),
            href="https://reflex.dev/docs/getting-started/introduction/",
            color_scheme="gray",
        ),
        rx.link(
            rx.text("Blog"),
            href="https://reflex.dev/blog/",
            color_scheme="gray",
        ),
        width="100%",
        border_top=styles.border,
        padding="1em",
    )


def sidebar_item(text: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.
    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Home"
    )

    return rx.link(
        rx.hstack(
            rx.text(
                text,
            ),
            bg=rx.cond(
                active,
                rx.color("accent", 2),
                "transparent",
            ),
            border=rx.cond(
                active,
                f"1px solid {rx.color('accent', 6)}",
                f"1px solid {rx.color('gray', 6)}",
            ),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            align="center",
            border_radius=styles.border_radius,
            width="100%",
            padding="1em",
        ),
        href=url,
        width="100%",
    )


from reflex.page import get_decorated_pages

def sidebar() -> rx.Component:
    """Constructs the sidebar component with filtered pages."""
    # Get all the decorated pages
    pages = get_decorated_pages()

    # Optionally filter out pages, e.g., exclude the camera page
    filtered_pages = [page for page in pages if page["route"] != "/camera"]

    return rx.box(
        rx.vstack(
            sidebar_header(),  # The top part of the sidebar
            rx.vstack(
                *[
                    sidebar_item(
                        # Customize text appearance or add conditions
                        text=customize_page_title(page),
                        url=page["route"],
                    )
                    for page in filtered_pages  # Use the filtered list
                ],
                width="100%",
                overflow_y="auto",  # Allows scrolling within the sidebar
                align_items="flex-start",  # Align items to the start of the flex axis
                padding="1em",
            ),
            rx.spacer(),  # Adds space between items
            sidebar_footer(),  # The bottom part of the sidebar
            height="100dvh",
        ),
        display=["none", "none", "block"],  # Responsive visibility settings
        min_width=styles.sidebar_width,
        height="100%",
        position="sticky",
        top="0px",
        border_right=styles.border,
    )

def customize_page_title(page) -> str:
    """Customizes the page title based on specific logic."""
    # Example: Capitalize each word and prepend 'Menu: '
    title = page.get("title", page["route"].strip("/").capitalize())
    return title.replace("_", " ").title()
