import os
import json
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
class GetHotelInput(TypedDict):
    city: str
    budget: int

@function_tool
@cl.step(type="Hotels")
async def suggest_hotel(wrapper: RunContextWrapper, input: GetHotelInput) -> dict:
    """Return a list of suggested hotels in a given city under a specific budget."""
    print("Tools Call: Suggest Hotel")
    try:
        prompt = (
            f"List 5 hotels in {input['city']} within a budget of {input['budget']} USD per night. "
            f"Include hotel name, location, star rating, price per night in USD, and one-line description. "
            f"Return the result in valid JSON format as a list of objects."
        )

        response = await client.chat.completions.create(
            model="gemini-2.0-flash", 
            messages=[{"role": "user", "content": prompt}]
        )

        hotel_data_raw = response.choices[0].message.content.strip()
        print(hotel_data_raw, "hotel_data_raw")

        return {"hotels": hotel_data_raw}

    except Exception as e:
        print(f"Error in tool {str(e)}")
        return {"error": f"Error in tool {str(e)}"}
