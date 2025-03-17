from json import loads

from openai import OpenAI

from src.utils.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_plant_care_advice(plant_name, conditions):
    """Дає рекомендації щодо догляду за рослиною."""
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
                
                Use HTML <b> tags to highlight key information, critical values, and important recommendations in the output. For example: ideal temperature range of <b>18-22°C</b>, <b>reduce watering</b> during winter, etc.
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


def analyze_plant_statistics(plant_name, statistics_data):
    """Аналізує статистику за 7 днів і генерує рекомендації."""
    
    # Формування запиту до GPT із реальними значеннями за 7 днів
    formatted_data = "\n".join(
        [
            f"{d.date.strftime('%Y-%m-%d')}: Temperature: {d.statistics.temperature}°C, "
            f"Humidity: {d.statistics.humidity}%, Soil Moisture: {d.statistics.soil_moisture}%, "
            f"Light Level: {d.statistics.light_level}"
            for d in statistics_data
        ]
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system", 
                "content": """
                You are a plant care expert. Analyze the given 7-day statistics and provide clear, concise, and actionable care recommendations in <important>Ukrainian</important>.
                
                Your response should include:
                - 🌡 <important>Temperature</important>: Identify patterns and suggest improvements.
                - 💦 <important>Humidity</important>: Determine if adjustments are needed.
                - 🌱 <important>Soil Moisture</important>: Recommend watering frequency.
                - 🌞 <important>Light Level</important>: Assess if the plant is getting sufficient light.
                - ⚠️ <important>Warnings</important>: Highlight any critical issues that require immediate attention.
                
                Do not assume optimal ranges; determine them based on the provided data and general plant care knowledge. Format your response into short, distinct paragraphs with emojis.
                
                Use HTML <b> tags to highlight key information, critical values, and important recommendations in your output. For example: temperature is <b>too low</b>, increase watering to <b>twice per week</b>, etc.
                """
            },
            {
                "role": "user", 
                "content": f"""
                Plant: {plant_name}
                
                Data for the last 7 days:
                {formatted_data}
                """
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "plant_statistics_analysis",
                "schema": {
                    "type": "object",
                    "properties": {
                        "advice": {
                            "description": "Аналіз стану рослини на основі даних за останні 7 днів",
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