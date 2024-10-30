import time
from urllib.request import urlopen
from PIL import Image
import os
import subprocess

import reflex as rx
import reflex_webcam as webcam

from UCLAHacks.templates import template
import reflex as rx

# Identifies a particular webcam component in the DOM
WEBCAM_REF = "webcam"


class CamState(rx.State):
    last_screenshot: Image.Image | None = None
    last_screenshot_timestamp: str = ""
    loading: bool = False

    def prepare_capture(self):
        time.sleep(3)

    def handle_screenshot(self, img_data_uri: str):
        """Webcam screenshot upload handler.
        Args:
            img_data_uri: The data uri of the screenshot (from upload_screenshot).
        """
        if self.loading:
            return
        self.last_screenshot_timestamp = time.strftime("%H:%M:%S")
        with urlopen(img_data_uri) as img:
            self.last_screenshot = Image.open(img)
            self.last_screenshot.load()
            filename = "Person.jpeg"
            # convert to webp during serialization for smaller size
            self.last_screenshot.save("../UCLAHacks/UCLAHacks/pages/humanPose/Pics/"+filename, "JPEG")  # type: ignore
            
            subprocess.run(["../UCLAHacks/.venv/bin/python3", "../UCLAHacks/UCLAHacks/pages/humanPose/lahackstest.py"])


def last_screenshot_widget() -> rx.Component:
    """Widget for displaying the last screenshot and timestamp."""
    return rx.box(
        rx.cond(
            CamState.last_screenshot,
            rx.fragment(
                rx.image(src=CamState.last_screenshot),
                rx.text(CamState.last_screenshot_timestamp),
            ),
            rx.center(
                rx.text("Click image to capture.", size="4"),
                ),
        ),
        height="270px",
    )

def delayPic():
    time.sleep(3)
    
    webcam.upload_screenshot(ref=WEBCAM_REF, handler=CamState.handle_screenshot)
    
    

def webcam_upload_component(ref: str) -> rx.Component:
    """Component for displaying webcam preview and uploading screenshots.
    Args:
        ref: The ref of the webcam component.
    Returns:
        A reflex component.
    """
    return rx.vstack(
        webcam.webcam(
            id=ref,
            on_click=[CamState.prepare_capture, webcam.upload_screenshot(ref=ref, handler=CamState.handle_screenshot), rx.redirect("/scanner")],  # type: ignore
        ),
        rx.box(
            border_radius="5px", 
            border="2px solid red", 
            position="absolute",
            #Bounding Box
            width="150px",
            height="350px",
            top="195px",
            left="625px",
        ),
        last_screenshot_widget(),
        width="640px",
        height="480px",
        align="start",
    )

@template(route="/camera", title="Camera")
def camera() -> rx.Component:
    return rx.fragment(
        webcam_upload_component(WEBCAM_REF),
    )