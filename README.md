# AI Travel Designer Agent ✈

An AI-powered multi-agent system designed to guide users in the Traveling.

---

## 🧠 How It Works

### 🧩 Agents Involved:

1. **travel_designer_agent** – The main agent that:
   - Receives user input.
   - Validates whether the question is related to `travel`, `destinations` or `bookings`.
   - Rejects irrelevant questions politely.
   - Hands off the task to one of the specialized agents based on context.

2. **destination_agent** – Help user choose destinations based on their mood, interests, or preferences.
    You can recommend beaches, cities, mountains etc.

3. **booking_agent** –     Help user simulate travel booking by checking available flights and hotels.
    Use `tools get_flights` and `suggest_hotels`.

4. **explore_agent** – Suggest food places, attractions, and activities in a city.
    Reply naturally based on city or destination provided by user.
---

## 🔧 Tool Used

### `get_flights(from_city: str, to_city: str) -> dict`

A mock function that return a list of flight based on provided cities.

### `suggest_hotels(city: str) -> dict`

Suggest hotels in a given city under a specific budget.


---

## 🛠️ Technologies

- Python 
- Chainlit (for chat interface)
- OpenAI Agent SDK
- Mock tools + multi-agent system
- Handsoff


