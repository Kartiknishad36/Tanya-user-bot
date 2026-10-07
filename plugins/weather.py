"""Weather Plugin"""
import httpx
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("weather(?: |$)(.*)"))
    @errors_handler
    async def weather(event):
        city = event.pattern_match.group(1).strip()
        if not city:
            return await edit_or_reply(event, "❌ Usage: `.weather <city>`\nExample: `.weather Delhi`")
        msg = await edit_or_reply(event, f"🌤️ Fetching weather for **{city}**...")
        try:
            async with httpx.AsyncClient(timeout=15) as http:
                r = await http.get(f"https://wttr.in/{city}?format=3")
                if r.status_code == 200:
                    await msg.edit(f"**🌤️ Weather**\n\n`{r.text.strip()}`")
                else:
                    await msg.edit("❌ City not found")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
