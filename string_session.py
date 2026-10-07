"""
Generate Telethon String Session for Tanya UserBot
Run this locally: python string_session.py
"""

from telethon import TelegramClient
from telethon.sessions import StringSession

print("=" * 50)
print("   Tanya UserBot - String Session Generator")
print("=" * 50)
print()

API_ID = input("Enter your API_ID (from my.telegram.org): ").strip()
API_HASH = input("Enter your API_HASH: ").strip()

if not API_ID.isdigit():
    print("❌ API_ID must be a number!")
    exit(1)

API_ID = int(API_ID)

print("\n📱 A login code will be sent to your Telegram app...")
print("   (If 2FA is enabled, you will be asked for password)\n")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n" + "=" * 50)
    print("✅ YOUR STRING SESSION (Copy this carefully):")
    print("=" * * 50)
    print(client.session.save())
    print("=" * 50)
    print("\n⚠️  NEVER share this string with anyone!")
    print("   Paste it in Render Environment Variables as STRING_SESSION")
