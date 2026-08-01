from mcp.server.fastmcp import FastMCP
import requests
import os

from dotenv import load_dotenv
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Mcp Creation
mcp = FastMCP("Wheather Server")

# Creating Tools of Mcp

# First Tool : get_wheather_Forecast
@mcp.tool()
def get_current_weather(city:str):
    """
    Get current weather for a city using OpenWeather API.
    Args:
        city: City name (e.g. "Delhi")

    Returns:
        Dictionary containing weather information.
    """
    
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(
        url ,
        params={
            "q":city,
            "appid":OPENWEATHER_API_KEY,
            "units":"metric"
        }
    )
    
    data = response.json()
    
    if response.status_code != 200:
        return data

    return {
        "city": data["name"],
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

# 2nd Tool : get_forecast
@mcp.tool()
def get_forecast(city:str):
    """
    Get weather forecast for a city.

    Args:
        city: City name (e.g. "Delhi")

    Returns:
        List of forecast dictionaries.    
    """
    
    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        )
    
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    forecast = []

    # Return first 5 forecast entries
    for item in data["list"][:5]:

        forecast.append(
            {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"]
            }
        )

    return {
        "city": city,
        "forecast": forecast
    }


if __name__ == "__main__":
    mcp.run()
    

    


