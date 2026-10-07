"""
AI Plugin - Gemini & OpenAI integration
"""

from telethon import events
from config import GEMINI_API_KEY, OPENAI_API_KEY, CMD_PREFIX
from utils.helpers import edit_or_reply, command_pattern


def register(client):
    @client.on(command_pattern("ai(?: |$)(.*)"))
    async def ai_handler(event):
        query = event.pattern_match.group(1).strip()
        if not query and event.is_reply:
            reply = await event.get_reply_message()
            query = reply.text or reply.raw_text
        if not query:
            return await edit_or_reply(event, f"❌ Usage: `{CMD_PREFIX}ai <your question>`")

        msg = await edit_or_reply(event, "🤖 Thinking...")

        if GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(query)
                answer = response.text
                await msg.edit(f"**🤖 Gemini AI**\n\n{answer}")
                return
            except Exception as e:
                await msg.edit(f"❌ Gemini Error: `{e}`\nTrying OpenAI...")

        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client_ai = OpenAI(api_key=OPENAI_API_KEY)
                response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": query}],
                    max_tokens=1500,
                )
                answer = response.choices[0].message.content
                await msg.edit(f"**🤖 ChatGPT**\n\n{answer}")
                return
            except Exception as e:
                await msg.edit(f"❌ OpenAI Error: `{e}`")
                return

        await msg.edit(
            "❌ No AI API key configured!\n\n"
            "Set `GEMINI_API_KEY` or `OPENAI_API_KEY` in environment variables."
        )

    @client.on(command_pattern("gemini(?: |$)(.*)"))
    async def gemini_handler(event):
        if not GEMINI_API_KEY:
            return await edit_or_reply(event, "❌ GEMINI_API_KEY not set!")
        query = event.pattern_match.group(1).strip()
        if not query and event.is_reply:
            reply = await event.get_reply_message()
            query = reply.text or reply.raw_text
        if not query:
            return await edit_or_reply(event, "❌ Provide a query")

        msg = await edit_or_reply(event, "✨ Gemini is thinking...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(query)
            await msg.edit(f"**✨ Gemini**\n\n{response.text}")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    @client.on(command_pattern("gpt(?: |$)(.*)"))
    async def gpt_handler(event):
        if not OPENAI_API_KEY:
            return await edit_or_reply(event, "❌ OPENAI_API_KEY not set!")
        query = event.pattern_match.group(1).strip()
        if not query and event.is_reply:
            reply = await event.get_reply_message()
            query = reply.text or reply.raw_text
        if not query:
            return await edit_or_reply(event, "❌ Provide a query")

        msg = await edit_or_reply(event, "💬 GPT is thinking...")
        try:
            from openai import OpenAI
            client_ai = OpenAI(api_key=OPENAI_API_KEY)
            response = client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": query}],
                max_tokens=1500,
            )
            await msg.edit(f"**💬 ChatGPT**\n\n{response.choices[0].message.content}")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
