import os 
import json 
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from aiohttp import ClientSession
import asyncio
import sys



# Load and access the api key 
load_dotenv(dotenv_path=".env")

# constants 
api_key = os.getenv("API_KEY")
base_url = "http://dataservice.accuweather.com"

# Create an MCP server
mcp = FastMCP("Weather-Info")

# Helper function to get the location ID where we want to find the weather
async def location_id(location: str):
    async with ClientSession() as session:
        location_search_url = f"{base_url}/locations/v1/cities/search"
        params = {
            "apikey": api_key,
            "q": location,
        }
        async with session.get(location_search_url, params=params) as response:
            locations = await response.json()
            if locations and len(locations) > 0:
                location_key = locations[0]["Key"]
                return location_key
            return None


# Call the weather API and then return weather
@mcp.tool()
async def weather(city: str):
    """ 
    Give me the weather for the city that the user gave you using this function. 
    """
    try:
        # First get the location key
        city_key = await location_id(city)
        if not city_key:
            return f"Did not find city: {city}"
            
        # Get current conditions
        async with ClientSession() as session:
            current_conditions_url = f"{base_url}/currentconditions/v1/{city_key}"
            params = {
                "apikey": api_key,
                "metric": "true",
            }

            async with session.get(current_conditions_url, params=params) as response:
                current_conditions = await response.json()
                
                if current_conditions and len(current_conditions) > 0:
                #     # Return the weather information as a formatted string
                #     weather_text = current_conditions[0].get("WeatherText", "Unknown")
                #     temperature = current_conditions[0].get("Temperature", {}).get("Metric", {}).get("Value", "Unknown")
                    
                    # return f"Current weather in {city}: {weather_text}, Temperature: {temperature}°C"
                    return current_conditions
    except Exception as e:
        return f"Error retrieving weather: {str(e)}"


if __name__ == "__main__":

    mcp.run(transport="stdio")

# mcp dev main.py         // Insert the API key into the environment variables // success 
# But when I try it in claude it does not work it sasys that the module AIOHTTP it cannot ve read 

#python3 ./main.py            

#uv run mcp install main.py       