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
                "content": "You are an expert in plant care. Provide helpful plant care advice based on the information provided. The answer should be short and clear. Answer in Ukrainian."
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