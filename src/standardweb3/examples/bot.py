import asyncio
from bot import Bot
from types.orderbook import TickEvent

# Initialize the bot with the server URL
bot = Bot("http://your-server-url")

# Developers can configure their own logic for the 'tick' event
@bot.on("tick")
async def handle_tick_event(data):
    tick_event = TickEvent(**data)
    print(f"Received TickEvent: {tick_event}")
    # Add custom async logic here
    await asyncio.sleep(1)  # Example async operation


if __name__ == "__main__":
    asyncio.run(bot.run())
