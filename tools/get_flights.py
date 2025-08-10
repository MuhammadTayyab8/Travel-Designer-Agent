import os
from dotenv import find_dotenv, load_dotenv
from agents import AsyncOpenAI, function_tool, RunContextWrapper
from typing import TypedDict
import chainlit as cl

# Load env variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

# Client setup
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# Input schema
class GetFlightInput(TypedDict):
    origin: str
    destination: str
    date: str

@function_tool
@cl.step(type="Flights")
async def get_flights(wrapper: RunContextWrapper, input: GetFlightInput) -> dict:
    """Return a list of flights based on provided origin, destination, and date."""
    print("Tools Call.")
    try:
        prompt = (
            f"List 5 available flights from {input['origin']} to {input['destination']} "
            f"on {input['date']}. Include airline, departure time, arrival time, and price in USD. "
            f"Return in JSON format."
        )

        response = await client.chat.completions.create(
            model="gemini-2.0-flash", 
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract and parse JSON from the response
        flight_data = response.choices[0].message.content.strip()
        print(flight_data, "flight_data")
        return {"flights": flight_data}

    except Exception as e:
        print(f"Error in tool {str(e)}")
        return {"error": f"Error in tool {str(e)}"}
