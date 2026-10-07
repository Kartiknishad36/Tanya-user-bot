"""
Fun & Entertainment Plugin
"""

import random
import httpx
from telethon import events
from utils.helpers import edit_or_reply, command_pattern

QUOTES = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Innovation distinguishes between a leader and a follower. – Steve Jobs",
    "Stay hungry, stay foolish. – Steve Jobs",
    "Life is what happens when you're busy making other plans. – John Lennon",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "Everything you’ve ever wanted is on the other side of fear. – George Addair",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
]

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the bicycle fall over? Because it was two tired!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why can't you give Elsa a balloon? Because she will let it go!",
    "What did the ocean say to the beach? Nothing, it just waved!",
    "Why did the math book look so sad? Because it had too many problems!",
    "What do you call a bear with no teeth? A gummy bear!",
]

TRUTHS = [
    "What's the most embarrassing thing you've ever done?",
    "Have you ever lied to your best friend?",
    "What's your biggest fear?",
    "Who was your first crush?",
    "What's the worst thing you've ever done at school/work?",
    "Have you ever cheated on a test?",
    "What's one thing you'd change about yourself?",
    "What's your biggest secret?",
]

DARES = [
    "Send a funny selfie to the group.",
    "Talk in a different accent for the next 5 messages.",
    "Do 10 push-ups and send a video.",
    "Change your Telegram bio to something embarrassing for 1 hour.",
    "Sing a song and send the voice note.",
    "Tell a joke in the group.",
    "Act like a cat for the next 3 messages.",
]


def register(client):
    @client.on(command_pattern("quote$"))
    async def quote(event):
        q = random.choice(QUOTES)
        await edit_or_reply(event, f"**💬 Quote**\n\n_{q}_")

    @client.on(command_pattern("joke$"))
    async def joke(event):
        j = random.choice(JOKES)
        await edit_or_reply(event, f"**😂 Joke**\n\n{j}")

    @client.on(command_pattern("truth$"))
    async def truth(event):
        t = random.choice(TRUTHS)
        await edit_or_reply(event, f"**🔵 Truth**\n\n{t}")

    @client.on(command_pattern("dare$"))
    async def dare(event):
        d = random.choice(DARES)
        await edit_or_reply(event, f"**🔴 Dare**\n\n{d}")

    @client.on(command_pattern("meme$"))
    async def meme(event):
        msg = await edit_or_reply(event, "🔍 Finding a meme...")
        try:
            async with httpx.AsyncClient() as http:
                r = await http.get("https://meme-api.com/gimme", timeout=10)
                data = r.json()
                title = data.get("title", "Meme")
                url = data.get("url")
                await event.client.send_file(
                    event.chat_id,
                    url,
                    caption=f"**😂 {title}**",
                )
                await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Failed to fetch meme: `{e}`")
