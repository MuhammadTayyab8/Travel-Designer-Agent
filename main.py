import chainlit as cl
from expert.travel_designer_agent import travel_designer_agent
from setup_config import config

from agents import(
    Runner,
)
from openai.types.responses import ResponseTextDeltaEvent




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
    

    


