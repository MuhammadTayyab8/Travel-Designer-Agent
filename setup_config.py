import os
from dotenv import load_dotenv, find_dotenv

from agents import(
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
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