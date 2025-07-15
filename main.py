import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv

from agents import(
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    Agent,
    function_tool
)
from openai.types.responses import ResponseTextDeltaEvent



load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)


# Tools
@function_tool
@cl.step(type="Flights")
def get_flights(from_city: str, to_city: str) -> dict:
    """return a list of flight based on provided arguments"""
    if from_city.lower() == "lahore" and to_city.lower() == "dubai":
        return {
            "flights": [
                {"airline": "FlyHigh", "price": 300, "time": "9:00 AM"},
                {"airline": "SkyLine", "price": 280, "time": "1:30 PM"}
            ]
        }
    elif from_city.lower() == "karachi" and to_city.lower() == "istanbul":
        return {
            "flights": [
                {"airline": "Turkish Delight", "price": 500, "time": "11:00 AM"},
                {"airline": "AirKarachi", "price": 480, "time": "5:30 PM"}
            ]
        }
    else:
        return {
            "flights": [
                {"airline": "No Flights Found", "price": 0, "time": "N/A"}
            ]
        }







@function_tool
@cl.step(type="Hotels")
def suggest_hotels(city: str) -> dict:
    """
    Suggest hotels in a given city under a specific budget.
    """
    if city.lower() == "dubai":
        return {
            "hotels": [
                {"name": "Budget Stay Dubai", "price": 80, "rating": 4},
                {"name": "City Inn", "price": 95, "rating": 4.2}
            ]
        }
    elif city.lower() == "lahore":
        return {
            "hotels": [
                {"name": "Lahore Suites", "price": 45, "rating": 3.8},
                {"name": "Model Town Inn", "price": 50, "rating": 4}
            ]
        }
    else:
        return {
            "hotels": [
                {"name": "No hotels found in budget", "price": 0, "rating": 0}
            ]
        }






# Agents
destination_agent = Agent(
    name="Destination Agent",
    instructions="""
    Help user choose destinations based on their mood, interests, or preferences.
    You can recommend beaches, cities, mountains etc.
    """,
    tools=[]
)





booking_agent = Agent(
    name="Booking Agent",
    instructions="""
    Help user simulate travel booking by checking available flights and hotels.
    Use tools get_flights and suggest_hotels.
    """,
    tools=[get_flights, suggest_hotels]
)




explore_agent = Agent(
    name="Explore Agent",
    instructions="""
    Suggest food places, attractions, and activities in a city.
    Reply naturally based on city or destination provided by user.
    """,
    tools=[]
)






travel_designer_agent = Agent(
    name="AI Travel Designer Agent",
    instructions="""
    You are a travel planner. The user will ask about travel, destinations, bookings, or attractions.
    Based on the query, you must hand off to the right agent.
    Only reply to travel-related queries.
    """,
    handoffs=[destination_agent, booking_agent, explore_agent]
)





@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message("Hello! I am a Travel Designer Agent").send()



@cl.on_message
async def main(message: cl.Message):
    try:
        history = cl.user_session.get("history")

        msg = cl.Message(content="Thinking...")
        await msg.send()

        history.append({"role": "user", "content": message.content})


        result = Runner.run_streamed(
            travel_designer_agent,
            input=history,
            run_config=config
        )


        collected = ''

        async for event in result.stream_events():

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                token = event.data.delta
                collected += token
                await msg.stream_token(token)

        history.append({"role": "assistant", "content": result.final_output})

        msg.content = collected
        await msg.update()

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        # await cl.Message(msg.content).send()
        await msg.update()
        raise
    

    


