from UCLAHacks.templates import ThemeState, template

import reflex as rx
import pandas as pd
import json

import google.generativeai as genai
GOOGLE_API_KEY = "YOUR-OWN-KEY"

class AIState(rx.State):
    is_program_loaded: bool = False
    
    def Generate_Prompt(self):
        self.is_program_loaded = False

        """
        At the command line, only need to run once to install the package via pip:

        $ pip install google-generativeai
        """

        from pathlib import Path

        genai.configure(api_key=GOOGLE_API_KEY)

        """
        At the command line, only need to run once to install the package via pip:

        $ pip install google-generativeai
        """

                
        # Set up the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        with open('../UCLAHacks/UCLAHacks/data.json', 'r') as file:
            data = json.load(file)
        
            system_instruction = f"""Generate a 7-day workout plan based on the following user data:
{{
    "name": "{data['name']}",
    "weight": "{data['weight']}",
    "height": "{data['height']}",
    "age": "{data['age']}",
    "sex": "{data['sex']}",
    "shoulder_width": {data['shoulder_width']},
    "hip_width": {data['hip_width']},
    "bmi": {data['bmi']},
    "shoulder_hip_ratio": {data['shoulder_hip_ratio']},
    "goals": "{data['goals']}",
    "problems": "{data['problems']}",
    "experience": "{data['experience']}",
    "time": "{data['time']}",
    "access": "{data['access']}",
    "preference": "{data['preference']}"
}}
Based on this data, generate a workout plan in JSON format with the following structure:
{{
    "Day 1": {{
        "Focus": "<Focus for Day 1>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 2": {{
        "Focus": "<Focus for Day 2>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 3": {{
        "Focus": "<Focus for Day 3>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 4": {{
        "Focus": "<Focus for Day 4>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 5": {{
        "Focus": "<Focus for Day 5>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 6": {{
        "Focus": "<Focus for Day 6>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }},
    "Day 7": {{
        "Focus": "<Focus for Day 7>",
        "Exercises": [
            {{
                "Name": "<Exercise Name>",
                "Sets": <Number of Sets>,
                "Reps": "<Number of Reps or Range>",
                "Rest": "<Rest Time>",
                "Intensity": "<Intensity Description>"
            }}
        ]
    }}
}}
Note: Only replace the placeholders enclosed in angle brackets (e.g., <Focus for Day 1>, <Exercise Name>, etc.). Do not change the structure or remove any parts of the template.
"""

      




        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    system_instruction=system_instruction,
                                    safety_settings=safety_settings)

    
        response = model.generate_content(system_instruction)
        print(response.text)
        
        workout_plan = json.loads(response.text)
        
        
        with open('../UCLAHacks/UCLAHacks/output.json', 'w') as f:
            json.dump(workout_plan, f, indent=4)
            
        self.is_program_loaded = True
        

@template(route="/Program", title="Program")
def Program() -> rx.Component:
    
    # Return all the day components stacked vertically
    return rx.vstack(
        rx.heading("AI Program", size="6", align="center", style={"width": "100%"}),
        rx.button("Generate Program", color_scheme="blue", on_click=AIState.Generate_Prompt),
        rx.text("Click generate program and wait around a minute for your custom workout plan!"),
        rx.cond(
            AIState.is_program_loaded,
            rx.button("Click here to see program", color_scheme="blue", on_click=rx.redirect("/Schedule"))
        ),
        # need to output workout plan here
        spacing="5",
        style={"width": "100%"},
        align="center",
    )