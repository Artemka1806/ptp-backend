from json import loads

from openai import OpenAI

from src.utils.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_plant_care_advice(plant_name, conditions):
    """Get plant care advice based on the provided plant and conditions"""
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "developer", 
                "content": """
                You are an expert in plant care. Based on the provided information, give concise and helpful plant care advice. The response should be in Ukrainian and structured into separate paragraphs according to the following parameters:

                🌡 Temperature – Provide recommendations based on the optimal temperature range for the plant.
                💦 Humidity – Advise on the required air humidity and how to maintain it.
                🌱 Soil Moisture – Explain the ideal soil moisture level and watering frequency.
                🌞 Light Level – Give guidance on the appropriate lighting conditions.

                Each paragraph should start with the corresponding emoji and parameter name for clarity."""
            },
            {
                "role": "user", 
                "content": f"Plant: {plant_name}\nConditions: {conditions}"
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "plant_care_advice_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "advice": {
                            "description": "Expert advice on plant care based on the provided conditions",
                            "type": "string"
                        }
                    },
                    "required": ["advice"],
                    "additionalProperties": False
                }
            }
        }
    )
    
    return loads(response.choices[0].message.content)