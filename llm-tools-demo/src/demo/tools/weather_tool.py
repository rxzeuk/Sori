weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather for a provided location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "A city or place name.",
                },
            },
            "required": ["location"],
        },
    },
}


def get_weather(location: str) -> dict:
    return {"location": location, "forecast": "cold and wet"}
