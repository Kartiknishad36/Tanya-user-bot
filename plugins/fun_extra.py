"""Extra Fun"""
import random
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("ship(?: |$)(.*)"))
    @errors_handler
    async def ship(event):
        args = event.pattern_match.group(1).strip().split()
        if len(args) >= 2: name1, name2 = args[0], args[1]
        elif event.is_reply:
            user = await (await event.get_reply_message()).get_sender()
            me = await event.client.get_me()
            name1, name2 = me.first_name, user.first_name if user else "Someone"
        else: return await edit_or_reply(event, "❌ Usage: `.ship Name1 Name2`")
        percent = random.randint(0, 100)
        bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
        await edit_or_reply(event, f"**❤️ Ship Meter**\n\n**{name1}** 💕 **{name2}**\n\n`[{bar}]` **{percent}%**")

    @client.on(command_pattern("decide$"))
    @errors_handler
    async def decide(event):
        await edit_or_reply(event, f"**🎱 {random.choice(['Yes ✅', 'No ❌', 'Maybe 🤔', 'Definitely! 🔥', 'Never 🚫'])}**")

    @client.on(command_pattern("choose(?: |$)(.*)"))
    @errors_handler
    async def choose(event):
        options = event.pattern_match.group(1).strip().split()
        if len(options) < 2: return await edit_or_reply(event, "❌ Usage: `.choose opt1 opt2 opt3`")
        await edit_or_reply(event, f"**🎯 I choose:** `{random.choice(options)}`")

    @client.on(command_pattern("run$"))
    @errors_handler
    async def run(event):
        await edit_or_reply(event, random.choice(["🏃 Running away...", "💨 Can't catch me!", "🚀 Boost mode!"]))
