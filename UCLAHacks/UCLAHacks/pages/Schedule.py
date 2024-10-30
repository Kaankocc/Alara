from UCLAHacks.templates import ThemeState, template
import reflex as rx
import json
import pandas as pd

@template(route="/Schedule", title="Schedule")
def Schedule() -> rx.Component:
    # Load the JSON file
    with open('../UCLAHacks/UCLAHacks/output.json', 'r') as file:
        workout_plan = json.load(file)

    day_components = []

    # Iterate over the dictionary
    for day, details in workout_plan.items():
        exercises = details['Exercises']
        # Create a DataFrame for the exercises
        df = pd.DataFrame(exercises)
        # Create a table for the exercises
        table = rx.data_table(
            data=df,
            pagination=True,
            search=False,
            sort=True
        )
        # Construct the title for the table (day and muscle group)
        title = f"{day}: {details['Focus']}"
        # Construct the component for this day's workout plan
        day_component = rx.vstack(
            rx.heading(title, size="5", align="center"),
            table,
            spacing="5",
            style={"width": "100%"},
            align="center",
        )
        # Append the day component to the list
        day_components.append(day_component)

    # Return the constructed components
    return rx.vstack(
        rx.heading("Schedule", size="6", align="center", style={"width": "100%"}),
        *day_components,
        spacing="5",
        style={"width": "100%"},
        align="center",
    )
