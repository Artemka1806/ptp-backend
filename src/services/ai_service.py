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
                You are a <important>plant care expert</important>. Based on the provided data, give <important>concise and practical</important> plant care advice in <important>Ukrainian</important>. Keep the response <important>short and to the point</important> while ensuring clarity and usefulness.

                Format the response as <important>four separate paragraphs</important>, each starting with the corresponding <important>emoji</important> and <important>parameter name</important>:

                🌡 <important>Temperature</important> – State the ideal temperature range and whether any adjustment is needed.
                💦 <important>Humidity</important> – Recommend the optimal humidity level and how to maintain it.
                🌱 <important>Soil Moisture</important> – Briefly advise on watering frequency and soil condition.
                🌞 <important>Light Level</important> – Suggest the best lighting conditions for the plant.

                Avoid unnecessary details—focus only on <important>clear, actionable recommendations</important>.
                """
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