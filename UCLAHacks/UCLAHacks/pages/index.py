"""The home page of the app."""

from UCLAHacks import styles
from UCLAHacks.templates import template
import reflex as rx

def introduction_text() -> rx.Component:
    """Component displaying introductory text about the system."""
    return rx.box(
        rx.text("Welcome to Your Personal Fitness Assistant!", size="6", align="center"),
        rx.text("We use advanced AI to analyze your body and provide customized workout plans.", align="center"),
        rx.text("Start by going to the Body Scanner to capture your body measurements.", align="center"),
        spacing="3",
        style={"width": "100%"},
        align="center"
    )

def place_image() -> rx.Component:
    return rx.image(src="/AlaraLogo.png", height="28em", style={"flex-grow": "0"})

@template(route="/", title="Home")
def index() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Everyone's\nTrainer", size="9", align="right", style={"flex-grow": "1"}),
            place_image(),
            style={"width": "100%", "align-items": "center"}
        ),
        introduction_text(),
        spacing="5",
        font_family="Montserrat", 
        style={"width": "100%"},
        align="center"
    )